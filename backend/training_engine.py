from datetime import time
import os
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets
from torch.utils.data import DataLoader
import torchvision.transforms as transforms
from sklearn.metrics import classification_report
import shutil

from ssl_engine import UniversalSSLEngine
from model.cnn import get_model
from gan_engine import UniversalGANEngine
from model_registry import load_all_models
from ssl_engine import UniversalSSLEngine


device = "cuda" if torch.cuda.is_available() else "cpu"

class UniversalTrainingEngine:

    def __init__(self, gan_epochs=5, ssl_epochs=3, cnn_epochs=8):
        self.gan_epochs = gan_epochs
        self.ssl_epochs = ssl_epochs
        self.cnn_epochs = cnn_epochs

        self.transform = transforms.Compose([
            transforms.Grayscale(),
            transforms.Resize((224, 224)),
            transforms.RandomHorizontalFlip(),
            transforms.ToTensor(),
            transforms.Normalize([0.5], [0.5])
        ])

    # =====================================
    # MERGE REAL + SYNTHETIC IMAGES
    # =====================================
    def build_augmented_training_data(self, dataset_name):
        real_train_root = f"../data/{dataset_name}/train"
        synthetic_root = f"../outputs/generated_images/{dataset_name}"
        import time
        augmented_root = f"../outputs/augmented_train/{dataset_name}_{int(time.time())}"

        os.makedirs(augmented_root, exist_ok=True)

        # copy real images first
        for cls in os.listdir(real_train_root):
            src_cls = os.path.join(real_train_root, cls)
            dst_cls = os.path.join(augmented_root, cls)

            shutil.copytree(src_cls, dst_cls)

        # merge synthetic images
        if os.path.exists(synthetic_root):
            for cls in os.listdir(synthetic_root):
                syn_cls = os.path.join(synthetic_root, cls)
                dst_cls = os.path.join(augmented_root, cls)

                if os.path.exists(dst_cls):
                    for img in os.listdir(syn_cls):
                        shutil.copy(
                            os.path.join(syn_cls, img),
                            os.path.join(dst_cls, f"syn_{img}")
                        )

        return augmented_root


    # =====================================
    # COMPLETE TRAINING PIPELINE
    # =====================================
    def train_dataset(self, dataset_name):
        train_path = f"../data/{dataset_name}/train"
        val_path = f"../data/{dataset_name}/val"
        test_path = f"../data/{dataset_name}/test"
        def update_status(msg):
            from main import training_status
            training_status[dataset_name] = msg

        if not os.path.exists(train_path):
            return {"status": "failed", "message": "Dataset not found"}

        # STEP 1 — GAN TRAINING
        gan = UniversalGANEngine(
            epochs=self.gan_epochs,
            status_callback=update_status
        )
        gan.train_generators(train_path)
        gan.generate_synthetic_images(dataset_name)
        augmented_train_path = self.build_augmented_training_data(dataset_name)
        ssl_engine = UniversalSSLEngine(epochs=self.ssl_epochs)
        ssl_pretrained_path = ssl_engine.pretrain_encoder(augmented_train_path, dataset_name)

        # STEP 2 — CNN DATA LOAD
        train_data = datasets.ImageFolder(augmented_train_path, transform=self.transform)
        val_data = datasets.ImageFolder(val_path, transform=self.transform)

        train_loader = DataLoader(train_data, batch_size=16, shuffle=True)
        val_loader = DataLoader(val_data, batch_size=16, shuffle=False)

        class_names = train_data.classes
        num_classes = len(class_names)

        # STEP 3 — CNN MODEL
        model = get_model(num_classes=num_classes)
        model.load_state_dict(torch.load(ssl_pretrained_path, map_location=device), strict=False)
        model.to(device)

        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(model.parameters(), lr=0.0001)

        print(f"🚀 Starting CNN training for {dataset_name}")

        for epoch in range(self.cnn_epochs):
            model.train()

            for images, labels in train_loader:
                images, labels = images.to(device), labels.to(device)

                outputs = model(images)
                loss = criterion(outputs, labels)

                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

            print(f"{dataset_name} CNN Epoch [{epoch+1}/{self.cnn_epochs}]")

        # STEP 4 — SAVE TRAINED MODEL
        os.makedirs("../models", exist_ok=True)
        save_path = f"../models/model_{dataset_name}.pth"
        torch.save(model.state_dict(), save_path)

        # STEP 5 — OPTIONAL TEST EVALUATION
        if os.path.exists(test_path):
            test_data = datasets.ImageFolder(test_path, transform=self.transform)
            test_loader = DataLoader(test_data, batch_size=16, shuffle=False)

            model.eval()
            all_preds = []
            all_labels = []

            with torch.no_grad():
                for images, labels in test_loader:
                    images, labels = images.to(device), labels.to(device)

                    outputs = model(images)
                    _, predicted = torch.max(outputs, 1)

                    all_preds.extend(predicted.cpu().numpy())
                    all_labels.extend(labels.cpu().numpy())

            report = classification_report(all_labels, all_preds, target_names=class_names)
            print(report)

        # STEP 6 — RELOAD MODEL REGISTRY
        load_all_models()

        return {
            "status": "success",
            "message": f"{dataset_name} trained and deployed successfully"
        }