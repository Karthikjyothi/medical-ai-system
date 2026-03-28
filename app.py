import streamlit as st
from PIL import Image
import torch
import torchvision.transforms as transforms
import numpy as np
import os

from utils.chatbot import chatbot_response
from torchvision import datasets
from model.cnn import get_model
from utils.gradcam import generate_gradcam

# =========================
# DEVICE
# =========================
device = "cuda" if torch.cuda.is_available() else "cpu"

# =========================
# TRANSFORM
# =========================
transform = transforms.Compose([
    transforms.Grayscale(),
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.5], [0.5])
])

# =========================
# 📂 DATASET SELECTION
# =========================
DATA_ROOT = "data"

available_datasets = [
    d for d in os.listdir(DATA_ROOT)
    if os.path.isdir(os.path.join(DATA_ROOT, d))
]

st.sidebar.title("⚙️ Settings")
selected_dataset = st.sidebar.selectbox("Select Dataset", available_datasets)

train_path = os.path.join(DATA_ROOT, selected_dataset, "train")

# =========================
# LOAD DATASET (AUTO CLASSES)
# =========================
dataset = datasets.ImageFolder(train_path, transform=transform)
class_names = dataset.classes
num_classes = len(class_names)

# =========================
# LOAD MODEL (AUTO)
# =========================
model = get_model(num_classes=num_classes)

model_path = f"outputs/models/model_{selected_dataset}.pth"

if os.path.exists(model_path):
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.to(device)
    model.eval()
else:
    st.error(f"❌ Model not found for dataset: {selected_dataset}")
    st.stop()

# =========================
# MC DROPOUT
# =========================
def mc_predict(image_path, model, transform, passes=10):
    image = Image.open(image_path)
    image = transform(image).unsqueeze(0).to(device)

    model.eval()  # keep base model stable

    predictions = []

    for _ in range(passes):
        # temporarily enable dropout ONLY
        def enable_dropout(m):
            if isinstance(m, torch.nn.Dropout):
                m.train()

        model.apply(enable_dropout)

        output = model(image)
        probs = torch.softmax(output, dim=1)
        predictions.append(probs.detach().cpu().numpy())

    predictions = np.array(predictions)

    mean_probs = predictions.mean(axis=0)
    std_probs = predictions.std(axis=0)

    predicted_class = np.argmax(mean_probs)
    confidence = mean_probs[0][predicted_class]
    uncertainty = std_probs[0][predicted_class]

    return predicted_class, confidence, uncertainty


def get_uncertainty_level(unc):
    if unc < 0.05:
        return "Low"
    elif unc < 0.15:
        return "Medium"
    else:
        return "High"


# =========================
# 🎨 UI
# =========================
st.title("🧠 Medical Image Intelligence System")
st.write("Upload an image for disease detection")

st.write(f"📂 Current Dataset: **{selected_dataset}**")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)

    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Save temp for Grad-CAM
    image.save("temp.jpg")

    # Prediction
    cls, conf, unc = mc_predict("temp.jpg", model, transform)

    label = class_names[cls]

    st.subheader(f"Prediction: {label}")
    st.subheader(f"Confidence: {conf*100:.2f}%")

    level = get_uncertainty_level(unc)
    st.subheader(f"Uncertainty: {level} ({unc:.4f})")

    # Grad-CAM
    cam_image = generate_gradcam("temp.jpg")
    st.image(cam_image, caption="Grad-CAM Heatmap", use_column_width=True)

st.subheader("🤖 Medical Assistant")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_query = st.text_input("Ask your question...")

if user_query:
    response = chatbot_response(user_query, label)

    st.session_state.chat_history.append(("You", user_query))
    st.session_state.chat_history.append(("Bot", response))

for speaker, msg in st.session_state.chat_history:
    if speaker == "You":
        st.write(f"🧑‍💻 **You:** {msg}")
    else:
        st.write(f"🤖 **Bot:** {msg}")


# =========================
# 📊 METRICS + GENERATED DATA
# =========================
st.subheader("📊 Training Metrics")

if os.path.exists("outputs/accuracy.png"):
    st.image("outputs/accuracy.png", caption="Accuracy Graph")

if os.path.exists("outputs/loss.png"):
    st.image("outputs/loss.png", caption="Loss Graph")
if os.path.exists("outputs/confusion_matrix.png"):
    st.image("outputs/confusion_matrix.png", caption="Confusion Matrix")

st.subheader("🧬 Generated Synthetic Images")

gen_path = "outputs/generated_images"

if os.path.exists(gen_path):
    classes = os.listdir(gen_path)

    for cls in classes:
        st.write(f"### {cls}")
        class_folder = os.path.join(gen_path, cls)

        images = [
            f for f in os.listdir(class_folder)
            if f.lower().endswith((".png", ".jpg", ".jpeg"))
        ][:5]

        if len(images) > 0:
            cols = st.columns(len(images))

            for i, img_name in enumerate(images):
                img_path = os.path.join(class_folder, img_name)

                if os.path.isfile(img_path):
                    cols[i].image(img_path, use_column_width=True)
        else:
            st.warning(f"No images found in {cls}")
'''
        for i, img_name in enumerate(images):
            img_path = os.path.join(class_folder, img_name)

            if os.path.isfile(img_path):
                cols[i].image(img_path, use_column_width=True)
                '''