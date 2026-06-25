import os
import torch
import torchvision
import torchvision.transforms as transforms
from torch.utils.data import DataLoader, Subset
import torchvision.utils as vutils
import torch.nn as nn
import torch.optim as optim

from model.gan import Generator, Discriminator

device = "cuda" if torch.cuda.is_available() else "cpu"

class UniversalGANEngine:

    def __init__(self, image_size=64, z_dim=100, epochs=5, status_callback=None):
        self.image_size = image_size
        self.z_dim = z_dim
        self.epochs = epochs
        self.status_callback = status_callback

        self.transform = transforms.Compose([
            transforms.Grayscale(),
            transforms.Resize((image_size, image_size)),
            transforms.ToTensor(),
            transforms.Normalize([0.5], [0.5])
        ])

    # =====================================
    # TRAIN GAN ON ANY DATASET
    # =====================================
    def train_generators(self, dataset_train_path):
        dataset = torchvision.datasets.ImageFolder(dataset_train_path, transform=self.transform)
        classes = dataset.classes

        os.makedirs("../models/generators", exist_ok=True)

        print("🚀 Starting Universal GAN training...")

        for cls in classes:
            print(f"🔥 Training GAN for class: {cls}")
            if self.status_callback:
                self.status_callback(f"GAN training started for class {cls}")

            class_idx = dataset.class_to_idx[cls]
            indices = [i for i, (_, label) in enumerate(dataset.samples) if label == class_idx]
            subset = Subset(dataset, indices)

            loader = DataLoader(subset, batch_size=32, shuffle=True)

            gen = Generator(self.z_dim).to(device)
            disc = Discriminator().to(device)

            opt_gen = optim.Adam(gen.parameters(), lr=0.0002, betas=(0.5, 0.999))
            opt_disc = optim.Adam(disc.parameters(), lr=0.0002, betas=(0.5, 0.999))
            criterion = nn.BCELoss()

            for epoch in range(self.epochs):
                for real, _ in loader:
                    real = real.to(device)

                    noise = torch.randn(real.shape[0], self.z_dim, 1, 1).to(device)
                    fake = gen(noise)

                    # discriminator
                    disc_real = disc(real).reshape(-1)
                    loss_real = criterion(disc_real, torch.ones_like(disc_real))

                    disc_fake = disc(fake.detach()).reshape(-1)
                    loss_fake = criterion(disc_fake, torch.zeros_like(disc_fake))

                    loss_disc = (loss_real + loss_fake) / 2

                    disc.zero_grad()
                    loss_disc.backward()
                    opt_disc.step()

                    # generator
                    output = disc(fake).reshape(-1)
                    loss_gen = criterion(output, torch.ones_like(output))

                    gen.zero_grad()
                    loss_gen.backward()
                    opt_gen.step()

                print(f"{cls} Epoch [{epoch+1}/{self.epochs}]")
                if self.status_callback:
                    self.status_callback(f"GAN {cls} Epoch {epoch+1}/{self.epochs}")

            torch.save(gen.state_dict(), f"../models/generators/generator_{cls}.pth")

        print("✅ All GAN generators trained.")
        if self.status_callback:
            self.status_callback("GAN training complete. Generating synthetic images...")

    # =====================================
    # GENERATE SYNTHETIC IMAGES
    # =====================================
    def generate_synthetic_images(self, dataset_name, num_images=20):
        generator_root = "../models/generators"
        output_root = f"../outputs/generated_images/{dataset_name}"

        os.makedirs(output_root, exist_ok=True)

        for file in os.listdir(generator_root):
            if file.startswith("generator_"):
                cls = file.replace("generator_", "").replace(".pth", "")

                gen = Generator(self.z_dim).to(device)
                gen.load_state_dict(torch.load(os.path.join(generator_root, file), map_location=device))
                gen.eval()

                class_dir = os.path.join(output_root, cls)
                os.makedirs(class_dir, exist_ok=True)

                for i in range(num_images):
                    noise = torch.randn(1, self.z_dim, 1, 1).to(device)
                    fake = gen(noise)

                    vutils.save_image(fake, f"{class_dir}/fake_{i}.png", normalize=True)

        print("✅ Synthetic images generated.")