import cv2
import os
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QPushButton, QFileDialog, QMessageBox,QGridLayout
from PyQt5.QtCore import QTimer,Qt, QTime
from PyQt5.QtGui import QImage, QPixmap

class VideoWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("河道污染物识别")
        self.setGeometry(100, 100, 1400, 600)  # 调整窗口大小以容纳新的布局
        # 页面布局
        self.central_widget = QWidget()
        self.layout = QVBoxLayout()  # 用于上下放置
        # 设置布局的边距，左、上、右、下均为 10 像素
        self.layout.setContentsMargins(25, 25, 25, 25)
        self.setCentralWidget(self.central_widget)
        self.central_widget.setLayout(self.layout)
        # 顶部布局
        self.top_layout = QHBoxLayout()
        self.top_layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addLayout(self.top_layout)
        
        self.topG_layout = QGridLayout()
        # 创建一个用于包装表格布局的小部件
        wrapper_widget = QWidget()
        wrapper_widget.setLayout(self.topG_layout)
        self.top_layout.addWidget(wrapper_widget, alignment=Qt.AlignLeft)
            # 第一行
        self.sign_led = QLabel(self)
        self.sign_led.setFixedSize(12, 12)
        self.topG_layout.addWidget(self.sign_led,0,0)

        self.sign_lab = QLabel("信号源:", self)
        self.sign_lab.setFixedSize(50, 20)
        self.topG_layout.addWidget(self.sign_lab,0,1)

        self.sign_sta = QLabel("无", self)
        self.sign_sta.setFixedSize(200, 20)
        self.topG_layout.addWidget(self.sign_sta,0,2) 

        self.meth_led = QLabel(self)
        self.meth_led.setFixedSize(12, 12)
        self.topG_layout.addWidget(self.meth_led,0,3)

        self.meth_lab = QLabel("算法:", self)
        self.meth_lab.setFixedSize(50, 20)
        self.topG_layout.addWidget(self.meth_lab,0,4)

        self.meth_sta = QLabel("无", self)
        self.meth_sta.setFixedSize(200, 20)
        self.topG_layout.addWidget(self.meth_sta,0,5)

        self.fps_lab = QLabel("FPS:", self)
        self.fps_lab.setFixedSize(50, 20)
        self.topG_layout.addWidget(self.fps_lab,0,6)

        self.fps_sta = QLabel("0", self)
        self.fps_num = 0
        self.fps_sta.setFixedSize(50, 20)
        self.topG_layout.addWidget(self.fps_sta,0,7)
      
            # 第二行
        self.recording_led = QLabel(self)
        self.recording_led.setFixedSize(12, 12)
        self.recording_led.setStyleSheet("background-color: red;")
        self.topG_layout.addWidget(self.recording_led,1,0)

        self.recording_lab = QLabel("录制状态：", self)
        self.sign_lab.setFixedSize(50, 20)
        self.topG_layout.addWidget(self.recording_lab,1,1)

        self.recording_sta = QLabel("未开始", self)
        self.recording_sta.setFixedSize(200, 20)
        self.topG_layout.addWidget(self.recording_sta,1,2)

        # 中部布局
        self.mid_layout = QHBoxLayout()  # 用于左右放置
        self.mid_layout.setAlignment(Qt.AlignCenter)  # 设置水平居中对齐
        self.original_image_label = QLabel(self)  # 添加原始视频窗口的 QLabel
        self.processed_image_label = QLabel(self)  # 添加处理后视频窗口的 QLabel
        
        self.layout.addLayout(self.mid_layout)
        self.mid_layout.addWidget(self.original_image_label)    #加入原始图像窗口
        self.mid_layout.addWidget(self.processed_image_label)   #加入处理后图像窗口   

        # 底部布局
        self.bottom_layout = QHBoxLayout()  # 用于左右放置

        self.layout.addLayout(self.bottom_layout)
        # 添加按钮
        self.source_button = QPushButton("选择源", self)
        self.source_button.clicked.connect(self.select_source)
        self.bottom_layout.addWidget(self.source_button)

        self.realtime_button = QPushButton("实时查看", self)
        self.realtime_button.clicked.connect(self.start_realtime)
        self.bottom_layout.addWidget(self.realtime_button)

        self.play_button = QPushButton("-", self)
        self.play_button.clicked.connect(self.play_video)
        self.bottom_layout.addWidget(self.play_button)

        self.export_button = QPushButton("-", self)
        self.export_button.clicked.connect(self.export_result)
        self.bottom_layout.addWidget(self.export_button)

        self.cls = QPushButton("重置", self)
        self.cls.clicked.connect(self.cls_result)
        self.bottom_layout.addWidget(self.cls)

        self.cap = None
        self.video_path = None
        self.timer = QTimer()
        self.chkTimer = QTimer()
        self.rcodTimer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.chkTimer.timeout.connect(self.check)
        self.rcodTimer.timeout.connect(self.rcod_cnt)

        self.sign = 'None'
        self.is_recording = False
        self.play_button.setEnabled(False)
        self.export_button.setEnabled(False)
        self.frame_ms = 31
        self.is_sec = False
        #加载完成
        self.chkTimer.start(500)

    def cls_result(self):
        self.sign = 'None'
        if self.cap is not None and self.cap.isOpened():
            self.cap.release()
            self.cap = None
        self.timer.stop()
        if self.is_recording:
            self.is_recording = False
            self.rcodTimer.stop()
        QMessageBox.information(self, "提示", "已重置。")
    
    # 无信号图像
    def load_dftIMG(self):
       # 读取或创建 default.jpg
        default_image_path = "./default.jpg"
        if not os.path.exists(default_image_path):
            # 创建一张 500x500 的全黑图像
            black_image = np.zeros((500, 500, 3), dtype=np.uint8)
            font = cv2.FONT_HERSHEY_SIMPLEX
            text = "No Signal"
            text_size = cv2.getTextSize(text, font, 1, 2)[0]
            text_x = (black_image.shape[1] - text_size[0]) // 2
            text_y = (black_image.shape[0] + text_size[1]) // 2
            cv2.putText(black_image, text, (text_x, text_y), font, 1, (255, 255, 255), 1, cv2.LINE_AA)
            cv2.imwrite(default_image_path, black_image)
        
        # 读取图像
        image = cv2.imread(default_image_path)
        if image is not None:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            h, w, ch = image.shape
            bytes_per_line = ch * w
            qt_image = QImage(image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qt_image)
            self.original_image_label.setPixmap(pixmap)
            self.processed_image_label.setPixmap(pixmap)
        else:
            QMessageBox.warning(self, "错误", "启动文件被破坏") 
    # 主动更新布局-中断函数-500ms
    def check(self):
        # 计算帧率
        if self.is_sec:
            self.fps_sta.setText(str(self.fps_num))
            self.fps_num = 0
        self.is_sec = not self.is_sec
        # 检查信号
        if self.sign == 'None':      #0:None     1:Pic       2:MP4       3:Cam
            self.sign_sta.setText("无")
            self.load_dftIMG()
            self.play_button.setEnabled(False)
            self.play_button.setText("-")
            self.export_button.setEnabled(False)
            self.export_button.setText("-")
            self.realtime_button.setText("实时查看")
            self.sign_led.setStyleSheet("background-color: red;")
        elif self.sign == 'Pic':
            self.sign_sta.setText("图片")
            self.sign_led.setStyleSheet("background-color: green;")
            self.export_button.setEnabled(True)
            self.export_button.setText("导出图像")
        elif self.sign == 'MP4':
            self.sign_sta.setText("视频")
            self.sign_led.setStyleSheet("background-color: green;")
            self.realtime_button.setEnabled(True)
            self.play_button.setEnabled(True)
            self.export_button.setEnabled(True)
            if self.play_button.text() == "-":
                self.play_button.setText("播放")
            if self.export_button.text() == "-":
                self.export_button.setText("开始录制")
        elif self.sign == 'Cam':
            self.sign_sta.setText("摄像头")
            self.sign_led.setStyleSheet("background-color: green;")
            self.realtime_button.setEnabled(True)
            self.realtime_button.setText("关闭实时")
            self.export_button.setEnabled(True)    
            self.play_button.setEnabled(True)
            if self.play_button.text() == "-":
                self.play_button.setText("暂停")
            if self.export_button.text() == "-":
                self.export_button.setText("开始录制")
        else:
            self.sign_sta.setText("ERROR")
            self.sign_led.setStyleSheet("background-color: red;")

    # 录制计时-中断函数-1000ms
    def rcod_cnt(self):
        current_time = QTime.fromString(self.recording_sta.text(), 'hh:mm:ss')
        if current_time.isValid():
            current_time = current_time.addSecs(1)
            self.recording_sta.setText(current_time.toString('hh:mm:ss'))
    # 选择源-按钮响应
    def select_source(self):
        # 关闭摄像头
        if self.cap is not None and self.cap.isOpened():
            self.cap.release()
            self.cap = None
            self.timer.stop()
            self.sign = 'None'
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "选择图像或视频", "", "Images/Video Files (*.jpg *.jpeg *.png *.mp4 *.avi);;All Files (*)", options=options)
        if file_path:
            if file_path.endswith(('.mp4', '.avi')):
                self.video_path = file_path
                self.cap = cv2.VideoCapture(file_path)
                self.update_frame()
                self.sign = 'MP4'
            else:
                self.video_path = None
                image = cv2.imread(file_path)
                if image is not None:
                    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    h, w, ch = image.shape
                    bytes_per_line = ch * w
                    qt_image = QImage(image.data, w, h, bytes_per_line, QImage.Format_RGB888)
                    pixmap = QPixmap.fromImage(qt_image)
                    self.original_image_label.setPixmap(pixmap)
                    self.sign = 'Pic'
                    proced_pixmap = self.process_frame(image)
                    self.display_image(proced_pixmap,self.processed_image_label)
                else:
                    QMessageBox.warning(self, "错误", "无法加载图像文件")
    # 实时模式-按钮响应
    def start_realtime(self):
        # 摄像头已打开
        if self.cap is not None and self.cap.isOpened():
            self.cap.release()
            self.cap = None
            self.timer.stop()
            self.sign = 'None'
        # 摄像头已关闭  
        else:
            self.video_path = None
            self.sign = 'Cam'
            self.export_button.setText("开始录制")
            self.cap = cv2.VideoCapture(0)
            self.timer.start(self.frame_ms)
    # 播放-按钮响应
    def play_video(self):
        if self.play_button.text() == "暂停":
            self.timer.stop()
            if self.is_recording:
                self.rcodTimer.stop()
            self.play_button.setText("播放")
            self.export_button.setText("导出图像")
        elif self.play_button.text() == "播放":
            self.timer.start(self.frame_ms)
            if self.is_recording:
                self.rcodTimer.start(1000)
            self.play_button.setText("暂停")
            self.export_button.setText("开始录制")
    # 帧更新-中断函数-30ms
    def update_frame(self):
        self.fps_num += 1
        # 捕获对象已配置
        if self.cap is not None and self.cap.isOpened():
            ret, frame = self.cap.read()
            # 帧处理
            if ret:
                original_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # 原始帧
                self.display_image(original_frame, self.original_image_label)
                processed_frame = self.process_frame(original_frame)
                self.display_image(processed_frame, self.processed_image_label)
                # 录制
                if self.export_button.text() == "结束录制":
                    processed_frame = cv2.cvtColor(processed_frame, cv2.COLOR_RGB2BGR)
                    self.recorder.write(processed_frame)
            # 视频结束
            else:
                self.cap.release()
                self.cap = None
                self.timer.stop()
    # 处理帧->帧更新
    def process_frame(self, frame):
        return frame
    # 显示帧->帧更新
    def display_image(self, image, label):
        h, w, ch = image.shape
        bytes_per_line = ch * w
        qt_image = QImage(image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qt_image)
        label.setPixmap(pixmap)
    # 导出/录制-按钮响应
    def export_result(self):
        # 结束录制
        if self.export_button.text() == "结束录制":
            self.recorder.release()
            self.recorder = None
            self.is_recording = False
            self.recording_sta.setText("未开始")
            self.recording_led.setStyleSheet("background-color: red;")
            self.export_button.setText("开始录制")
            QMessageBox.information(self, "成功", "视频已保存。")
        # 开始录制
        elif self.export_button.text() == "开始录制":
            self.recorder = cv2.VideoWriter('./temp.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 30, (self.processed_image_label.pixmap().width(), self.processed_image_label.pixmap().height()))
            self.is_recording = True
            self.recording_sta.setText("00:00:00")
            self.recording_led.setStyleSheet("background-color: green;")
            self.rcodTimer.start(1000)
            self.export_button.setText("结束录制")
        # 导出图像
        elif self.export_button.text() == "导出图像":
            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getSaveFileName(self, "导出结果", "", "Images (*.jpg *.jpeg *.png);;All Files (*)", options=options)
            if file_path:
                image = self.processed_image_label.pixmap().toImage()
                image.save(file_path)
                QMessageBox.information(self, "成功", "图像已保存。")


if __name__ == '__main__':
    app = QApplication([])
    window = VideoWindow()
    window.show()
    app.exec_()