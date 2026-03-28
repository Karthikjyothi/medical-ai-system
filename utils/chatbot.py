from utils.disease_info import get_disease_info

def chatbot_response(user_query, disease):
    query = user_query.lower()
    info = get_disease_info(disease)

    if "what" in query or "about" in query:
        return info["description"]

    elif "symptom" in query:
        return "Common symptoms include: " + ", ".join(info.get("symptoms", ["Consult doctor"]))

    elif "precaution" in query or "care" in query:
        return "Precautions:\n- " + "\n- ".join(info["precautions"])

    elif "danger" in query or "serious" in query:
        return info["severity"]

    elif "cure" in query or "treatment" in query:
        return "Treatment depends on severity. Please consult a specialist."

    else:
        return f"This is related to {disease}. Please consult a medical professional for detailed advice."