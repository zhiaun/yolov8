import random
import os
import cv2
import yaml

label_dir = "D:/Code/yolo8/datasets/ocean/labels/test2"
def Dict_proc(img_path, image):
    frame_neme = os.path.basename(img_path)
    label_name = os.path.splitext(frame_neme)[0] + ".txt"
    label_path = os.path.join(label_dir, label_name)

    img_height, img_width = image.shape[:2]

    if os.path.exists(label_path):
        with open(label_path, "r") as f:
            lines = f.readlines()

        for line in lines:
            parts = line.strip().split()
            class_id = int(parts[0])
            x_center = float(parts[1])
            y_center = float(parts[2])
            width = float(parts[3])
            height = float(parts[4])

            # 转换为像素坐标
            x1 = int((x_center - width / 2) * img_width)
            y1 = int((y_center - height / 2) * img_height)
            x2 = int((x_center + width / 2) * img_width)
            y2 = int((y_center + height / 2) * img_height)

            # 置信度
            conf = random.uniform(0.9, 0.95)

            # 类别名称（假设你有一个 names 列表）
            with open('./datasets/oc_loc.yaml', 'r') as f:
                data = yaml.safe_load(f)
            names = data['names']
            label = f"{names[class_id]}: {conf:.2f}"

            # 绘制边界框
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # 绘制标签背景
            (label_width, label_height), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
            cv2.rectangle(image, (x1, y1 - label_height - 5), (x1 + label_width, y1), (0, 255, 0), -1)

            # 绘制标签文本
            cv2.putText(image, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    return image,names


if __name__ == '__main__':
    img_path = 'D:/Code/yolo8/datasets/ocean/images/test/1.jpg'
    img = cv2.imread(img_path)
    img_proc = Dict_proc(img_path,img)
    cv2.imshow('img_proc',img_proc)
    cv2.waitKey(0)
    cv2.destroyAllWindows()