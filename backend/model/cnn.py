import torch.nn as nn
from torchvision.models import resnet18, ResNet18_Weights

def get_model(num_classes=4):
    model = resnet18(weights=ResNet18_Weights.DEFAULT)

    # =========================
    # MODIFY FIRST LAYER (GRAYSCALE)
    # =========================
    model.conv1 = nn.Conv2d(1, 64, kernel_size=7, stride=2, padding=3, bias=False)

    # =========================
    # FREEZE ALL LAYERS (IMPORTANT FOR SPEED)
    # =========================
    # Freeze all layers first
    # Freeze early layers
    for param in model.parameters():
        param.requires_grad = False

    # Unfreeze last block (IMPORTANT)
    for param in model.layer4.parameters():
        param.requires_grad = True

    # Final layer always trainable
    for param in model.fc.parameters():
        param.requires_grad = True

    # 🔥 Unfreeze last conv block (IMPORTANT for Grad-CAM)
    for param in model.layer4.parameters():
        param.requires_grad = True

    # =========================
    # REPLACE FINAL LAYER
    # =========================
    model.fc = nn.Linear(model.fc.in_features, num_classes)

    return model