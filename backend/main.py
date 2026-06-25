import os
import shutil
import uuid

from fastapi import FastAPI, UploadFile, File, Depends, Form
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from training_engine import UniversalTrainingEngine
from chatbot_engine import medical_chatbot, generate_medical_summary, ask_openrouter,general_medical_chatbot
from datetime import datetime

from database import init_db, get_db, DiagnosisHistory
from schemas import *
from auth import register_user, authenticate_user

from model_registry import load_all_models, get_available_datasets
from inference_engine import run_prediction
from gradcam_engine import generate_gradcam
from chatbot_engine import medical_chatbot, generate_medical_summary
from report_generator import generate_pdf_report

from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# ==========================================
# APP INIT
# ==========================================
app = FastAPI(title="MedIntel AI Backend")
import threading

training_status = {}

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TrainRequest(BaseModel):
    dataset_name: str

def run_training(dataset_name):

    global training_status

    try:
        training_status[dataset_name] = "Initializing training pipeline..."

        trainer = UniversalTrainingEngine()

        training_status[dataset_name] = "Running GAN + SSL + CNN training..."

        result = trainer.train_dataset(dataset_name)

        training_status[dataset_name] = result["message"]

    except Exception as e:
        training_status[dataset_name] = f"Training failed: {str(e)}"

class CompareRequest(BaseModel):
    left_disease: str
    right_disease: str
    left_confidence: float
    right_confidence: float
    left_uncertainty: str
    right_uncertainty: str

# ==========================================
# STARTUP LOAD
# ==========================================
@app.on_event("startup")
def startup_event():
    init_db()
    load_all_models()
    os.makedirs("uploads/images", exist_ok=True)
    trainer = UniversalTrainingEngine()


# ==========================================
# REGISTER API
# ==========================================
@app.post("/register", response_model=AuthResponse)
def register(data: UserRegister, db: Session = Depends(get_db)):
    user = register_user(db, data.full_name, data.email, data.password)

    if user is None:
        return {"message": "Email already exists", "user": None}

    return {"message": "Registration successful", "user": user}


# ==========================================
# LOGIN API
# ==========================================
@app.post("/login", response_model=AuthResponse)
def login(data: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, data.email, data.password)

    if user is None:
        return {"message": "Invalid credentials", "user": None}

    return {"message": "Login successful", "user": user}


# ==========================================
# GET DATASETS API
# ==========================================
@app.get("/datasets")
def datasets():
    return {"available_datasets": get_available_datasets()}


# ==========================================
# DIAGNOSIS API
# ==========================================
@app.post("/diagnose")
def diagnose(
    user_id: int = Form(...),
    dataset_name: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # save uploaded image
    image_filename = f"{uuid.uuid4().hex}_{file.filename}"
    image_path = os.path.join("uploads/images", image_filename)

    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # run prediction
    diagnosis_result = run_prediction(image_path, dataset_name)

    if diagnosis_result is None:
        return {"error": "Dataset model not found"}

    # gradcam
    gradcam_path = generate_gradcam(image_path, dataset_name)

    # ai summary auto generation
    # ai summary auto generation
    ai_summary = generate_medical_summary(
        disease_name=diagnosis_result["predicted_disease"],
        confidence=diagnosis_result["confidence"],
        uncertainty_level=diagnosis_result["uncertainty_level"]
    )

    radiologist_opinion = ask_openrouter(f"""
    You are an expert radiologist.

    Generate a short radiological imaging observation for detected disease:
    {diagnosis_result["predicted_disease"]}

    Confidence: {diagnosis_result["confidence"]}%

    Mention likely abnormal visual feature concentration and image interpretation in 3 professional lines.
    """)

    specialist_opinion = ask_openrouter(f"""
    You are a senior medical specialist.

    Detected disease: {diagnosis_result["predicted_disease"]}
    Confidence: {diagnosis_result["confidence"]}%
    Uncertainty: {diagnosis_result["uncertainty_level"]}

    Generate a concise clinical specialist opinion including seriousness, probable concern, and suggested consultation in 3 lines.
    """)

    preventive_advice = ask_openrouter(f"""
    You are a preventive healthcare advisor.

    Detected disease: {diagnosis_result["predicted_disease"]}

    Generate 3 line patient-friendly preventive care and lifestyle recommendation.
    """)

    # pdf report
    report_path = generate_pdf_report(
        user_name=f"User {user_id}",
        diagnosis_result=diagnosis_result,
        uploaded_image_path=image_path,
        gradcam_path=gradcam_path,
        ai_summary=ai_summary
    )

    # save history
    history = DiagnosisHistory(
        user_id=user_id,
        dataset=diagnosis_result["dataset"],
        predicted_disease=diagnosis_result["predicted_disease"],
        confidence=diagnosis_result["confidence"],
        uncertainty=diagnosis_result["uncertainty"],
        uncertainty_level=diagnosis_result["uncertainty_level"],
        uploaded_image=image_path,
        gradcam_image=gradcam_path,
        pdf_report=report_path
    )

    db.add(history)
    db.commit()

    return {
        "diagnosis": diagnosis_result,
        "gradcam_path": gradcam_path,
        "report_path": report_path,
        "ai_summary": ai_summary,
        "radiologist_opinion": radiologist_opinion,
        "specialist_opinion": specialist_opinion,
        "preventive_advice": preventive_advice
    }


# ==========================================
# CHAT API
# ==========================================
@app.post("/chat")
def chat(
    session_id: str = Form(...),
    user_query: str = Form(...),
    disease_name: str = Form(...),
    confidence: float = Form(...),
    uncertainty_level: str = Form(...)
):
    response = medical_chatbot(
        session_id=session_id,
        user_query=user_query,
        disease_name=disease_name,
        confidence=confidence,
        uncertainty_level=uncertainty_level
    )

    return {"response": response}

# ==========================================
# ADMIN UNIVERSAL DATASET TRAINING API
# ==========================================
@app.post("/admin/train-dataset")
def train_new_dataset(dataset_name: str = Form(...)):
    result = trainer.train_dataset(dataset_name)
    return result

@app.get("/history/{user_id}")
def get_history(user_id: int, db: Session = Depends(get_db)):
    records = db.query(DiagnosisHistory).filter(
        DiagnosisHistory.user_id == user_id
    ).order_by(DiagnosisHistory.id.desc()).all()

    history = []

    for r in records:
        history.append({
            "id": r.id,
            "dataset": r.dataset,
            "predicted_disease": r.predicted_disease,
            "confidence": r.confidence,
            "uncertainty": r.uncertainty,
            "uncertainty_level": r.uncertainty_level,
            "uploaded_image": r.uploaded_image,
            "gradcam_image": r.gradcam_image,
            "pdf_report": r.pdf_report,
            "created_at": str(r.created_at)
        })

    return {"history": history}

@app.delete("/history/delete/{record_id}")
def delete_history_record(record_id: int, db: Session = Depends(get_db)):
    record = db.query(DiagnosisHistory).filter(DiagnosisHistory.id == record_id).first()

    if not record:
        return {"message": "Record not found"}

    db.delete(record)
    db.commit()

    return {"message": "Diagnosis history deleted successfully"}

@app.post("/admin/train")
def admin_train(request: TrainRequest):

    dataset_name = request.dataset_name

    if dataset_name in training_status:
        return {
            "status": "running",
            "message": "Training already in progress"
        }

    training_thread = threading.Thread(
        target=run_training,
        args=(dataset_name,)
    )

    training_thread.start()

    return {
        "status": "started",
        "message": f"{dataset_name} training started in background"
    }

@app.get("/admin/train-status/{dataset_name}")
def get_training_status(dataset_name: str):

    status = training_status.get(
        dataset_name,
        "No active training found"
    )

    return {
        "dataset": dataset_name,
        "status": status
    }

@app.post("/compare-reports-ai")
def compare_reports_ai(data: CompareRequest):
    prompt = f"""
You are MedIntel AI Comparative Clinical Analysis Engine.

Report A:
Disease: {data.left_disease}
Confidence: {data.left_confidence}%
Uncertainty: {data.left_uncertainty}

Report B:
Disease: {data.right_disease}
Confidence: {data.right_confidence}%
Uncertainty: {data.right_uncertainty}

Generate one professional comparative medical intelligence paragraph that includes:
- comparative confidence reliability
- likely diagnostic seriousness differences
- explain that GradCAM evidence may vary due to feature activation differences
- why retrospective report comparison is useful

STRICT:
- no bullet points
- no conversational style
- clinical analytical tone
"""

    try:
        result = ask_openrouter(prompt)
        return {"comparison": result}
    except Exception as e:
        print(e)
        return {
            "comparison": f"{data.left_disease} and {data.right_disease} represent two separate diagnostic outcomes. Confidence and uncertainty analysis indicate measurable variation in AI reliability across both reports, while GradCAM activation may reflect differing radiological feature attention."
        }
    
@app.get("/admin/dataset-analytics")
def dataset_analytics(db: Session = Depends(get_db)):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    dataset_root = os.path.join(BASE_DIR, "..", "data")
    dataset_root = os.path.abspath(dataset_root)

    dataset_folders = [
        d for d in os.listdir(dataset_root)
        if os.path.isdir(os.path.join(dataset_root, d))
    ]

    active_datasets = len(dataset_folders)

    total_classes = 0
    latest_dataset = "N/A"
    latest_time = None

    for ds in dataset_folders:
        train_path = os.path.join(dataset_root, ds, "train")

        if os.path.exists(train_path):
            class_count = len([
                c for c in os.listdir(train_path)
                if os.path.isdir(os.path.join(train_path, c))
            ])
            total_classes += class_count

        modified = os.path.getmtime(os.path.join(dataset_root, ds))
        if latest_time is None or modified > latest_time:
            latest_time = modified
            latest_dataset = ds

    total_reports = db.query(DiagnosisHistory).count()

    return {
        "active_datasets": active_datasets,
        "total_classes": total_classes,
        "total_reports": total_reports,
        "latest_dataset": latest_dataset,
        "engines_active": "GAN + SSL + CNN + GradCAM + Copilot"
    }

@app.get("/similar-cases/{user_id}/{disease_name}/{dataset_name}")
def similar_cases(user_id: int, disease_name: str, dataset_name: str, db: Session = Depends(get_db)):
    records = db.query(DiagnosisHistory).filter(
        DiagnosisHistory.user_id == user_id,
        DiagnosisHistory.predicted_disease == disease_name
    ).order_by(DiagnosisHistory.id.desc()).limit(3).all()

    if len(records) == 0:
        records = db.query(DiagnosisHistory).filter(
            DiagnosisHistory.user_id == user_id,
            DiagnosisHistory.dataset == dataset_name
        ).order_by(DiagnosisHistory.id.desc()).limit(3).all()

    result = []
    for item in records:
        result.append({
            "id": item.id,
            "predicted_disease": item.predicted_disease,
            "confidence": item.confidence,
            "dataset": item.dataset,
            "gradcam_image": item.gradcam_image,
            "created_at": str(item.created_at)
        })

    return {"cases": result}

@app.post("/medical-assistant-chat")
def medical_assistant_chat(
    session_id: str = Form(...),
    user_query: str = Form(...)
):
    response = general_medical_chatbot(session_id, user_query)
    return {"response": response}