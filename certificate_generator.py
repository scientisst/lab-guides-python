import sys
import os
from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
import pandas as pd

script_path = sys.argv[0]
project_path, _ = os.path.split(script_path)
resources_path = os.path.join(project_path, 'resources')

certificates_path = os.path.join(project_path, 'certificates')

certificate_template_path = os.path.join(certificates_path, 'certificate_template.pdf')
participant_list_path = os.path.join(certificates_path, 'Participant_list.xlsx')

df_participants = pd.read_excel(participant_list_path)

print("processing participant...")

for index, row in df_participants.iterrows():
    f_name = row['First names']
    s_name = row['Second names']

    print(f_name, s_name)

    output_filename = '{}_{}_certificate.pdf'.format(f_name, s_name)
    output_file_path = os.path.join(certificates_path, output_filename)

    existing_pdf = PdfFileReader(open(certificate_template_path, "rb"))
    output = PdfFileWriter()
    # add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.pages[0]

    page_width, page_height = existing_pdf.pages[0].mediaBox.upperRight

    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=(page_width, page_height))# letter)
    can.setFont("Helvetica-Bold", 30)

    # TODO: choose the coordinates for inserting centered text here
    x = int(can._pagesize[0] / 2) # half way horizontally
    y = 300 # custom to 300 (by trial and error)

    can.drawCentredString(x, y, "{} {}".format(f_name, s_name))
    can.save()

    # create a new PDF with Reportlab
    new_pdf = PdfFileReader(packet)

    packet.seek(0)

    page.merge_page(new_pdf.pages[0])
    output.add_page(page)

    # write "output" to a file
    output_stream = open(output_file_path, "wb")

    output.write(output_stream)
    output_stream.close()

