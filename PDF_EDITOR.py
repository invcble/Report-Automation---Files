from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import letter


o = canvas.Canvas("new.pdf", pagesize=letter)
o.setFont("Helvetica", 12)
o.setFillColor("white")
o.drawString(62, 530, "Imon Bera")

logo = ImageReader("logo.png")
o.drawImage(logo, 430, 100, 100, 30, mask="auto")
o.save()

reader = PdfReader("Ahn.pdf")
overlay = PdfReader("new.pdf")
writer = PdfWriter()
# Read the existing PDF

for pagenum in range(len(reader.pages)):
    target_page = reader.pages[pagenum]

    try:
        overlay_page = overlay.pages[pagenum]
        target_page.merge_page(overlay_page)
    except:
        pass
    writer.add_page(target_page)

writer.write("Overlay+target.pdf")