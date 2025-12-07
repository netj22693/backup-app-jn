import streamlit as st 


from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm

file_name = "offer.pdf"

styles = getSampleStyleSheet()

# Vlastní styly
title_style = ParagraphStyle(
    'TitleStyle',
    parent=styles['Heading1'],
    fontSize=16,
    leading=20,
    spaceAfter=10,
)

bold_style = ParagraphStyle(
    'BoldStyle',
    parent=styles['Normal'],
    fontSize=11,
    leading=14,
    spaceAfter=4,
)

normal_style = styles['Normal']

doc = SimpleDocTemplate(file_name, pagesize=A4)

content = []

# Nadpis
content.append(Paragraph("Offer Summary", title_style))
content.append(Spacer(1, 5*mm))

# Sekce 1 — základní info
content.append(Paragraph("<b>Offer number:</b> F7-143", normal_style))
content.append(Paragraph("<b>Offer created:</b> 07-Dec-25 - 10:07 CET", normal_style))
content.append(Paragraph("<b>Customer to approve till:</b> 09-Dec-25 - 10:07 CET (2 days)", normal_style))

content.append(Spacer(1, 4*mm))

# Linie (oddělovací čára)
table = Table([[""]], colWidths=[180*mm], rowHeights=[1])
table.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), colors.black)]))
content.append(table)
content.append(Spacer(1, 4*mm))

# Sekce 2 — logistika
content.append(Paragraph("<b>Delivery from Graz (AT) to Augsburg (DE):</b>", bold_style))
content.append(Paragraph("Costs: 1,052.36 euro", normal_style))
content.append(Paragraph("Distance: 526.18 km", normal_style))
content.append(Paragraph("Time to cover the distance: 7.52 hour(s)", normal_style))
content.append(Paragraph("Transport type: Truck", normal_style))

content.append(Spacer(1, 4*mm))

content.append(Paragraph("<b>Door-to-Door:</b>", bold_style))
content.append(Paragraph("Additional: 0 km", normal_style))
content.append(Paragraph("Time to cover the Door-to-Door: 0.00 hour(s)", normal_style))

content.append(Spacer(1, 4*mm))

content.append(Paragraph("<b>Truck details:</b>", bold_style))
content.append(Paragraph("Standard service requires 32.00 hours for administration and loading.", normal_style))
content.append(Paragraph("Mandatory breaks: 0.75 hour(s)", normal_style))

content.append(Spacer(1, 4*mm))
content.append(Paragraph("<b>Overall time end-to-end:</b> 40.27 hours", bold_style))

content.append(Spacer(1, 8*mm))
content.append(Paragraph("<b>Expected delivery:</b> Thursday - 11-Dec-25 by 07:00 CET", bold_style))

content.append(Spacer(1, 10*mm))

# Oddělovací čára
table2 = Table([[""]], colWidths=[180*mm], rowHeights=[1])
table2.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), colors.black)]))
content.append(table2)

content.append(Spacer(1, 8*mm))

# Sekce 3 — ceny
content.append(Paragraph("<b>Additional services - costs:</b>", bold_style))
content.append(Paragraph("Insurance: 0.00 euro", normal_style))
content.append(Paragraph("Fragile goods: 0.00 euro", normal_style))
content.append(Paragraph("Danger goods: 0.00 euro", normal_style))
content.append(Paragraph("Door-To-Door Graz: 0.00 euro", normal_style))
content.append(Paragraph("Door-To-Door Augsburg: 0.00 euro", normal_style))

content.append(Spacer(1, 6*mm))
content.append(Paragraph("<b>Final price:</b> 1,052.36 euro", title_style))

# Uložení
doc.build(content)