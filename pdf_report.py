from reportlab.pdfgen import canvas


def create_pdf(filename, score, skills, missing, jobs):

    pdf = canvas.Canvas(filename)

    pdf.drawString(50, 800, "AI Resume Analyzer Report")

    pdf.drawString(50, 760, f"Resume Score: {score}%")

    pdf.drawString(50, 720, "Skills Found:")

    y = 700

    for skill in skills:
        pdf.drawString(70, y, "- " + skill)
        y -= 20


    pdf.drawString(50, y-20, "Missing Skills:")

    y -= 40

    for skill in missing:
        pdf.drawString(70, y, "- " + skill)
        y -= 20


    pdf.drawString(50, y-20, "Recommended Jobs:")

    y -= 40

    for job in jobs:
        pdf.drawString(70, y, "- " + job)
        y -= 20


    pdf.save()