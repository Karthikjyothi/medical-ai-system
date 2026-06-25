import os
import uuid
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

# =========================================
# GENERATE PDF REPORT
# =========================================
def generate_pdf_report(user_name, diagnosis_result, uploaded_image_path, gradcam_path, ai_summary):

    os.makedirs("uploads/reports", exist_ok=True)

    report_filename = f"{uuid.uuid4().hex}.pdf"
    report_path = os.path.join("uploads/reports", report_filename)

    doc = SimpleDocTemplate(report_path, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    # Title
    elements.append(Paragraph("MedIntel AI - Intelligent Medical Diagnostic Report", styles["Title"]))
    elements.append(Spacer(1, 20))

    # Patient Info
    elements.append(Paragraph(f"Patient Name: {user_name}", styles["Normal"]))
    elements.append(Paragraph(f"Generated On: {datetime.now()}", styles["Normal"]))
    elements.append(Spacer(1, 20))

    # Diagnosis Table
    data = [
        ["Dataset Module", diagnosis_result["dataset"]],
        ["Predicted Disease", diagnosis_result["predicted_disease"]],
        ["Confidence Score", f'{diagnosis_result["confidence"]}%'],
        ["Uncertainty", f'{diagnosis_result["uncertainty"]}%'],
        ["Risk Level", diagnosis_result["uncertainty_level"]],
    ]

    table = Table(data, colWidths=[150, 250])
    table.setStyle(TableStyle([
        ("GRID", (0,0), (-1,-1), 1, colors.black),
        ("BACKGROUND", (0,0), (-1,-1), colors.whitesmoke)
    ]))

    elements.append(table)
    elements.append(Spacer(1, 20))

    # Uploaded Image
    if os.path.exists(uploaded_image_path):
        elements.append(Paragraph("Uploaded Medical Scan", styles["Heading3"]))
        elements.append(Image(uploaded_image_path, width=200, height=200))
        elements.append(Spacer(1, 20))

    # GradCAM
    if os.path.exists(gradcam_path):
        elements.append(Paragraph("Explainable AI Heatmap (GradCAM)", styles["Heading3"]))
        elements.append(Image(gradcam_path, width=200, height=200))
        elements.append(Spacer(1, 20))

    # AI Summary
    elements.append(Paragraph("AI Medical Consultation Summary", styles["Heading3"]))
    elements.append(Paragraph(ai_summary.replace("\n", "<br/>"), styles["BodyText"]))

    doc.build(elements)

    return report_path