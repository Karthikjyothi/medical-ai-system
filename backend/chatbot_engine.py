import os
import requests
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

conversation_memory = {}

# =====================================
# OPENROUTER LLM CALL
# =====================================
def ask_openrouter(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:3000",
        "X-Title": "MedIntel-AI"
    }

    payload = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(url, headers=headers, json=payload, timeout=40)

    data = response.json()
    if "choices" not in data:
        raise Exception(str(data))

    if "choices" not in data:
        raise Exception(str(data))

    return data["choices"][0]["message"]["content"]


# =====================================
# MEDICAL COPILOT CHATBOT
# =====================================
def medical_chatbot(session_id, user_query, disease_name, confidence, uncertainty_level):

    if session_id not in conversation_memory:
        conversation_memory[session_id] = []

    previous_context = "\n".join(conversation_memory[session_id])

    prompt = f"""
You are MedIntel AI Doctor Copilot, an advanced conversational medical consultation assistant.

Current Diagnosis Context:
Disease Predicted: {disease_name}
Confidence Score: {confidence}%
Uncertainty Level: {uncertainty_level}

Previous Conversation:
{previous_context}

Patient Current Question:
{user_query}

Instructions:
- Answer like a smart human medical consultant.
- Maintain continuity with previous questions.
- Be warm, natural, and conversational.
- Explain deeply if user asks about disease, symptoms, seriousness, confidence, uncertainty, precautions, body effects, treatment, home care.
- Avoid dangerous prescriptions.
- Give medically responsible educational guidance.
- Respond in 2 to 5 meaningful paragraphs depending on the question depth.
- Always encourage the patient to consult with a healthcare professional for a comprehensive evaluation and personalized medical advice.
- If the user asks for a second opinion, provide general advice on seeking a second opinion.
- If the user asks about the accuracy of the diagnosis, explain it deeply.
- If the user asks about the uncertainty, explain how uncertainty is calculated and what it means.
- If the user asks about the confidence, explain how confidence is calculated and what it means.
- If the user asks about the disease, explain what the disease is, how it affects the body, and common symptoms.
- If the user asks about symptoms, explain common manifestations.
- If the user asks about seriousness, explain complications and urgency.
- If the user asks about precautions, explain detailed precautionary measures.
- If the user asks about home care, explain supportive home management.
- If the user asks about treatment guidance, explain common treatment pathways.
- If the user asks about doctor consultation, explain when and why specialist consultation is needed.
"""

    try:
        bot_reply = ask_openrouter(prompt)

    except Exception as e:
        print("OpenRouter AI failed:", e)

        bot_reply = f"""
Predicted condition: {disease_name}

AI cloud consultation is temporarily unavailable.

Current model confidence is {confidence}% with {uncertainty_level} uncertainty.
Please consult a medical specialist for detailed interpretation while the local diagnosis report remains valid.
"""

    conversation_memory[session_id].append(f"User: {user_query}")
    conversation_memory[session_id].append(f"Bot: {bot_reply}")

    return bot_reply

# =====================================
# GENERAL MEDICAL GPT ASSISTANT
# =====================================
def general_medical_chatbot(session_id, user_query):

    if session_id not in conversation_memory:
        conversation_memory[session_id] = []

    previous_context = "\n".join(conversation_memory[session_id])

    prompt = f"""
You are MedIntel MedicalGPT, a highly knowledgeable conversational AI assistant specialized only in medicine, healthcare, diseases, symptoms, diagnostics, nutrition, preventive care, anatomy, pathology, clinical explanation, and patient guidance.

Previous Conversation:
{previous_context}

User Current Question:
{user_query}

Instructions:
- Answer naturally like ChatGPT but strictly in medical domain.
- Maintain continuity with previous messages.
- Understand follow-up questions.
- Explain deeply but clearly.
- Be warm, intelligent, and medically informative.
- If user asks non-medical questions, politely redirect that this assistant is specialized for healthcare only.
- Avoid direct dangerous prescriptions.
- Give educational consultation style responses.
- Response should feel human and advanced.
- If the user asks for a second opinion, provide general advice on seeking a second opinion.
- If the user asks about the accuracy of the diagnosis, explain it deeply.
- If the user asks about the uncertainty, explain how uncertainty is calculated and what it means.
- If the user asks about the confidence, explain how confidence is calculated and what it means.
- If the user asks about the disease, explain what the disease is, how it affects the body, and common symptoms.
- If the user asks about symptoms, explain common manifestations.
- If the user asks about seriousness, explain complications and urgency.
- If the user asks about precautions, explain detailed precautionary measures.
- If the user asks about home care, explain supportive home management.
- If the user asks about treatment guidance, explain common treatment pathways.
- If the user asks about doctor consultation, explain when and why specialist consultation is needed.
- Always encourage the user to consult with a healthcare professional for a comprehensive evaluation and personalized medical advice.
- If the user asks about nutrition, provide general dietary advice related to health and wellness.
- If the user asks about preventive care, provide general advice on preventive health measures and screenings.
- If the user asks about anatomy or pathology, provide clear explanations of relevant anatomical structures or pathological processes.
- If the user asks about clinical explanations, provide detailed explanations of medical concepts in an accessible manner.
- If the user asks about patient guidance, provide general advice on managing health conditions and navigating healthcare systems.
- If user asks friendly questions, respond warmly and maintain a good relationship
- If the question demands giving historical information or statistics, provide accurate and up-to-date information ask the internet if needed.
- try to respond by giving table format if the question demands comparison or listing of multiple items.
"""

    try:
        bot_reply = ask_openrouter(prompt)

    except Exception as e:
        print("MedicalGPT failed:", e)
        bot_reply = "Medical AI assistant is temporarily unavailable."

    conversation_memory[session_id].append(f"User: {user_query}")
    conversation_memory[session_id].append(f"Bot: {bot_reply}")

    return bot_reply

def generate_medical_summary(disease_name, confidence, uncertainty_level):
    prompt = f"""
You are MedIntel AI Clinical Report Generator.

Diagnosis Details:
Disease Predicted: {disease_name}
Confidence Score: {confidence}%
Uncertainty Level: {uncertainty_level}

Generate a professional formal medical summary in exactly 3 concise paragraphs:

Paragraph 1:
Explain what this diagnosed disease/condition is and what it generally indicates in the human body.

Paragraph 2:
Explain the seriousness level, likely symptoms, and what the confidence + uncertainty imply regarding this AI finding.

Paragraph 3:
Provide general precautions, follow-up recommendations, and when medical consultation is advisable.

STRICT INSTRUCTIONS:
- Do not use conversational openings like Certainly, Of course, I'm glad, Here is your summary.
- Do not speak like a chatbot.
- Write like a clinical AI analysis report.
- Keep language professional, direct, and medically informative.
- No bullet points.
"""

    try:
        return ask_openrouter(prompt)

    except Exception as e:
        print("Summary AI failed:", e)
        return f"The AI model predicts {disease_name} with {confidence}% confidence and {uncertainty_level} uncertainty. Clinical review and routine specialist consultation are recommended."