disease_info = {
    "glioma": {
        "description": "Glioma is a type of brain tumor that occurs in the brain and spinal cord.",
        "symptoms": ["Headache", "Nausea", "Vision problems", "Seizures"],
        "precautions": [
            "Consult a neurologist immediately",
            "Avoid stress",
            "Follow prescribed medications",
            "Regular MRI monitoring"
        ],
        "severity": "Can be serious depending on type and growth rate."
    },

    "meningioma": {
        "description": "Meningioma is usually a non-cancerous tumor arising from brain membranes.",
        "symptoms": ["Headache", "Hearing loss", "Memory issues"],
        "precautions": [
            "Regular checkups",
            "Monitor tumor growth",
            "Maintain healthy lifestyle"
        ],
        "severity": "Often slow-growing and less aggressive."
    },

    "no_tumor": {
        "description": "No tumor detected in the MRI scan.",
        "symptoms": [],
        "precautions": [
            "Maintain healthy lifestyle",
            "Regular health checkups"
        ],
        "severity": "No immediate concern."
    },

    "pituatory": {
        "description": "Pituitary tumor affects hormone-producing gland in brain.",
        "symptoms": ["Hormonal imbalance", "Vision problems", "Fatigue"],
        "precautions": [
            "Consult endocrinologist",
            "Monitor hormone levels",
            "Follow medical advice"
        ],
        "severity": "Manageable if detected early."
    }
}
def get_disease_info(label):
    info = disease_info.get(label)

    if info:
        return info

    # fallback (for unknown diseases)
    return {
        "description": f"{label} is a medical condition detected by the model.",
        "precautions": [
            "Consult a medical professional",
            "Follow proper diagnosis procedures",
            "Do not rely solely on AI results"
        ],
        "severity": "Unknown - requires clinical evaluation"
    }