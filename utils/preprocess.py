import torchvision.transforms as transforms

def get_transforms():
    transform = transforms.Compose([
        transforms.Grayscale(),
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.5], [0.5]),
        transforms.RandomHorizontalFlip(),
        transforms.RandomRotation(10)
    ])
    return transform