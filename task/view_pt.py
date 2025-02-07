import torch

# 加载训练后的 .pt 文件
checkpoint = torch.load('./runs/detect/train5/weights/best.pt',weights_only=False)

# 查看文件中包含的键
print(checkpoint.keys())

# 查看模型权重
model_weights = checkpoint['model'].state_dict()
print(model_weights)

# 查看优化器状态
optimizer_state = checkpoint['optimizer']
print(optimizer_state)