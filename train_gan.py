import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
from torch.utils.data import DataLoader, Subset
from model.gan import Generator, Discriminator

device = "cuda" if torch.cuda.is_available() else "cpu"

# Hyperparameters
lr = 0.0002
batch_size = 32
image_size = 64
z_dim = 100
epochs = 10  # keep small for laptop

# Transform
transform = transforms.Compose([
    transforms.Grayscale(),
    transforms.Resize((image_size, image_size)),
    transforms.ToTensor(),
    transforms.Normalize([0.5], [0.5])
])

# Load full dataset
dataset = torchvision.datasets.ImageFolder(root="data/train", transform=transform)

# Class names (IMPORTANT)
classes = dataset.classes

criterion = nn.BCELoss()

print("🚀 Starting CLASS-WISE GAN training...")

# Loop through each class
for cls in classes:
    print(f"\n🔥 Training GAN for class: {cls}")

    # Get class index
    class_idx = dataset.class_to_idx[cls]

    # Filter dataset for this class
    indices = [i for i, (_, label) in enumerate(dataset.samples) if label == class_idx]
    subset = Subset(dataset, indices)

    loader = DataLoader(subset, batch_size=batch_size, shuffle=True)

    # Initialize models
    gen = Generator(z_dim).to(device)
    disc = Discriminator().to(device)

    opt_gen = optim.Adam(gen.parameters(), lr=lr, betas=(0.5, 0.999))
    opt_disc = optim.Adam(disc.parameters(), lr=lr, betas=(0.5, 0.999))

    # Training loop
    for epoch in range(epochs):
        for real, _ in loader:
            real = real.to(device)

            noise = torch.randn(real.shape[0], z_dim, 1, 1).to(device)
            fake = gen(noise)

            # Train Discriminator
            disc_real = disc(real).reshape(-1)
            loss_real = criterion(disc_real, torch.ones_like(disc_real))

            disc_fake = disc(fake.detach()).reshape(-1)
            loss_fake = criterion(disc_fake, torch.zeros_like(disc_fake))

            loss_disc = (loss_real + loss_fake) / 2

            disc.zero_grad()
            loss_disc.backward()
            opt_disc.step()

            # Train Generator
            output = disc(fake).reshape(-1)
            loss_gen = criterion(output, torch.ones_like(output))

            gen.zero_grad()
            loss_gen.backward()
            opt_gen.step()

        print(f"{cls} Epoch [{epoch+1}/{epochs}] Loss D: {loss_disc:.4f}, Loss G: {loss_gen:.4f}")

    # Save generator for this class
    torch.save(gen.state_dict(), f"generator_{cls}.pth")
    print(f"✅ Saved generator_{cls}.pth")

print("\n🎉 All class-wise GANs trained successfully!")