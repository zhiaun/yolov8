from ultralytics import YOLO
import cv2
#import numpy as np

# 加载训练好的模型
#model = YOLO('./yolov8n.pt')
model = YOLO('./runs/detect/train/weights/best.pt')

# 进行单张图像推理
image_path = './task/bus.jpg'
results = model.predict(source=image_path)

# 读取原始图像
image = cv2.imread(image_path)

# 处理推理结果
for result in results:
    boxes = result.boxes  # 获取边界框信息
    if boxes is not None:
        for box in boxes:
            # 获取边界框坐标
            xyxy = box.xyxy[0].cpu().numpy().astype(int)
            x1, y1, x2, y2 = xyxy

            # 获取类别索引和置信度
            cls = int(box.cls[0])
            conf = float(box.conf[0])

            # 绘制边界框
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # 准备标签文本
            label = f'{cls}: {conf:.2f}'

            # 绘制标签背景
            (label_width, label_height), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
            cv2.rectangle(image, (x1, y1 - label_height - 5), (x1 + label_width, y1), (0, 255, 0), -1)

            # 绘制标签文本
            cv2.putText(image, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

# 显示带有检测结果的图像
cv2.imshow('YOLOv8 Inference', image)
cv2.waitKey(0)
cv2.destroyAllWindows()