# forensic_tool_web/reporting.py

import os
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Table, TableStyle, Frame, PageTemplate
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.lib import colors  # <-- यह लाइन जोड़ दी गई है
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from utils import format_size

class PDFReport:
    def __init__(self, filename, company_name="Cyber Hunter Warrior"):
        self.filename = filename
        self.company_name = company_name
        self.doc = SimpleDocTemplate(
            filename, 
            pagesize=letter,
            topMargin=1.2*inch, 
            bottomMargin=1*inch,
            leftMargin=0.75*inch,
            rightMargin=0.75*inch
        )
        self.story = []
        
        # --- Professional Color Palette (Court-Ready Theme) ---
        self.colors = {
            "header_blue": colors.HexColor('#0D47A1'),   # Deep blue for headers
            "section_blue": colors.HexColor('#003366'),  # Dark blue for section headings
            "dark_text": colors.HexColor('#333333'),     # Dark gray for body text
            "accent_text": colors.HexColor('#004D40'),   # Dark teal for hash values
            "gold_accent": colors.HexColor('#C9A43B'),   # Gold for accents
            "white": colors.HexColor('#FFFFFF'),
            "zebra_stripe": colors.HexColor('#F5F5F5'),  # Light gray for table rows
            "light_gold": colors.HexColor('#F8F4E6'),    # Light gold for background accents
        }

        self._create_styles()

    def _create_styles(self):
        """Creates custom paragraph styles for a professional report."""
        self.styles = getSampleStyleSheet()
        
        # Cover page styles
        self.styles.add(ParagraphStyle(
            name='CoverTitle', 
            fontName='Helvetica-Bold', 
            fontSize=26, 
            textColor=self.colors['section_blue'], 
            alignment=TA_CENTER, 
            spaceAfter=12
        ))
        
        self.styles.add(ParagraphStyle(
            name='CoverSubtitle', 
            fontName='Helvetica', 
            fontSize=14, 
            textColor=self.colors['dark_text'], 
            alignment=TA_CENTER, 
            spaceAfter=24
        ))
        
        self.styles.add(ParagraphStyle(
            name='CoverSectionHeader', 
            fontName='Helvetica-Bold', 
            fontSize=16,
            textColor=self.colors['dark_text'], 
            alignment=TA_CENTER, 
            spaceAfter=14
        ))
        
        self.styles.add(ParagraphStyle(
            name='PoweredBy', 
            fontName='Helvetica-Oblique', 
            fontSize=10, 
            textColor=self.colors['dark_text'], 
            alignment=TA_CENTER
        ))

        # Document styles
        self.styles.add(ParagraphStyle(
            name='SectionHeader', 
            fontName='Helvetica-Bold', 
            fontSize=14, 
            textColor=self.colors['section_blue'], 
            alignment=TA_LEFT, 
            spaceAfter=14, 
            spaceBefore=12,
            borderPadding=5,
            borderColor=self.colors['gold_accent'],
            borderWidth=1,
            backColor=self.colors['light_gold']
        ))
        
        self.styles.add(ParagraphStyle(
            name='SubsectionHeader', 
            fontName='Helvetica-Bold', 
            fontSize=12, 
            textColor=self.colors['section_blue'], 
            alignment=TA_LEFT, 
            spaceAfter=8, 
            spaceBefore=10
        ))
        
        self.styles.add(ParagraphStyle(
            name='Body', 
            fontName='Helvetica', 
            fontSize=10, 
            textColor=self.colors['dark_text'], 
            alignment=TA_JUSTIFY, 
            spaceAfter=6, 
            leading=14
        ))
        
        self.styles.add(ParagraphStyle(
            name='BodyBold', 
            parent=self.styles['Body'], 
            fontName='Helvetica-Bold',
            textColor=colors.black
        ))
        
        self.styles.add(ParagraphStyle(
            name='Mono', 
            fontName='Courier-Bold', 
            fontSize=9, 
            textColor=self.colors['accent_text'], 
            alignment=TA_LEFT
        ))
        
        self.styles.add(ParagraphStyle(
            name='Footer', 
            fontName='Helvetica', 
            fontSize=8, 
            textColor=colors.grey, 
            alignment=TA_CENTER
        ))

    def _header_footer(self, canvas, doc):
        """Adds a professional header and footer with company name, rights reserved, and page number."""
        canvas.saveState()
        
        # Header
        canvas.setFont('Helvetica-Bold', 10)
        canvas.setFillColor(self.colors['section_blue'])
        canvas.drawString(doc.leftMargin, doc.height + doc.topMargin + 0.2*inch, self.company_name)
        
        # Draw a line under the header
        canvas.setStrokeColor(self.colors['gold_accent'])
        canvas.setLineWidth(0.5)
        canvas.line(doc.leftMargin, doc.height + doc.topMargin, doc.width + doc.leftMargin, doc.height + doc.topMargin)
        
        # Footer
        canvas.setFont('Helvetica', 9)
        canvas.setFillColor(colors.grey)
        
        current_year = datetime.now().year
        copyright_text = f"© {current_year} {self.company_name}. All Rights Reserved."
        page_text = f"Page {doc.page}"
        timestamp = f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

        canvas.drawString(doc.leftMargin, doc.bottomMargin - 0.3*inch, copyright_text)
        canvas.drawCentredString(doc.width/2 + doc.leftMargin, doc.bottomMargin - 0.3*inch, timestamp)
        canvas.drawRightString(doc.width + doc.leftMargin, doc.bottomMargin - 0.3*inch, page_text)
        
        # Draw a line above the footer
        canvas.setStrokeColor(self.colors['gold_accent'])
        canvas.setLineWidth(0.5)
        canvas.line(doc.leftMargin, doc.bottomMargin, doc.width + doc.leftMargin, doc.bottomMargin)
        
        canvas.restoreState()

    def generate_cover_page(self, case_metadata):
        """Creates a clean, professional cover page with a styled table."""
        # Add company logo
        logo_path = os.path.join(os.path.dirname(__file__), 'static', 'images', 'logo.png')
        if os.path.exists(logo_path):
            logo = Image(logo_path, width=1.8*inch, height=1.8*inch)
            logo.hAlign = 'CENTER'
            self.story.append(logo)
        else:
            # Fallback to text if logo not available
            self.story.append(Paragraph(self.company_name, self.styles['CoverTitle']))
        
        self.story.append(Spacer(1, 0.3 * inch))
        self.story.append(Paragraph("Forensic Hashing-X Report", self.styles['CoverTitle']))
        self.story.append(Paragraph("Powerd by: Cyber Hunter Warrior", self.styles['CoverSubtitle']))
        self.story.append(Spacer(1, 0.5 * inch))

        # Attractive Table for Case Details
        self.story.append(Paragraph("CASE INFORMATION", self.styles['CoverSectionHeader']))
        
        metadata_table_data = [
            [Paragraph("<b>Investigator Name:</b>", self.styles['BodyBold']), Paragraph(case_metadata["investigator_name"], self.styles['Body'])],
            [Paragraph("<b>Case ID:</b>", self.styles['BodyBold']), Paragraph(case_metadata["case_id"], self.styles['Body'])],
            [Paragraph("<b>Case Description:</b>", self.styles['BodyBold']), Paragraph(case_metadata["case_description"], self.styles['Body'])],
            [Paragraph("<b>Date & Time:</b>", self.styles['BodyBold']), Paragraph(case_metadata["date_time"], self.styles['Body'])]
        ]
        
        table = Table(metadata_table_data, colWidths=[2 * inch, 4.5 * inch])
        table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('BACKGROUND', (0, 0), (0, -1), self.colors['light_gold']), # Label column background
            ('BACKGROUND', (1, 0), (1, -1), self.colors['zebra_stripe']), # Value column background
            ('LINEBELOW', (0, 0), (-1, -1), 1, colors.lightgrey),
            ('BOX', (0,0), (-1,-1), 1.5, self.colors['gold_accent']),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ]))
        self.story.append(table)
        
        self.story.append(Spacer(1, 0.8 * inch))
        
        # Add confidentiality notice
        confidentiality = Paragraph(
            "<i>This document contains confidential information pertaining to an ongoing investigation. "
            "Distribution is restricted to authorized personnel only.</i>", 
            self.styles['Body']
        )
        self.story.append(confidentiality)
        
        self.story.append(Spacer(1, 0.3 * inch))
        self.story.append(PageBreak())

    def add_hashing_results(self, report_data):
        """Adds all hashing results. LOGIC IS UNCHANGED."""
        # Add a brief introduction section
        intro_text = """
        This document presents the cryptographic hash values generated during the forensic examination. 
        Hash functions are used to verify data integrity and authenticity throughout the investigation process. 
        Any alteration to the original data will result in a different hash value, indicating potential tampering.
        """
        self.story.append(Paragraph("Report Overview", self.styles['SectionHeader']))
        self.story.append(Paragraph(intro_text, self.styles['Body']))
        self.story.append(Spacer(1, 0.2*inch))
        
        # This part of the logic remains exactly the same as your original code.
        if report_data.get('text_results'):
            self.story.append(Paragraph("Text Hashing Results", self.styles['SectionHeader']))
            self.story.append(Paragraph(f"<b>Original Text:</b> {report_data['text_results']['text']}", self.styles['Body']))
            self._add_table(report_data['text_results']['hashes'])
            self.story.append(Spacer(1, 0.2*inch))

        if report_data.get('file_results'):
            self.story.append(Paragraph("File Hashing Results", self.styles['SectionHeader']))
            self._add_metadata_table(report_data['file_results']['metadata'])
            self._add_table(report_data['file_results']['hashes'])
            self.story.append(Spacer(1, 0.2*inch))

        if report_data.get('dir_results'):
            self.story.append(Paragraph("Directory Hashing Results", self.styles['SectionHeader']))
            self._add_metadata_table(report_data['dir_results']['summary'], is_summary=True)
            self.story.append(Spacer(1, 0.2*inch))
            for i, item in enumerate(report_data['dir_results']['results']):
                self.story.append(Paragraph(f"File Details: {item['metadata']['File Name']}", self.styles['SubsectionHeader']))
                self._add_metadata_table(item['metadata'])
                self._add_table(item['hashes'])
                self.story.append(Spacer(1, 0.3*inch))
                
        # Add a conclusion section only if there's space on the current page
        # We'll check if we have enough space for the conclusion section
        self.story.append(Paragraph("Investigation Conclusion", self.styles['SectionHeader']))
        conclusion_text = """
        The cryptographic hashing process has been completed for all specified digital evidence. 
        The hash values documented in this report can be used to verify the integrity of the evidence 
        throughout the legal proceedings. Any changes to the original evidence will result in different 
        hash values, indicating potential tampering or corruption.
        """
        self.story.append(Paragraph(conclusion_text, self.styles['Body']))
        self.story.append(Spacer(1, 0.3*inch))
        
        # Add signature fields
        sign_data = [
            ["Investigator Signature:", "________________________", "Date:", "________________________"],
            ["Witness Signature:", "________________________", "Date:", "________________________"]
        ]
        sign_table = Table(sign_data, colWidths=[1.5*inch, 2*inch, 0.8*inch, 2*inch])
        sign_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('VALIGN', (0, 0), (-1, -1), 'BOTTOM'),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (2, 0), (2, -1), 'RIGHT'),
            ('LINEABOVE', (1, 0), (1, 0), 1, colors.black),
            ('LINEABOVE', (3, 0), (3, 0), 1, colors.black),
            ('LINEABOVE', (1, 1), (1, 1), 1, colors.black),
            ('LINEABOVE', (3, 1), (3, 1), 1, colors.black),
            ('TOPPADDING', (0, 0), (-1, -1), 20),
        ]))
        self.story.append(sign_table)

    def _add_metadata_table(self, metadata, is_summary=False):
        """Helper for metadata tables. LOGIC IS UNCHANGED."""
        # This part of the logic remains exactly the same.
        if is_summary:
            data = [
                [Paragraph("<b>Total Files Processed:</b>", self.styles['BodyBold']), Paragraph(str(metadata["Total Files Processed"]), self.styles['Body'])],
                [Paragraph("<b>Total Directory Size:</b>", self.styles['BodyBold']), Paragraph(format_size(metadata["Total Directory Size"]), self.styles['Body'])]
            ]
        else:
             data = [
                [Paragraph("<b>File Name:</b>", self.styles['BodyBold']), Paragraph(metadata["File Name"], self.styles['Body'])],
                [Paragraph("<b>File Size:</b>", self.styles['BodyBold']), f"{metadata['File Size']} bytes ({format_size(metadata['File Size'])})"],
                [Paragraph("<b>File Path:</b>", self.styles['BodyBold']), Paragraph(metadata["File Path"], self.styles['Body'])],
                [Paragraph("<b>Last Modified:</b>", self.styles['BodyBold']), Paragraph(metadata["Last Modified Time"], self.styles['Body'])],
            ]
        
        table = Table(data, colWidths=[1.5 * inch, 5 * inch])
        table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('BACKGROUND', (0, 0), (0, -1), self.colors['light_gold']),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ]))
        self.story.append(table)
        self.story.append(Spacer(1, 0.1*inch))

    def _add_table(self, hashes):
        """Creates a professional, 'animated' table with zebra striping."""
        header = [Paragraph("<b>Algorithm</b>", self.styles['BodyBold']), Paragraph("<b>Hash Value</b>", self.styles['BodyBold'])]
        data = [header]
        
        for alg, h_val in hashes.items():
            data.append([Paragraph(alg, self.styles['Body']), Paragraph(h_val, self.styles['Mono'])])

        table = Table(data, colWidths=[1.5 * inch, 5 * inch])
        
        # Professional Animated Table Style
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.colors['header_blue']),
            ('TEXTCOLOR', (0, 0), (-1, 0), self.colors['white']),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('BOX', (0, 0), (-1, -1), 1, self.colors['gold_accent']),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, self.colors['gold_accent'])
        ])
        
        # Add zebra striping for data rows
        for i in range(1, len(data)):
            if i % 2 != 0: # Odd rows (1, 3, 5...)
                style.add('BACKGROUND', (0, i), (-1, i), self.colors['zebra_stripe'])

        table.setStyle(style)
        self.story.append(table)
        
    def save(self):
        """Saves the PDF. NO CHANGE IN LOGIC HERE."""
        frame = Frame(self.doc.leftMargin, self.doc.bottomMargin, self.doc.width, self.doc.height, id='normal')
        
        content_template = PageTemplate(id='content', frames=[frame], onPage=self._header_footer)
        
        self.doc.addPageTemplates([
            PageTemplate(id='cover', frames=frame),
            content_template
        ])
        
        self.story.insert(0, Paragraph('<page template=cover>'))
        # This is corrected to apply the content template from the second page onwards
        self.story.append(Paragraph('<setnextpage template=content>'))

        self.doc.build(self.story)
