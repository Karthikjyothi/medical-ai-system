import os
from utils.uge import UniversalGenerativeEngine

uge = UniversalGenerativeEngine(epochs=5)

DATA_ROOT = "data"

datasets = [
    d for d in os.listdir(DATA_ROOT)
    if os.path.isdir(os.path.join(DATA_ROOT, d))
]

for dataset in datasets:
    train_path = os.path.join(DATA_ROOT, dataset, "train")

    if os.path.exists(train_path):
        print(f"\n🚀 Training UGE for: {dataset}")
        uge.train(train_path)