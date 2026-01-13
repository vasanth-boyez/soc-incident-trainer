# report.py

from io import BytesIO
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


def build_pdf_bytes(scenario_text, timeline, score, level, feedback) -> bytes:
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("<b>Cyber Incident Response Training Report</b>", styles["Title"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles["Normal"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("<b>Scenario Summary</b>", styles["Heading2"]))
    story.append(Paragraph(scenario_text, styles["BodyText"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("<b>Action Timeline</b>", styles["Heading2"]))
    for step in timeline:
        story.append(Paragraph(step, styles["BodyText"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("<b>Final Score</b>", styles["Heading2"]))
    story.append(Paragraph(f"Score: {score}/100", styles["BodyText"]))
    story.append(Paragraph(f"Readiness Level: {level}", styles["BodyText"]))

    if feedback:
        story.append(Spacer(1, 12))
        story.append(Paragraph("<b>Learning Feedback</b>", styles["Heading2"]))
        for f in feedback:
            story.append(Paragraph(f"- {f}", styles["BodyText"]))

    doc.build(story)
    buffer.seek(0)
    return buffer.read()
