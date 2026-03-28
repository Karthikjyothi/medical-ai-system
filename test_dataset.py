from torchvision import datasets
from torch.utils.data import DataLoader
from utils.preprocess import get_transforms

dataset = datasets.ImageFolder(root="data/train", transform=get_transforms())
loader = DataLoader(dataset, batch_size=8, shuffle=True)

for images, labels in loader:
    print("Images shape:", images.shape)
    print("Labels:", labels)
    break