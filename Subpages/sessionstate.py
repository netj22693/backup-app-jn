import streamlit as st
from io import BytesIO

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm

styles = getSampleStyleSheet()

# Styly
title_style = ParagraphStyle(
    'TitleStyle',
    parent=styles['Heading1'],
    fontSize=14,
    leading=20,
    spaceAfter=10,
)

summary_style = ParagraphStyle(
    'TitleStyle',
    parent=styles['Heading1'],
    fontSize=13,
    leading=20,
    spaceAfter=4,
)

bold_style = ParagraphStyle(
    'BoldStyle',
    parent=styles['Normal'],
    fontSize=11,
    leading=16,
    spaceAfter=4,
)

normal_style = styles['Normal']

spaced_style = ParagraphStyle(
    'SpacedStyle',
    parent=normal_style,
    fontSize=11,
    leading=14,
    spaceAfter=3
)

spaced_style_detail = ParagraphStyle(
    'SpacedStyle',
    parent=normal_style,
    fontSize=10,
    leading=14,
    spaceAfter=2
)

# Vytvoření PDF bufferu
buffer = BytesIO()
doc = SimpleDocTemplate(buffer, pagesize=A4)

content = []

# --- Logo vedle "Offer Summary" ---
logo = Image("Pictures/Function_7/F7_pdf_logo_png/F7_pdf_logo_train_v3.png", width=20, height=20)

header_table = Table(
    [[Paragraph("Offer Summary", title_style), logo]],
    colWidths=[160*mm, 20*mm]
)
header_table.setStyle(TableStyle([
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),  # vertikální zarovnání na střed
    ('ALIGN', (1,0), (1,0), 'RIGHT'),      # logo doprava
    ('BOTTOMPADDING', (0,0), (-1,-1), 0)
]))
content.append(header_table)
content.append(Spacer(1, 5*mm))

# --- Zbytek obsahu ---
content.append(Paragraph("<b>Offer number:</b> F7-143", spaced_style))
content.append(Paragraph("<b>Offer created:</b> 07-Dec-25 - 10:07 CET", spaced_style))
content.append(Paragraph("<b>Customer to approve till:</b> 09-Dec-25 - 10:07 CET (2 days)", spaced_style))

content.append(Spacer(1, 4*mm))

# Oddělovací čára
table = Table([[""]], colWidths=[180*mm], rowHeights=[1])
table.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), colors.black)]))
content.append(table)
content.append(Spacer(1, 4*mm))

# Sekce logistika
content.append(Paragraph("<b>Delivery from Graz (AT) to Augsburg (DE):</b>", bold_style))
content.append(Paragraph("• Costs: 1,052.36 euro", spaced_style_detail))
content.append(Paragraph("• Distance: 526.18 km", spaced_style_detail))
content.append(Paragraph("• Time to cover the distance: 7.52 hour(s)", spaced_style_detail))
content.append(Paragraph("• Transport type: Truck", spaced_style_detail))

content.append(Spacer(1, 4*mm))

content.append(Paragraph("<b>Door-to-Door:</b>", bold_style))
content.append(Paragraph("• Additional: 0 km", spaced_style_detail))
content.append(Paragraph("• Time to cover the Door-to-Door: 0.00 hour(s)", spaced_style_detail))

content.append(Spacer(1, 4*mm))

content.append(Paragraph("<b>Truck details:</b>", bold_style))
content.append(Paragraph("• Standard service requires 32.00 hours for administration and loading.", spaced_style_detail))
content.append(Paragraph("• Mandatory breaks: 0.75 hour(s)", spaced_style_detail))

content.append(Spacer(1, 4*mm))
content.append(Paragraph("<b>Overall time end-to-end:</b> 40.27 hours", bold_style))

content.append(Spacer(1, 2*mm))
content.append(Paragraph("<b>Expected delivery:</b> Thursday - 11-Dec-25 by 07:00 CET", summary_style))

content.append(Spacer(1, 4*mm))

# Oddělovací čára
table2 = Table([[""]], colWidths=[180*mm], rowHeights=[1])
table2.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), colors.black)]))
content.append(table2)

content.append(Spacer(1, 4*mm))

# Sekce 3 — ceny
content.append(Paragraph("<b>Additional services - costs:</b>", bold_style))
content.append(Paragraph("• Insurance: 0.00 euro", spaced_style_detail))
content.append(Paragraph("• Fragile goods: 0.00 euro", spaced_style_detail))
content.append(Paragraph("• Danger goods: 0.00 euro", spaced_style_detail))
content.append(Paragraph("• Door-To-Door Graz: 0.00 euro", spaced_style_detail))
content.append(Paragraph("• Door-To-Door Augsburg: 0.00 euro", spaced_style_detail))

content.append(Spacer(1, 4*mm))

# Oddělovací čára
table2 = Table([[""]], colWidths=[180*mm], rowHeights=[1])
table2.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), colors.black)]))
content.append(table2)

content.append(Spacer(1, 4*mm))
content.append(Paragraph("<b>Final price:</b> 1,052.36 euro", summary_style))

# Uložení PDF do bufferu
doc.build(content)
pdf_bytes = buffer.getvalue()

# Download button ve Streamlitu
st.download_button(
    label="Stáhnout PDF",
    data=pdf_bytes,
    file_name="offer.pdf",
    mime="application/pdf"
)
