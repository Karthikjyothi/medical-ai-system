import os
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

from model.cnn import get_model

device = "cuda" if torch.cuda.is_available() else "cpu"

class UniversalSSLEngine:

    def __init__(self, epochs=3):
        self.epochs = epochs

        self.transform_ssl = transforms.Compose([
            transforms.Grayscale(),
            transforms.Resize((224, 224)),
            transforms.RandomHorizontalFlip(),
            transforms.RandomRotation(10),
            transforms.ToTensor(),
            transforms.Normalize([0.5], [0.5])
        ])

    # ==========================================
    # SSL FEATURE PRETRAINING
    # ==========================================
    def pretrain_encoder(self, augmented_train_path, dataset_name):

        dataset = datasets.ImageFolder(
            augmented_train_path,
            transform=self.transform_ssl
        )

        # SMALL SUBSET FOR FAST SSL
        subset_size = min(300, len(dataset))
        subset_indices = list(range(subset_size))

        subset = torch.utils.data.Subset(dataset, subset_indices)

        loader = DataLoader(
            subset,
            batch_size=8,
            shuffle=True,
            num_workers=0
        )

        num_classes = len(dataset.classes)

        model = get_model(num_classes=num_classes)

        # FREEZE MOST LAYERS FOR FAST PRETRAINING
        for param in model.parameters():
            param.requires_grad = False

        # only final layer trains
        for param in model.fc.parameters():
            param.requires_grad = True

        model.to(device)

        optimizer = optim.Adam(model.fc.parameters(), lr=0.0005)

        print(f"🚀 Starting FAST SSL pretraining for {dataset_name}")

        for epoch in range(1):  # ONLY 1 FAST EPOCH
            model.train()

            for batch_idx, (images, _) in enumerate(loader):

                images = images.to(device)

                outputs = model(images)

                pseudo_loss = torch.mean(outputs ** 2)

                optimizer.zero_grad()
                pseudo_loss.backward()
                optimizer.step()

                if batch_idx % 10 == 0:
                    print(
                        f"{dataset_name} SSL Batch "
                        f"[{batch_idx}/{len(loader)}] "
                        f"Loss: {pseudo_loss.item():.4f}"
                    )

            print(f"✅ {dataset_name} FAST SSL Epoch Complete")

        os.makedirs("../models/ssl_pretrained", exist_ok=True)

        ssl_path = f"../models/ssl_pretrained/ssl_{dataset_name}.pth"

        torch.save(model.state_dict(), ssl_path)

        print(f"✅ SSL pretrained encoder saved: {ssl_path}")

        return ssl_path