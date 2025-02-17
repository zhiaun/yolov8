import cv2
import os
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QPushButton, QFileDialog, QMessageBox,QGridLayout
from PyQt5.QtCore import QTimer,Qt
from PyQt5.QtGui import QImage, QPixmap

class VideoWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("河道污染物识别")
        self.setGeometry(100, 100, 1200, 600)  # 调整窗口大小以容纳新的布局
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
        self.sign_led.setStyleSheet("background-color: red;")
        self.topG_layout.addWidget(self.sign_led,0,0)

        self.sign_lab = QLabel("信号源:", self)
        self.sign_lab.setFixedSize(50, 20)
        self.topG_layout.addWidget(self.sign_lab,0,1)

        self.sign_sta = QLabel("无", self)
        self.sign_sta.setFixedSize(200, 20)
        self.topG_layout.addWidget(self.sign_sta,0,2) 

        self.meth_led = QLabel(self)
        self.meth_led.setFixedSize(12, 12)
        self.meth_led.setStyleSheet("background-color: red;")
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

        self.play_button = QPushButton("播放", self)
        self.play_button.clicked.connect(self.play_video)
        self.bottom_layout.addWidget(self.play_button)

        self.export_button = QPushButton("-", self)
        self.export_button.clicked.connect(self.export_result)
        self.bottom_layout.addWidget(self.export_button)

        self.cap = None
        self.video_path = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        #self.timer.start(30)  # 30 ms interval

        self.text_x = 416  # Initial x position of the text
        self.text_y = 50   # y position of the text

        self.is_realtime = False
        self.is_recording = False
        self.play_button.setEnabled(False)
        self.export_button.setEnabled(False)

        #加载完成

    def select_source(self):
        if self.cap is not None and self.cap.isOpened():
            self.cap.release()
            self.cap = None
            self.timer.stop()
            self.original_image_label.clear()  # 清除原始图像窗口内容
            self.processed_image_label.clear()  # 清除处理后图像窗口内容

        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "选择图像或视频", "", "Images/Video Files (*.jpg *.jpeg *.png *.mp4 *.avi);;All Files (*)", options=options)
        if file_path:
            if file_path.endswith(('.mp4', '.avi')):
                self.video_path = file_path
                self.cap = cv2.VideoCapture(file_path)
                self.update_frame()
                self.play_button.setEnabled(True)
                self.export_button.setEnabled(True)
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
                    self.process_frame(image)
                    self.export_button.setEnabled(True)
                else:
                    QMessageBox.warning(self, "错误", "无法加载图像文件")
        self.is_realtime = False
        self.realtime_button.setEnabled(True)
        self.play_button.setEnabled(False)

    def start_realtime(self):
        if self.cap is not None and self.cap.isOpened():# 摄像头就绪
            # 关闭摄像头
            self.cap.release()
            self.cap = None
            self.is_realtime = False
            self.timer.stop()
                # 修改文本
            self.original_image_label.clear()  # 清除原始图像窗口内容
            self.processed_image_label.clear()  # 清除处理后图像窗口内容
            self.play_button.setEnabled(False)
            self.export_button.setEnabled(False)
            self.realtime_button.setText("实时查看")
            self.sign_led.setStyleSheet("background-color: red;")
            self.sign_sta.text = "无"            
        else:
            # 打开摄像头
            self.video_path = None
            self.cap = cv2.VideoCapture(0)
            self.is_realtime = True
            self.timer.start(30)
                # 修改文本
            self.realtime_button.setEnabled(True)
            self.realtime_button.setText("关闭实时")
            self.play_button.setEnabled(True)
            self.play_button.setText("暂停")
            self.export_button.setEnabled(True)
            self.export_button.setText("开始录制")
            self.sign_led.setStyleSheet("background-color: green;")
            self.sign_sta.text = "实时模式"

    def play_video(self):
        if self.is_realtime and self.play_button.text() == "暂停":
            self.timer.stop()
            self.play_button.setText("播放")
        elif self.is_realtime and self.play_button.text() == "播放":
            self.timer.start(30)
            self.play_button.setText("暂停")
        
        if self.video_path:
            self.cap = cv2.VideoCapture(self.video_path)
            self.update_frame()
            self.timer.start(30)

    def update_frame(self):
        # 实时模式更新帧
        if self.is_realtime:
            if self.cap is not None and self.cap.isOpened():
                ret, frame = self.cap.read()
                # 处理帧,出错自动关闭
                if ret:
                    original_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # 原始帧
                    self.display_image(original_frame, self.original_image_label)
                    processed_frame = self.process_frame(original_frame)
                    self.display_image(processed_frame, self.processed_image_label)
                    # 录制
                    if self.is_recording:
                        processed_frame = cv2.cvtColor(processed_frame, cv2.COLOR_RGB2BGR)
                        self.recorder.write(processed_frame)
                else:
                    self.cap.release()
                    self.cap = None
                    self.timer.stop()
        # 视频流更新帧
        else:
            original_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # 原始帧
            self.display_image(original_frame, self.original_image_label)
            processed_frame = self.process_frame(original_frame)
            self.display_image(processed_frame, self.processed_image_label)

    def process_frame(self, frame):
        return frame

    def display_image(self, image, label):
        h, w, ch = image.shape
        bytes_per_line = ch * w
        qt_image = QImage(image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qt_image)
        label.setPixmap(pixmap)

    def export_result(self):
        # 结束录制
        if self.is_recording:
            self.recorder.release()
            self.recorder = None
            self.is_recording = False
            self.export_button.setText("开始录制")
        # 开始录制
        else:
            self.recorder = cv2.VideoWriter('./temp.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 30, (self.processed_image_label.pixmap().width(), self.processed_image_label.pixmap().height()))
            self.is_recording = True
            self.export_button.setText("停止录制")
        if self.processed_image_label.pixmap() is not None and self.export_button.text() == "导出图像":
            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getSaveFileName(self, "导出结果", "", "Images (*.jpg *.jpeg *.png);;All Files (*)", options=options)
            if file_path:
                image = self.processed_image_label.pixmap().toImage()
                image.save(file_path)

    # def closeEvent(self, event):
    #     if self.cap is not None:
    #         self.cap.release()
    #     event.accept()

if __name__ == '__main__':
    app = QApplication([])
    window = VideoWindow()
    window.show()
    app.exec_()