from utils.uge import UniversalGenerativeEngine
import argparse
import os

# =========================
# ARGUMENTS (DATASET INPUT)
# =========================
parser = argparse.ArgumentParser()
parser.add_argument("--data", type=str, default="data/brain_tumor/train")
args = parser.parse_args()

train_path = args.data

# Extract dataset name (for logging clarity)
dataset_name = train_path.split("/")[-2]

print(f"🚀 Running UGE for dataset: {dataset_name}")

# =========================
# INIT ENGINE
# =========================
uge = UniversalGenerativeEngine(epochs=5)

# =========================
# TRAIN GAN ON DATASET
# =========================
uge.train(train_path)

# =========================
# GENERATE IMAGES
# =========================
uge.generate(dataset_name)

print("✅ UGE completed successfully!")