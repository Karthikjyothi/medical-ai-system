from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# ==============================
# USER AUTH SCHEMAS
# ==============================

class UserRegister(BaseModel):
    full_name: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: str

    class Config:
        from_attributes = True


# ==============================
# DIAGNOSIS RESPONSE SCHEMA
# ==============================

class DiagnosisResponse(BaseModel):
    id: int
    dataset: str
    predicted_disease: str
    confidence: float
    uncertainty: float
    uncertainty_level: str
    uploaded_image: str
    gradcam_image: str
    pdf_report: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


# ==============================
# CHATBOT SCHEMAS
# ==============================

class ChatRequest(BaseModel):
    user_id: int
    disease_context: str
    user_query: str


class ChatResponse(BaseModel):
    response: str


# ==============================
# LOGIN TOKEN RESPONSE
# ==============================

class AuthResponse(BaseModel):
    message: str
    user: Optional[UserResponse] = None