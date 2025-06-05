from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import letter
from PIL import Image
from datetime import datetime
import WorkbookReport as wr
import sys, os, shutil
import pandas as pd
import re


def clean_ascii_str(s: str) -> str:
    return re.sub(r'[^\x00-\x7F]', '', str(s)) if pd.notna(s) else s

def clean_ascii_names(df: pd.DataFrame) -> pd.DataFrame:
    for col in ['FName', 'LName']:
        if col in df.columns:
            df[col] = df[col].apply(lambda x: clean_ascii_str(x))
    return df

def load_and_clean_to_csv(input_path: str, prefix: str) -> str:
    _, fname = os.path.split(input_path)
    _, ext = os.path.splitext(fname)
    temp_name = f"{prefix}_cleaned.csv"

    if ext.lower() in ['.xls', '.xlsx']:
        df = pd.read_excel(input_path)
    else:
        df = pd.read_csv(input_path)

    df = clean_ascii_names(df)
    df.to_csv(temp_name, index=False)
    return temp_name

def process(combined_path, feedback_path, logo_path, template_path):
    # ─────────────────────────────────────────────────────────────────────────────
    combined_csv_path = combined_path
    feedback_csv_path = feedback_path
    LOGO_PATH      = logo_path
    TEMPLATE_PATH  = template_path
    employee_num = 3
    # ─────────────────────────────────────────────────────────────────────────────

    cleaned_combined_path = load_and_clean_to_csv(combined_csv_path, prefix="combined")
    cleaned_feedback_path = load_and_clean_to_csv(feedback_csv_path, prefix="feedback")

    combined_csv_path = cleaned_combined_path
    feedback_csv_path = cleaned_feedback_path


    date = datetime.today().strftime('%B %Y')
    png = Image.open(LOGO_PATH)
    logo = ImageReader(png)
    white_logo = ImageReader(Image.composite(Image.new('RGBA', png.size, (255, 255, 255, 255)), png, png))

    for s in range(employee_num):
        os.makedirs("report_images//", exist_ok=True)
        os.makedirs("workbook_reports", exist_ok=True)
        try:
            name, savename = wr.gen_name_image(combined_csv_path, s+1)
            feedback_list = wr.get_feedback(combined_csv_path, feedback_csv_path, s+1)
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

        template = PdfReader(TEMPLATE_PATH)
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
                o.drawImage(chart, 153, 427, 300, 180, mask="auto")
                chart = ImageReader("report_images//SI" + f"{s+1}.png")
                o.drawImage(chart, 153, 130, 300, 180, mask="auto")
            if pagenum == 4:
                chart = ImageReader("report_images//MCON" + f"{s+1}.png")
                o.drawImage(chart, 153, 427, 300, 180, mask="auto")
                chart = ImageReader("report_images//WIT" + f"{s+1}.png")
                o.drawImage(chart, 153, 125, 300, 180, mask="auto")
            if pagenum == 5:
                chart = ImageReader("report_images//LBE" + f"{s+1}.png")
                o.drawImage(chart, 153, 415, 300, 180, mask="auto")
                chart = ImageReader("report_images//PDM" + f"{s+1}.png")
                o.drawImage(chart, 153, 125, 300, 180, mask="auto")
            if pagenum == 6:
                chart = ImageReader("report_images//COACH" + f"{s+1}.png")
                o.drawImage(chart, 153, 415, 300, 180, mask="auto")
                chart = ImageReader("report_images//INF" + f"{s+1}.png")
                o.drawImage(chart, 153, 130, 300, 180, mask="auto")
            if pagenum == 7:
                chart = ImageReader("report_images//SCTI" + f"{s+1}.png")
                o.drawImage(chart, 153, 407, 300, 180, mask="auto")
            if pagenum == 8:
                chart = ImageReader("report_images//SG" + f"{s+1}.png")
                o.drawImage(chart, 153, 427, 300, 180, mask="auto")
                chart = ImageReader("report_images//EJ" + f"{s+1}.png")
                o.drawImage(chart, 153, 125, 300, 180, mask="auto")
            if pagenum == 9:
                chart = ImageReader("report_images//SD" + f"{s+1}.png")
                o.drawImage(chart, 153, 427, 300, 180, mask="auto")
                chart = ImageReader("report_images//ED" + f"{s+1}.png")
                o.drawImage(chart, 153, 140, 300, 180, mask="auto")
            if pagenum == 10:
                chart = ImageReader("report_images//HG" + f"{s+1}.png")
                o.drawImage(chart, 153, 410, 300, 180, mask="auto")
            if pagenum == 11:
                chart = ImageReader("report_images//VL" + f"{s+1}.png")
                o.drawImage(chart, 153, 430, 300, 180, mask="auto")
                chart = ImageReader("report_images//MBL" + f"{s+1}.png")
                o.drawImage(chart, 153, 133, 300, 180, mask="auto")
            if pagenum == 13:
                o.drawImage(logo, 365.3, 65, 185, 54, mask="auto", preserveAspectRatio=True )
            if pagenum == 14:
                chart = ImageReader("report_images//SAFE" + f"{s+1}.png")
                o.drawImage(chart, 53, 427, 250, 150, mask="auto")
                chart = ImageReader("report_images//ITT" + f"{s+1}.png")
                o.drawImage(chart, 308, 427, 250, 150, mask="auto")
            if pagenum == 15:
                chart = ImageReader("report_images//KS" + f"{s+1}.png")
                o.drawImage(chart, 180, 450, 250, 150, mask="auto")
                chart = ImageReader("report_images//IE" + f"{s+1}.png")
                o.drawImage(chart, 153, 130, 300, 180, mask="auto")
            if pagenum == 16:
                chart = ImageReader("report_images//NET" + f"{s+1}.png")
                o.drawImage(chart, 153, 422, 300, 180, mask="auto")
                chart = ImageReader("report_images//II" + f"{s+1}.png")
                o.drawImage(chart, 153, 130, 300, 180, mask="auto")
            if pagenum == 17:
                chart = ImageReader("report_images//SAS" + f"{s+1}.png")
                o.drawImage(chart, 153, 422, 300, 180, mask="auto")
                chart = ImageReader("report_images//ASN" + f"{s+1}.png")
                o.drawImage(chart, 153, 130, 300, 180, mask="auto")
            if pagenum == 18:
                chart = ImageReader("report_images//COOP" + f"{s+1}.png")
                o.drawImage(chart, 153, 427, 300, 180, mask="auto")
            if pagenum == 19:
                chart = ImageReader("report_images//TMX" + f"{s+1}.png")
                o.drawImage(chart, 153, 420, 300, 180, mask="auto")
                chart = ImageReader("report_images//SL" + f"{s+1}.png")
                o.drawImage(chart, 180, 135, 250, 150, mask="auto")
            if pagenum == 20:
                chart = ImageReader("report_images//CRE" + f"{s+1}.png")
                o.drawImage(chart, 153, 427, 300, 180, mask="auto")
            if pagenum == 22:
                o.drawImage(logo, 365.3, 78, 185, 54, mask="auto", preserveAspectRatio=True )
            if pagenum == 23:
                chart = ImageReader("report_images//RTCRS" + f"{s+1}.png")
                o.drawImage(chart, 53, 427, 250, 150, mask="auto")
                chart = ImageReader("report_images//RTCER" + f"{s+1}.png")
                o.drawImage(chart, 308, 427, 250, 150, mask="auto")
            if pagenum == 24:
                chart = ImageReader("report_images//PT" + f"{s+1}.png")
                o.drawImage(chart, 53, 435, 250, 150, mask="auto")
                chart = ImageReader("report_images//PP" + f"{s+1}.png")
                o.drawImage(chart, 308, 435, 250, 150, mask="auto")
            if pagenum == 25:
                chart = ImageReader("report_images//EISE" + f"{s+1}.png")
                o.drawImage(chart, 53, 442, 250, 150, mask="auto")
                chart = ImageReader("report_images//EIOE" + f"{s+1}.png")
                o.drawImage(chart, 308, 442, 250, 150, mask="auto")
                chart = ImageReader("report_images//EIUE" + f"{s+1}.png")
                o.drawImage(chart, 53, 170, 250, 150, mask="auto")
                chart = ImageReader("report_images//EIRE" + f"{s+1}.png")
                o.drawImage(chart, 308, 170, 250, 150, mask="auto")
            if pagenum == 26:
                chart = ImageReader("report_images//Bel" + f"{s+1}.png")
                o.drawImage(chart, 53, 407, 250, 150, mask="auto")
                chart = ImageReader("report_images//Uniq" + f"{s+1}.png")
                o.drawImage(chart, 308, 407, 250, 150, mask="auto")
            if pagenum == 27:
                chart = ImageReader("report_images//ALT" + f"{s+1}.png")
                o.drawImage(chart, 53, 442, 250, 150, mask="auto")
                chart = ImageReader("report_images//PAY" + f"{s+1}.png")
                o.drawImage(chart, 308, 442, 250, 150, mask="auto")
                chart = ImageReader("report_images//REL" + f"{s+1}.png")
                o.drawImage(chart, 53, 170, 250, 150, mask="auto")
                chart = ImageReader("report_images//SEC" + f"{s+1}.png")
                o.drawImage(chart, 308, 170, 250, 150, mask="auto")
            if pagenum == 28:
                chart = ImageReader("report_images//AUTH" + f"{s+1}.png")
                o.drawImage(chart, 53, 445, 250, 150, mask="auto")
                chart = ImageReader("report_images//VAR" + f"{s+1}.png")
                o.drawImage(chart, 308, 445, 250, 150, mask="auto")
                chart = ImageReader("report_images//AUTO" + f"{s+1}.png")
                o.drawImage(chart, 53, 170, 250, 150, mask="auto")
                chart = ImageReader("report_images//PRES" + f"{s+1}.png")
                o.drawImage(chart, 308, 170, 250, 150, mask="auto")
            if pagenum == 29:
                text_object = o.beginText()
                text_object.setTextOrigin(55, 660)
                text_object.setFont("Helvetica", 11)

                for each in feedback_list[0]:
                    if len(each) > 3:
                        words = each.split()
                        line = ["○"]
                        for word in words:
                            test_line = " ".join(line + [word])
                            if o.stringWidth(test_line, "Helvetica", 11) < 500:
                                line.append(word)
                            else:
                                text_object.textLine(" ".join(line))
                                line = [word]
                        if line:
                            text_object.textLine(" ".join(line))
                o.drawText(text_object)

            if pagenum == 30:
                text_object = o.beginText()
                text_object.setTextOrigin(55, 660)
                text_object.setFont("Helvetica", 11)

                for each in feedback_list[1]:
                    if len(each) > 3:
                        words = each.split()
                        line = ["○"]
                        for word in words:
                            test_line = " ".join(line + [word])
                            if o.stringWidth(test_line, "Helvetica", 11) < 500:
                                line.append(word)
                            else:
                                text_object.textLine(" ".join(line))
                                line = [word]
                        if line:
                            text_object.textLine(" ".join(line))
                o.drawText(text_object)

            if pagenum == 31:
                text_object = o.beginText()
                text_object.setTextOrigin(55, 660)
                text_object.setFont("Helvetica", 11)

                for each in feedback_list[2]:
                    if len(each) > 3:
                        words = each.split()
                        line = ["○"]
                        for word in words:
                            test_line = " ".join(line + [word])
                            if o.stringWidth(test_line, "Helvetica", 11) < 500:
                                line.append(word)
                            else:
                                text_object.textLine(" ".join(line))
                                line = [word]
                        if line:
                            text_object.textLine(" ".join(line))
                o.drawText(text_object)
            
            if pagenum == 33:
                o.drawImage(white_logo, 422.5, 56.8, 115, 35, mask="auto", preserveAspectRatio=True )
            
            o.setFont("Helvetica", 10)
            if pagenum != 33:
                o.drawString(510 - o.stringWidth(name.split('.')[1]), 34.4, name.split('.')[1])

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

        writer.write("workbook_reports//"+f"{savename}"+".pdf")
        shutil.rmtree("report_images//")
        os.remove("data_overlay.pdf")

    os.remove("combined_cleaned.csv")
    os.remove("feedback_cleaned.csv")
