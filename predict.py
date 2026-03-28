import torch
from PIL import Image
import torchvision.transforms as transforms
from torchvision import datasets
import numpy as np
import argparse

from model.cnn import get_model

# =========================
# ARGUMENTS (SELECT DATASET + IMAGE)
# =========================
parser = argparse.ArgumentParser()
parser.add_argument("--data", type=str, default="data/brain_tumor/train")
parser.add_argument("--image", type=str, default="test.jpg")
args = parser.parse_args()

train_path = args.data
image_path = args.image

# Extract dataset name (e.g., brain_tumor)
dataset_name = train_path.split("/")[-2]

# =========================
# DEVICE
# =========================
device = "cuda" if torch.cuda.is_available() else "cpu"

# =========================
# TRANSFORM
# =========================
transform = transforms.Compose([
    transforms.Grayscale(),
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.5], [0.5])
])

# =========================
# LOAD DATASET (AUTO CLASS NAMES)
# =========================
dataset = datasets.ImageFolder(train_path, transform=transform)
class_names = dataset.classes
num_classes = len(class_names)

print("Dataset:", dataset_name)
print("Classes:", class_names)

# =========================
# LOAD MODEL (DATASET-SPECIFIC)
# =========================
model = get_model(num_classes=num_classes)

model_path = f"outputs/models/model_{dataset_name}.pth"

model.load_state_dict(torch.load(model_path, map_location=device))
model.to(device)
model.eval()

# =========================
# MC DROPOUT FUNCTION
# =========================
def mc_predict(image_path, model, transform, passes=10):
    image = Image.open(image_path)
    image = transform(image).unsqueeze(0).to(device)

    model.eval()  # keep base model stable

    predictions = []

    for _ in range(passes):
        # temporarily enable dropout ONLY
        def enable_dropout(m):
            if isinstance(m, torch.nn.Dropout):
                m.train()

        model.apply(enable_dropout)

        output = model(image)
        probs = torch.softmax(output, dim=1)
        predictions.append(probs.detach().cpu().numpy())

    predictions = np.array(predictions)

    mean_probs = predictions.mean(axis=0)
    std_probs = predictions.std(axis=0)

    predicted_class = np.argmax(mean_probs)
    confidence = mean_probs[0][predicted_class]
    uncertainty = std_probs[0][predicted_class]

    return predicted_class, confidence, uncertainty


def get_uncertainty_level(unc):
    if unc < 0.05:
        return "Low"
    elif unc < 0.15:
        return "Medium"
    else:
        return "High"


# =========================
# RUN PREDICTION
# =========================
if __name__ == "__main__":
    cls, conf, unc = mc_predict(image_path, model, transform)

    print("\n🔍 Prediction Result")
    print("----------------------")
    print("Prediction:", class_names[cls])
    print(f"Confidence: {conf*100:.2f}%")

    level = get_uncertainty_level(unc)
    print(f"Uncertainty: {level} ({unc:.4f})")