import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets
from torch.utils.data import DataLoader
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
import os
import argparse

from model.cnn import get_model

# =========================
# ARGUMENTS (MULTI-DATASET)
# =========================
parser = argparse.ArgumentParser()
parser.add_argument("--data", type=str, default="data/brain_tumor/train")
args = parser.parse_args()

train_path = args.data
val_path = train_path.replace("train", "val")
test_path = train_path.replace("train", "test")

# =========================
# DEVICE
# =========================
device = "cuda" if torch.cuda.is_available() else "cpu"

# =========================
# TRANSFORMS
# =========================
transform = transforms.Compose([
    transforms.Grayscale(),
    transforms.Resize((224, 224)),
    transforms.RandomHorizontalFlip(),
    #transforms.RandomRotation(10),
    transforms.ToTensor(),
    transforms.Normalize([0.5], [0.5])
])

# =========================
# DATASETS
# =========================
train_data = datasets.ImageFolder(train_path, transform=transform)
val_data = datasets.ImageFolder(val_path, transform=transform)

#train_loader = DataLoader(train_data, batch_size=16, shuffle=True)
#val_loader = DataLoader(val_data, batch_size=16, shuffle=False)
train_loader = DataLoader(train_data, batch_size=16, shuffle=True, num_workers=0)
val_loader = DataLoader(val_data, batch_size=16, shuffle=False, num_workers=0)

class_names = train_data.classes
num_classes = len(class_names)

print("Dataset Path:", train_path)
print("Classes:", class_names)

# =========================
# MODEL
# =========================
model = get_model(num_classes=num_classes)
model.to(device)

# =========================
# LOSS + OPTIMIZER
# =========================
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.0001)

epochs = 10

# =========================
# TRACKING
# =========================
train_losses = []
val_losses = []
train_accs = []
val_accs = []

# =========================
# TRAINING LOOP
# =========================
for epoch in range(epochs):
    model.train()
    running_loss = 0

    correct = 0
    total = 0

    for i, (images, labels) in enumerate(train_loader):
        if i % 20 == 0:
            print(f"Processing batch {i}/{len(train_loader)}")

        images, labels = images.to(device), labels.to(device)

        outputs = model(images)
        loss = criterion(outputs, labels)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        running_loss += loss.item()

        _, predicted = torch.max(outputs, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

    train_acc = correct / total
    train_loss = running_loss / len(train_loader)

    train_accs.append(train_acc)
    train_losses.append(train_loss)

    # =========================
    # VALIDATION
    # =========================
    model.eval()
    correct = 0
    total = 0
    val_loss = 0

    with torch.no_grad():
        for images, labels in val_loader:
            images, labels = images.to(device), labels.to(device)

            outputs = model(images)
            loss_v = criterion(outputs, labels)

            val_loss += loss_v.item()

            _, predicted = torch.max(outputs, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

    val_acc = correct / total
    val_loss = val_loss / len(val_loader)

    val_accs.append(val_acc)
    val_losses.append(val_loss)

    print(f"Epoch [{epoch+1}/{epochs}] "
          f"Train Loss: {train_loss:.4f}, Train Acc: {train_acc:.4f} | "
          f"Val Loss: {val_loss:.4f}, Val Acc: {val_acc:.4f}")

# =========================
# TEST EVALUATION (ONCE)
# =========================
if os.path.exists(test_path):
    test_data = datasets.ImageFolder(test_path, transform=transform)
    test_loader = DataLoader(test_data, batch_size=16, shuffle=False)

    model.eval()
    correct = 0
    total = 0

    with torch.no_grad():
        for images, labels in test_loader:
            images, labels = images.to(device), labels.to(device)

            outputs = model(images)
            _, predicted = torch.max(outputs, 1)

            total += labels.size(0)
            correct += (predicted == labels).sum().item()

    test_acc = correct / total
    print(f"🧪 Final Test Accuracy: {test_acc:.4f}")

# =========================
# CONFUSION MATRIX + CLASSIFICATION REPORT (ONCE)
# =========================
from sklearn.metrics import confusion_matrix, classification_report
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

if os.path.exists(test_path):
    print("\n📊 Generating Evaluation Metrics...")

    all_preds = []
    all_labels = []

    model.eval()

    with torch.no_grad():
        for images, labels in test_loader:
            images, labels = images.to(device), labels.to(device)

            outputs = model(images)
            _, predicted = torch.max(outputs, 1)

            all_preds.extend(predicted.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())

    # Confusion Matrix
    cm = confusion_matrix(all_labels, all_preds)

    plt.figure(figsize=(6,5))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
                xticklabels=class_names,
                yticklabels=class_names)
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.title("Confusion Matrix")
    plt.savefig("outputs/confusion_matrix.png")
    plt.close()

    # Classification Report
    report = classification_report(all_labels, all_preds, target_names=class_names)
    print("\n📊 Classification Report:\n")
    print(report)

    # Save report to file
    with open("outputs/classification_report.txt", "w") as f:
        f.write(report)

# =========================
# SAVE MODEL (DATASET-SPECIFIC)
# =========================
os.makedirs("outputs/models", exist_ok=True)

dataset_name = train_path.split("/")[-2]  # e.g. brain_tumor
save_path = f"outputs/models/model_{dataset_name}.pth"

torch.save(model.state_dict(), save_path)

print(f"✅ Model saved at {save_path}")

# =========================
# SAVE GRAPHS
# =========================
os.makedirs("outputs", exist_ok=True)

plt.figure()
plt.plot(train_accs, label="Train Accuracy")
plt.plot(val_accs, label="Validation Accuracy")
plt.legend()
plt.title("Accuracy Graph")
plt.savefig("outputs/accuracy.png")

plt.figure()
plt.plot(train_losses, label="Train Loss")
plt.plot(val_losses, label="Validation Loss")
plt.legend()
plt.title("Loss Graph")
plt.savefig("outputs/loss.png")

print("📊 Graphs saved in outputs/")