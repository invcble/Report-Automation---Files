from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import letter
from PIL import Image
from datetime import datetime
import WorkbookReport as wr
import sys, os, shutil


# combined_csv_path = input("Paste the path to Combined CSV: ")[1:-1]
combined_csv_path = "Merck2024Combined_Suppliers.csv"
# feedback_csv_path = "Namefixed_ALLpeersMerk2024.csv"
# employee_num = int(input("Enter total number of employees: "))
employee_num = 50

date = datetime.today().strftime('%B %Y')
png = Image.open("Merck_Logo.png")      ###########  LOGO HERE  #############
logo = ImageReader(png)
white_logo = ImageReader(Image.composite(Image.new('RGBA', png.size, (255, 255, 255, 255)), png, png))

for s in range(employee_num):
# for s in range(0 , 3):
    if not os.path.exists("report_images//"):
        os.makedirs("report_images//")
    try:
        name = wr.gen_name_image(combined_csv_path, s+1)
        # feedback_list = wr.get_feedback(combined_csv_path, feedback_csv_path, s+1)
    except IndexError:
        print("No more employees left.")
        shutil.rmtree("report_images//")
        sys.exit()
    
    print(f"Generating PDF for {name}")

    o = canvas.Canvas("data_overlay.pdf", pagesize=letter)
    o.setFont("Helvetica", 11)
    o.setFillColor("white")
    o.drawString(62, 564, name +', '+ date)
    o.drawImage(white_logo, 422.5, 60.8, 115, 35, mask="auto", preserveAspectRatio=True )

    template = PdfReader("Merk_Diverse_Suppliers.pdf")      ###########  TEMPLATE HERE  #############
    #Actual Page No. is pagenum + 2
    for pagenum in range(len(template.pages)-1):
        o.showPage()
        if pagenum == 1:
            o.drawImage(logo, 365.3, 103.6, 185, 54, mask="auto", preserveAspectRatio=True )
        if pagenum == 2:
            chart = ImageReader("report_images//MOTAI" + f"{s+1}.png")
            o.drawImage(chart, 53, 447, 250, 150, mask="auto")
            chart = ImageReader("report_images//MOTSN" + f"{s+1}.png")
            o.drawImage(chart, 308, 447, 250, 150, mask="auto")
            chart = ImageReader("report_images//MOTNC" + f"{s+1}.png")
            o.drawImage(chart, 53, 170, 250, 150, mask="auto")
            chart = ImageReader("report_images//Leff" + f"{s+1}.png")
            o.drawImage(chart, 308, 170, 250, 150, mask="auto")
        if pagenum == 3:
            chart = ImageReader("report_images//MOTI" + f"{s+1}.png")
            o.drawImage(chart, 56, 420, 240, 144, mask="auto")
            chart = ImageReader("report_images//SI" + f"{s+1}.png")
            o.drawImage(chart, 315, 420, 240, 144, mask="auto")
            chart = ImageReader("report_images//MCON" + f"{s+1}.png")
            o.drawImage(chart, 56, 120, 240, 144, mask="auto")
            chart = ImageReader("report_images//WIT" + f"{s+1}.png")
            o.drawImage(chart, 315, 120, 240, 144, mask="auto")
        if pagenum == 4:
            chart = ImageReader("report_images//LBE" + f"{s+1}.png")
            o.drawImage(chart, 56, 435, 240, 144, mask="auto")
            chart = ImageReader("report_images//PDM" + f"{s+1}.png")
            o.drawImage(chart, 315, 435, 240, 144, mask="auto")
            chart = ImageReader("report_images//COACH" + f"{s+1}.png")
            o.drawImage(chart, 56, 150, 240, 144, mask="auto")
        if pagenum == 5:
            chart = ImageReader("report_images//INF" + f"{s+1}.png")
            o.drawImage(chart, 56, 445, 240, 144, mask="auto")
            chart = ImageReader("report_images//SCTI" + f"{s+1}.png")
            o.drawImage(chart, 315, 445, 240, 144, mask="auto")
        if pagenum == 6:
            chart = ImageReader("report_images//VL" + f"{s+1}.png")
            o.drawImage(chart, 55, 435, 240, 144, mask="auto")
            chart = ImageReader("report_images//MBL" + f"{s+1}.png")
            o.drawImage(chart, 303, 435, 240, 144, mask="auto")
        if pagenum == 8:
            o.drawImage(logo, 365.3, 65, 185, 54, mask="auto", preserveAspectRatio=True )
        if pagenum == 9:
            chart = ImageReader("report_images//SAFE" + f"{s+1}.png")
            o.drawImage(chart, 56, 430, 240, 144, mask="auto")
            chart = ImageReader("report_images//ITT" + f"{s+1}.png")
            o.drawImage(chart, 315, 430, 240, 144, mask="auto")
            chart = ImageReader("report_images//KS" + f"{s+1}.png")
            o.drawImage(chart, 56, 143, 240, 144, mask="auto")
            chart = ImageReader("report_images//IE" + f"{s+1}.png")
            o.drawImage(chart, 315, 143, 240, 144, mask="auto")
        if pagenum == 10:
            chart = ImageReader("report_images//NET" + f"{s+1}.png")
            o.drawImage(chart, 56, 425, 240, 144, mask="auto")
            chart = ImageReader("report_images//II" + f"{s+1}.png")
            o.drawImage(chart, 315, 425, 240, 144, mask="auto")
            chart = ImageReader("report_images//SAS" + f"{s+1}.png")
            o.drawImage(chart, 56, 145, 240, 144, mask="auto")
            chart = ImageReader("report_images//ASN" + f"{s+1}.png")
            o.drawImage(chart, 315, 145, 240, 144, mask="auto")
        if pagenum == 11:
            chart = ImageReader("report_images//COOP" + f"{s+1}.png")
            o.drawImage(chart, 185, 445, 240, 144, mask="auto")
        if pagenum == 12:
            chart = ImageReader("report_images//TMX" + f"{s+1}.png")
            o.drawImage(chart, 56, 420, 240, 144, mask="auto")
            chart = ImageReader("report_images//SL" + f"{s+1}.png")
            o.drawImage(chart, 315, 420, 240, 144, mask="auto")
        if pagenum == 13:
            chart = ImageReader("report_images//CRE" + f"{s+1}.png")
            o.drawImage(chart, 185, 475, 240, 144, mask="auto")
        if pagenum == 15:
            o.drawImage(logo, 365.3, 78, 185, 54, mask="auto", preserveAspectRatio=True )
        if pagenum == 16:
            chart = ImageReader("report_images//RTCRS" + f"{s+1}.png")
            o.drawImage(chart, 56, 430, 240, 144, mask="auto")
            chart = ImageReader("report_images//RTCER" + f"{s+1}.png")
            o.drawImage(chart, 315, 430, 240, 144, mask="auto")
        if pagenum == 17:
            chart = ImageReader("report_images//PT" + f"{s+1}.png")
            o.drawImage(chart, 56, 435, 240, 144, mask="auto")
            chart = ImageReader("report_images//PP" + f"{s+1}.png")
            o.drawImage(chart, 315, 435, 240, 144, mask="auto")
        if pagenum == 18:
            chart = ImageReader("report_images//EISE" + f"{s+1}.png")
            o.drawImage(chart, 56, 440, 240, 144, mask="auto")
            chart = ImageReader("report_images//EIOE" + f"{s+1}.png")
            o.drawImage(chart, 315, 440, 240, 144, mask="auto")
            chart = ImageReader("report_images//EIUE" + f"{s+1}.png")
            o.drawImage(chart, 56, 160, 240, 144, mask="auto")
            chart = ImageReader("report_images//EIRE" + f"{s+1}.png")
            o.drawImage(chart, 315, 160, 240, 144, mask="auto")
        if pagenum == 20:
            o.drawImage(logo, 365.3, 94, 185, 54, mask="auto", preserveAspectRatio=True )
        if pagenum == 21:
            chart = ImageReader("report_images//ALT" + f"{s+1}.png")
            o.drawImage(chart, 56, 443, 240, 144, mask="auto")
            chart = ImageReader("report_images//PAY" + f"{s+1}.png")
            o.drawImage(chart, 315, 443, 240, 144, mask="auto")
            chart = ImageReader("report_images//REL" + f"{s+1}.png")
            o.drawImage(chart, 56, 170, 240, 144, mask="auto")
            chart = ImageReader("report_images//SEC" + f"{s+1}.png")
            o.drawImage(chart, 315, 170, 240, 144, mask="auto")
        if pagenum == 22:
            chart = ImageReader("report_images//AUTH" + f"{s+1}.png")
            o.drawImage(chart, 56, 443, 240, 144, mask="auto")
            chart = ImageReader("report_images//VAR" + f"{s+1}.png")
            o.drawImage(chart, 315, 443, 240, 144, mask="auto")
            chart = ImageReader("report_images//AUTO" + f"{s+1}.png")
            o.drawImage(chart, 56, 170, 240, 144, mask="auto")
            chart = ImageReader("report_images//PRES" + f"{s+1}.png")
            o.drawImage(chart, 315, 170, 240, 144, mask="auto")        
        if pagenum == 24:
            o.drawImage(white_logo, 422.5, 56.8, 115, 35, mask="auto", preserveAspectRatio=True )
        
        o.setFont("Helvetica", 10)
        if pagenum != 24:
            o.drawString(535 - o.stringWidth(name.split('.')[1]), 38.3, name.split('.')[1])

    o.save()

    overlay = PdfReader("data_overlay.pdf")
    writer = PdfWriter()

    for pagenum in range(len(template.pages)):
        target_page = template.pages[pagenum]

        try:
            overlay_page = overlay.pages[pagenum]
            target_page.merge_page(overlay_page)
        except:
            pass
        writer.add_page(target_page)

    writer.write("Workbook "+f"{name}"+".pdf")
    shutil.rmtree("report_images//")
    os.remove("data_overlay.pdf")