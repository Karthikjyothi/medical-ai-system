import os
import uuid
import numpy as np
import torch
from PIL import Image
from torchvision import transforms

from model_registry import get_dataset_model, get_dataset_classes

device = "cuda" if torch.cuda.is_available() else "cpu"

# ==============================
# IMAGE TRANSFORM
# ==============================
transform = transforms.Compose([
    transforms.Grayscale(),
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.5], [0.5])
])

# ==============================
# MC DROPOUT ENABLE
# ==============================
def enable_dropout(m):
    if isinstance(m, torch.nn.Dropout):
        m.train()

# ==============================
# UNCERTAINTY LABEL
# ==============================
def get_uncertainty_level(unc):
    if unc < 0.05:
        return "Low"
    elif unc < 0.15:
        return "Medium"
    else:
        return "High"

# ==============================
# UNIVERSAL PREDICTION ENGINE
# ==============================
def run_prediction(image_path, dataset_name, passes=10):
    model = get_dataset_model(dataset_name)
    class_names = get_dataset_classes(dataset_name)

    if model is None:
        return None

    image = Image.open(image_path)
    image = transform(image).unsqueeze(0).to(device)

    predictions = []

    for _ in range(passes):
        model.eval()
        model.apply(enable_dropout)

        output = model(image)
        probs = torch.softmax(output, dim=1)
        predictions.append(probs.detach().cpu().numpy())

    predictions = np.array(predictions)

    mean_probs = predictions.mean(axis=0)
    std_probs = predictions.std(axis=0)

    predicted_class = np.argmax(mean_probs)
    confidence = float(mean_probs[0][predicted_class])
    uncertainty = float(std_probs[0][predicted_class])

    result = {
        "dataset": dataset_name,
        "predicted_disease": class_names[predicted_class],
        "confidence": round(confidence * 100, 2),
        "uncertainty": round(uncertainty * 100, 4),
        "uncertainty_level": get_uncertainty_level(uncertainty)
    }

    return result