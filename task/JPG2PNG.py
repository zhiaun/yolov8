import os
from PIL import Image

def convert_to_png(folder):
  for file in os.listdir(folder):
      if file.endswith(".jpg"):
          full_path = os.path.join(folder, file)
          img = Image.open(full_path)
          new_path = full_path.replace(".jpg", ".png")
          img.save(new_path, "PNG")
          print(f"转换完成: {new_path}")

def convert_to_jpg(folder):
  for file in os.listdir(folder):
      if file.endswith(".png"):
          full_path = os.path.join(folder, file)
          img = Image.open(full_path)

          # 转换为 RGB 模式（避免透明通道问题）
          if img.mode in ("RGBA", "P"):
              img = img.convert("RGB")

          # 构建新的 .jpg 文件路径
          new_path = full_path.replace(".png", ".jpg")
          
          # 保存为 JPG 格式
          img.save(new_path, "JPEG", quality=95)
          print(f"已转换为 JPG: {new_path}")



if __name__ == "__main__":
  folder = "./datasets/ocean/images/test2"
  convert_to_jpg(folder)