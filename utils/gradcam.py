import torch
import cv2
import numpy as np
from PIL import Image
from torchvision import transforms
from pytorch_grad_cam import GradCAM
from pytorch_grad_cam.utils.image import show_cam_on_image
from model.cnn import get_model

device = "cuda" if torch.cuda.is_available() else "cpu"

def generate_gradcam(image_path):
    model = get_model(num_classes=4)
    model.load_state_dict(torch.load("outputs/models/model.pth", map_location=device))
    model.to(device)
    model.eval()

    target_layer = model.layer4[-1]

    transform = transforms.Compose([
        transforms.Grayscale(),
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
    ])

    image = Image.open(image_path).convert('L')
    input_tensor = transform(image).unsqueeze(0).to(device)

    cam = GradCAM(model=model, target_layers=[target_layer])

    grayscale_cam = cam(input_tensor=input_tensor)[0]

    image_np = np.array(image.resize((224, 224))) / 255.0
    image_np = np.stack([image_np]*3, axis=-1)

    visualization = show_cam_on_image(image_np, grayscale_cam, use_rgb=True)

    return visualization