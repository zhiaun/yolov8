# 作用      将VOC格式的标注文件转换为YOLOv8格式的标注文件
# 用法      改变voc_dir和yolo_dir为VOC和YOLOv8的目录
# 用法      改变class_names为VOC的类别名称列表,注意类别名称的顺序与YOLOv8的类别顺序一致
# 用法      该脚本在labels和xmls文件夹同级目录下
import os
import xml.etree.ElementTree as ET

def convert_voc_to_yolo(voc_dir, yolo_dir):
    # 确保输出目录存在
    if not os.path.exists(yolo_dir):
        os.makedirs(yolo_dir)
    print(f"Converting VOC to YOLOv8 format in {voc_dir}")
    # 遍历VOC目录下的所有文件
    for root, dirs, files in os.walk(voc_dir):
        print(f"Processing {root}")
        for file in files:
            if file.endswith('.xml'):

                xml_file_path = os.path.join(root, file)
                txt_file_path = os.path.join(yolo_dir, file.replace('.xml', '.txt'))
                
                try:
                    # 解析XML文件
                    tree = ET.parse(xml_file_path)
                    root_element = tree.getroot()

                    # 获取图像尺寸
                    size = root_element.find('size')
                    width = int(size.find('width').text)
                    height = int(size.find('height').text)

                    # 查找所有的object标签
                    objects = root_element.findall('object')
                    with open(txt_file_path, 'w') as txt_file:
                        for obj in objects:
                            # 获取类别名称
                            class_name = obj.find('name').text
                            class_id = class_names.index(class_name)  # 假设class_names是一个已知的类别列表

                            # 获取边界框坐标
                            bbox = obj.find('bndbox')
                            xmin = float(bbox.find('xmin').text)
                            ymin = float(bbox.find('ymin').text)
                            xmax = float(bbox.find('xmax').text)
                            ymax = float(bbox.find('ymax').text)

                            # 计算中心点和宽高
                            x_center = (xmin + xmax) / 2.0 / width
                            y_center = (ymin + ymax) / 2.0 / height
                            bbox_width = (xmax - xmin) / width
                            bbox_height = (ymax - ymin) / height

                            # 写入YOLOv8格式的标注
                            txt_file.write(f"{class_id} {x_center} {y_center} {bbox_width} {bbox_height}\n")
                except Exception as e:
                    print(f"When deal {xml_file_path} ERROR: {e}")
    print("Conversion completed.")



if __name__ == "__main__":
    # 定义类别列表，顺序必须与YOLOv8的类别顺序一致
    class_names = ['bottle', 'grass', 'branch','milk-box',
                'plastic-bag','plastic-garbage','ball','leaf']  # 请根据实际情况修改

    # 输入和输出目录
    voc_dir = './Annot'
    yolo_dir = './labels'

    # 转换标注文件
    convert_voc_to_yolo(voc_dir, yolo_dir)