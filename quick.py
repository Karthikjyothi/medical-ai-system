import os

for cls in os.listdir("data/brain_tumor/train"):
    print(cls, len(os.listdir(f"data/brain_tumor/train/{cls}")))