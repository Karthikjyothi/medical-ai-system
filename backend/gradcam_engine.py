import os
import uuid
import cv2
import torch
import numpy as np
from PIL import Image
from torchvision import transforms
from pytorch_grad_cam import GradCAM
from pytorch_grad_cam.utils.image import show_cam_on_image

from model_registry import get_dataset_model

device = "cuda" if torch.cuda.is_available() else "cpu"

# ==============================
# IMAGE TRANSFORM
# ==============================
transform = transforms.Compose([
    transforms.Grayscale(),
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

# ==============================
# GENERATE DYNAMIC GRADCAM
# ==============================
def generate_gradcam(image_path, dataset_name):
    model = get_dataset_model(dataset_name)

    if model is None:
        return None

    target_layer = model.layer4[-1]

    image = Image.open(image_path).convert("L")
    input_tensor = transform(image).unsqueeze(0).to(device)

    cam = GradCAM(model=model, target_layers=[target_layer])
    grayscale_cam = cam(input_tensor=input_tensor)[0]

    image_np = np.array(image.resize((224, 224))) / 255.0
    image_np = np.stack([image_np] * 3, axis=-1)

    visualization = show_cam_on_image(image_np, grayscale_cam, use_rgb=True)

    os.makedirs("uploads/gradcam", exist_ok=True)

    gradcam_filename = f"{uuid.uuid4().hex}.jpg"
    gradcam_path = os.path.join("uploads/gradcam", gradcam_filename)

    cv2.imwrite(gradcam_path, cv2.cvtColor(visualization, cv2.COLOR_RGB2BGR))

    return gradcam_path