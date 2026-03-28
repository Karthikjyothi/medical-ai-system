import torch
import os
import torchvision.utils as vutils
from model.gan import Generator

device = "cuda" if torch.cuda.is_available() else "cpu"

classes = ["glioma", "meningioma", "pituatory", "no_tumor"]
z_dim = 100

for cls in classes:
    print(f"Generating images for {cls}")

    gen = Generator().to(device)
    gen.load_state_dict(torch.load(f"generator_{cls}.pth", map_location=device))
    gen.eval()

    output_dir = f"outputs/generated_images/{cls}"
    os.makedirs(output_dir, exist_ok=True)

    for i in range(20):  # fewer but better
        noise = torch.randn(1, z_dim, 1, 1).to(device)
        fake = gen(noise)

        vutils.save_image(fake, f"{output_dir}/fake_{i}.png", normalize=True)

print("✅ All class-wise images generated!")