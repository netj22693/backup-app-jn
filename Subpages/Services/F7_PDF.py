import streamlit as st
from io import BytesIO

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm

def create_pdf(data, selected_transport):
    
    styles = getSampleStyleSheet()

    # Defining of styles
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
        spaceAfter=3
    )

    spaced_style_detail_sub = ParagraphStyle(
        'Sub', 
        parent=normal_style,
        fontSize=10,
        leading=14,
        spaceAfter=3,
        leftIndent=10, 
        firstLineIndent=0)

    # Create PDF - buffer
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)

    content = []

    # Logo
    if selected_transport == 'Truck':
        logo = Image("Pictures/Function_7/F7_pdf_logo_png/F7_pdf_logo_truck_v1.png", width=27.4, height=20)   

    if selected_transport == 'Train':
        logo = Image("Pictures/Function_7/F7_pdf_logo_png/F7_pdf_logo_train_v3.png", width=20, height=23.6)
    
    if selected_transport == 'Airplane':
        logo = Image("Pictures/Function_7/F7_pdf_logo_png/F7_pdf_logo_air_v1.png", width=20, height=20)

    header_table = Table(
        [[Paragraph("Offer Summary", title_style), logo]],
        colWidths=[160*mm, 20*mm]
    )
    header_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),  
        ('ALIGN', (1,0), (1,0), 'RIGHT'),      # logo allignment to the RIGHT
        ('BOTTOMPADDING', (0,0), (-1,-1), 0)
    ]))
    content.append(header_table)
    content.append(Spacer(1, 5*mm))

    # Content
    content.append(Paragraph(f"<b>Offer number:</b> {data['offer_id']}", spaced_style))
    content.append(Paragraph(f"<b>Offer created:</b> {data['europe_date_part']} - {data['europe_time_part']} - {data['time_zone']}", spaced_style))
    content.append(Paragraph(f"<b>Customer to approve till:</b> {data['customer_approve_date']} - {data['customer_approve_time']} - {data['time_zone']} ({data['agreed_till_str']})", spaced_style))

    content.append(Spacer(1, 5*mm))

    # Line ----
    table = Table([[""]], colWidths=[180*mm], rowHeights=[1])
    table.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), colors.black)]))
    content.append(table)
    content.append(Spacer(1, 5*mm))

    # Delivery 
    content.append(Paragraph(f"<b>Delivery from {data['from_city']} ({data['from_country']}) to {data['to_city']} ({data['to_country']}):</b>", bold_style))
    content.append(Paragraph(f"• Costs: {data['distance_cost']:,.2f} {data['currency']}", spaced_style_detail))
    content.append(Paragraph(f"• Distance: {data['distance_length']:,.2f} km", spaced_style_detail))
    content.append(Paragraph(f"• Time to cover the distance: {data['distance_time']:,.2f} hour(s)", spaced_style_detail))
    content.append(Paragraph(f"• Transport type: {data['selected_transport']}", spaced_style_detail))

    content.append(Spacer(1, 5*mm))

    # DTD
    content.append(Paragraph("<b>Door-to-Door:</b>", bold_style))
    content.append(Paragraph(f"• Additional: {(data['from_dtd'] + data['to_dtd']):,.2f} km", spaced_style_detail))
    content.append(Paragraph(f"• {data['from_city']}: {data['from_dtd']:,.2f} km", spaced_style_detail_sub))
    content.append(Paragraph(f"• {data['to_city']}: {data['to_dtd']:,.2f} km", spaced_style_detail_sub))
    content.append(Paragraph(f"• Time to cover the Door-to-Door: {data['dtd_time']:,.2f} hour(s)", spaced_style_detail))

    if selected_transport == 'Train' or selected_transport == 'Airplane':
        content.append(Paragraph(f"• Transfer {data['selected_transport']} ↔ Truck: {(data['shipment_transfer_dtd_from'] + data['shipment_transfer_dtd_to']):,.2f} hour(s)", spaced_style_detail_sub))      
        content.append(Paragraph(f"• Time for Truck ride: {data['dtd_truck_if_not_truck_main']:,.2f} hour(s)", spaced_style_detail_sub))  

    content.append(Spacer(1, 5*mm))

    content.append(Paragraph(f"<b>{data['selected_transport']}:</b>", bold_style))
    content.append(Paragraph(f"• <b>{data['service']}</b> service requires {data['service_time']:,.2f} hours for administration and loading.", spaced_style_detail))
    
    if selected_transport == 'Truck':
        content.append(Paragraph(f"• Mandatory breaks for driver (including Door-to-Door time): {data['truck_breaks']:,.2f} hour(s)", spaced_style_detail))
    
    content.append(Spacer(1, 4*mm))
    content.append(Paragraph(f"<b>Overall time end-to-end delivery:</b> {data['time_overall']:,.2f} hours", bold_style))

    content.append(Spacer(1, 2*mm))
    content.append(Paragraph(f"<b>Expected delivery:</b> {data['expected_delivery']} - {data['time_zone']}", summary_style))

    content.append(Spacer(1, 5*mm))

    # Line ----
    table2 = Table([[""]], colWidths=[180*mm], rowHeights=[1])
    table2.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), colors.black)]))
    content.append(table2)

    content.append(Spacer(1, 5*mm))

    # Costs
    content.append(Paragraph("<b>Additional services - costs:</b>", bold_style))
    content.append(Paragraph(f"• Insurance: {data['insurance']:,.2f} {data['currency']}", spaced_style_detail))
    content.append(Paragraph(f"• Fragile goods: {data['fragile']:,.2f} {data['currency']}", spaced_style_detail))
    content.append(Paragraph(f"• Danger goods: {data['danger']:,.2f} {data['currency']}", spaced_style_detail))
    content.append(Paragraph(f"• Door-To-Door {data['from_city']}: {data['dtd_from']:,.2f} {data['currency']}", spaced_style_detail))
    content.append(Paragraph(f"• Door-To-Door {data['to_city']}: {data['dtd_to']:,.2f} {data['currency']}", spaced_style_detail))

    content.append(Spacer(1, 5*mm))

    # Line ----
    table2 = Table([[""]], colWidths=[180*mm], rowHeights=[1])
    table2.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), colors.black)]))
    content.append(table2)

    content.append(Spacer(1, 5*mm))
    content.append(Paragraph(f"<b>Final price:</b> {data['final_price']:,.2f} {data['currency']}", summary_style))

    # Creating of PDF
    doc.build(content)
    pdf_file = buffer.getvalue()

    return pdf_file


# ===== FOR TESTING PURPOSES AS ISOLATED UNIT  =====
# TEST 
# offer_number_generated = "F7-5555555"
# europe_date_part = "06-Dec-25"
# europe_time_part = "12:04"
# cet_cest_now= "CET"
# offer_id = "F7-101"
# customer_approve_date = "11-Dec-25"
# customer_approve_time = "12:05"
# agreed_till_str = "5 days"
# selected_transport = "Train"
# urgency = "Standard"
# cet_cest_now = "CET"
# overall_time_truck = 38.42
# delivery_dt_formated = "Monday - 15-Dec-25 by 10:00"
# final_price = 27513.23
# selected_currency = "korunka"
# overall_time_db = 25.67
# country_code_from = "AT"
# from_city = "Prahahaha"
# from_city_extra_doortdoor = 10
# country_code_to = "DE"
# to_city = "Würzburg"
# to_city_extra_doortdoor = 20
# distance = 888.88
# time_journey = 12.12
# time_dtd = 14
# price = 111111.11
# door_from_result = 22.11
# door_to_result = 33.11
# shipment_value = 444.55
# money_insurance = 666.66
# money_fragile = 777.77
# money_danger = 888.88
# time_break = 1.17
# transfer_time_from = 1
# transfer_time_to = 2
# truck_time_dtd_air_train_from = 3
# truck_time_dtd_air_train_to = 4
# extra_time = 32

# data_for_pdf = {
#     "offer_id" : offer_number_generated,
#     "europe_date_part" : europe_date_part, 
#     "europe_time_part" : europe_time_part, 
#     "customer_approve_date":customer_approve_date,
#     "customer_approve_time" : customer_approve_time,
#     "agreed_till_str": agreed_till_str,
#     "selected_transport" : selected_transport,
#     "service" : urgency,
#     "service_time": extra_time,
#     "time_zone" : cet_cest_now,
#     "time_overall" : overall_time_db,
#     "expected_delivery" : delivery_dt_formated,
#     "final_price" : final_price,
#     "currency" : selected_currency,
#     "from_country" : country_code_from,
#     "from_city" : from_city,
#     "from_dtd" : from_city_extra_doortdoor,
#     "to_country" : country_code_to,
#     "to_city" : to_city,
#     "to_dtd" : to_city_extra_doortdoor,
#     "distance_length" : distance,
#     "distance_time" : time_journey,
#     "dtd_time" : time_dtd,
#     "distance_cost" : price,
#     "dtd_from" : door_from_result,
#     "dtd_to" : door_to_result,
#     "shipment_value" : shipment_value,
#     "insurance" : money_insurance,
#     "fragile" : money_fragile,
#     "danger" : money_danger,
#     "truck_breaks" : time_break,
#     "shipment_transfer_dtd_from" : transfer_time_from,
#     "shipment_transfer_dtd_to" : transfer_time_to,
#     "dtd_truck_if_not_truck_main" : (truck_time_dtd_air_train_from + truck_time_dtd_air_train_to)
# }

# pdf = create_pdf(data_for_pdf)

# # Download button ve Streamlitu
# st.download_button(
#     label="Stáhnout PDF",
#     data=pdf,
#     file_name="offer.pdf",
#     mime="application/pdf"
# )
