import os
import torch
from torchvision import datasets, transforms

from model.cnn import get_model

# ==============================
# PATH CONFIG
# ==============================
DATA_ROOT = "../data"
MODEL_ROOT = "../models"

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
# GLOBAL REGISTRY STORAGE
# ==============================
MODEL_REGISTRY = {}
CLASS_REGISTRY = {}

# ==============================
# AUTO DISCOVER AVAILABLE DATASETS
# ==============================
def discover_datasets():
    datasets_found = []

    if not os.path.exists(DATA_ROOT):
        return datasets_found

    for folder in os.listdir(DATA_ROOT):
        dataset_path = os.path.join(DATA_ROOT, folder)

        if os.path.isdir(dataset_path):
            train_path = os.path.join(dataset_path, "train")

            if os.path.exists(train_path):
                datasets_found.append(folder)

    return datasets_found


# ==============================
# LOAD ALL TRAINED MODELS AUTOMATICALLY
# ==============================
def load_all_models():
    available_datasets = discover_datasets()

    for dataset_name in available_datasets:
        model_path = os.path.join(MODEL_ROOT, f"model_{dataset_name}.pth")
        train_path = os.path.join(DATA_ROOT, dataset_name, "train")

        if os.path.exists(model_path):

            dataset = datasets.ImageFolder(train_path, transform=transform)
            class_names = dataset.classes
            num_classes = len(class_names)

            model = get_model(num_classes=num_classes)
            model.load_state_dict(torch.load(model_path, map_location=device))
            model.to(device)
            model.eval()

            MODEL_REGISTRY[dataset_name] = model
            CLASS_REGISTRY[dataset_name] = class_names

            print(f"✅ Loaded dataset model: {dataset_name}")


# ==============================
# GET MODEL
# ==============================
def get_dataset_model(dataset_name):
    return MODEL_REGISTRY.get(dataset_name, None)


# ==============================
# GET CLASS NAMES
# ==============================
def get_dataset_classes(dataset_name):
    return CLASS_REGISTRY.get(dataset_name, [])


# ==============================
# GET AVAILABLE DATASETS FOR FRONTEND
# ==============================
def get_available_datasets():
    return list(MODEL_REGISTRY.keys())