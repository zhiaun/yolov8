from ultralytics import YOLO

# Load a model
model = YOLO("./ultralytics/models/v8/yolov8n.yaml")  # yolov8经典模型
#model = YOLO("yolov8n.pt")  # load a pretrained model (recommended for training)

# Use the model
results = model.train(data="./datasets/RFT.yaml", epochs=1,imgsz=640,device='cpu')  # train the model