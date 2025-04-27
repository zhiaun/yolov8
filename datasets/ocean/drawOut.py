# 绘制带标注框的图片

import os
import cv2
import numpy as np

# 定义类别名称映射
CLASSES = {
    '0': 'Plant',
    '1': 'Other',
    '2': 'Plastic'
}

def draw_bounding_boxes(image_path, label_path, output_path):
    # 读取图片
    image = cv2.imread(image_path)
    if image is None:
        print(f"无法读取图片: {image_path}")
        return

    # 读取标注文件
    with open(label_path, 'r') as file:
        lines = file.readlines()

    # 遍历每一行标注
    for line in lines:
        parts = line.strip().split()
        if len(parts) < 5:
            continue

        class_id = parts[0]
        x_center, y_center, width, height = map(float, parts[1:5])

        # 将YOLO格式的坐标转换为像素坐标
        h, w = image.shape[:2]
        x_min = int((x_center - width / 2) * w)
        y_min = int((y_center - height / 2) * h)
        x_max = int((x_center + width / 2) * w)
        y_max = int((y_center + height / 2) * h)

        # 绘制边界框
        cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

        # 绘制类别名
        class_name = CLASSES.get(class_id, 'Unknown')
        cv2.putText(image, class_name, (x_min, y_min - 5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 0), 1)

    # 保存处理后的图片
    cv2.imwrite(output_path, image)

def process_labels():
    label_dir = './re_labels/valid'
    img_dir = './re_images/valid'
    output_dir = './output/valid'

    # 创建输出目录（如果不存在）
    os.makedirs(output_dir, exist_ok=True)

    txt_files = [f for f in os.listdir(label_dir) if f.endswith('.txt')]

    for txt_file in txt_files:
        txt_path = os.path.join(label_dir, txt_file)
        img_name = os.path.splitext(txt_file)[0] + '.jpg'  # 假设图片格式为.jpg
        img_path = os.path.join(img_dir, img_name)
        output_path = os.path.join(output_dir, f"prced_{img_name}")

        if os.path.exists(img_path):
            draw_bounding_boxes(img_path, txt_path, output_path)
            print(f"已处理图片: {img_name}")
        else:
            print(f"未找到对应图片: {img_name}")

if __name__ == "__main__":
    process_labels()