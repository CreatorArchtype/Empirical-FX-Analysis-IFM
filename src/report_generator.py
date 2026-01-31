"""
Report generation module for International Finance Analysis Project
Creates PDF reports and PowerPoint presentations
"""

import os
from typing import List, Optional, Dict

# Try importing reportlab for PDF generation
try:
    from reportlab.lib.pagesizes import A4, letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
    from reportlab.lib import colors as rl_colors
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False
    print("WARNING: reportlab not installed. PDF generation will be unavailable.")
    print("Install with: pip install reportlab")

# Try importing python-pptx for PowerPoint generation
try:
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.enum.text import PP_ALIGN
    from pptx.dml.color import RGBColor
    PPTX_AVAILABLE = True
except ImportError:
    PPTX_AVAILABLE = False
    print("WARNING: python-pptx not installed. PowerPoint generation will be unavailable.")
    print("Install with: pip install python-pptx")


class PDFReportGenerator:
    """Generate PDF reports for Korea-Switzerland finance analysis"""
    
    def __init__(self, filename: str):
        """
        Initialize PDF report generator
        
        Args:
            filename: Path to save PDF file
        
        Example:
            >>> pdf = PDFReportGenerator('outputs/reports/Korea_Switzerland_Analysis.pdf')
            >>> pdf.add_title("South Korea - Switzerland Currency Analysis")
            >>> pdf.build()
        """
        if not REPORTLAB_AVAILABLE:
            raise ImportError("reportlab is required for PDF generation. Install with: pip install reportlab")
        
        self.filename = filename
        self.doc = SimpleDocTemplate(filename, pagesize=A4,
                                     rightMargin=72, leftMargin=72,
                                     topMargin=72, bottomMargin=18)
        self.styles = getSampleStyleSheet()
        self.story = []
        
        # Custom styles
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=rl_colors.HexColor('#2c3e50'),
            spaceAfter=30,
            alignment=1,  # Center
            fontName='Helvetica-Bold'
        )
        
        self.heading_style = ParagraphStyle(
            'CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=rl_colors.HexColor('#34495e'),
            spaceAfter=12,
            spaceBefore=20,
            fontName='Helvetica-Bold'
        )
        
        self.subheading_style = ParagraphStyle(
            'CustomSubheading',
            parent=self.styles['Heading3'],
            fontSize=13,
            textColor=rl_colors.HexColor('#34495e'),
            spaceAfter=10,
            spaceBefore=15,
            fontName='Helvetica-Bold'
        )
        
        self.body_style = ParagraphStyle(
            'CustomBody',
            parent=self.styles['BodyText'],
            fontSize=11,
            leading=16,
            textColor=rl_colors.HexColor('#2c3e50'),
            spaceAfter=12,
            alignment=4  # Justify
        )
    
    def add_title(self, title_text: str):
        """Add report title"""
        title = Paragraph(title_text, self.title_style)
        self.story.append(title)
        self.story.append(Spacer(1, 0.2*inch))
    
    def add_heading(self, heading_text: str):
        """Add section heading"""
        heading = Paragraph(heading_text, self.heading_style)
        self.story.append(heading)
        self.story.append(Spacer(1, 0.1*inch))
    
    def add_subheading(self, subheading_text: str):
        """Add subsection heading"""
        subheading = Paragraph(subheading_text, self.subheading_style)
        self.story.append(subheading)
        self.story.append(Spacer(1, 0.08*inch))
    
    def add_paragraph(self, text: str):
        """Add paragraph text"""
        # Replace newlines with <br/> for reportlab
        text = text.replace('\n', '<br/>')
        para = Paragraph(text, self.body_style)
        self.story.append(para)
        self.story.append(Spacer(1, 0.12*inch))
    
    def add_image(self, image_path: str, width: Optional[float] = None, caption: Optional[str] = None):
        """Add image with optional caption"""
        if width is None:
            width = 5*inch
        if os.path.exists(image_path):
            img = Image(image_path, width=width)
            self.story.append(img)
            if caption:
                caption_style = ParagraphStyle(
                    'Caption',
                    parent=self.styles['BodyText'],
                    fontSize=10,
                    textColor=rl_colors.HexColor('#7f8c8d'),
                    alignment=1  # Center
                )
                self.story.append(Paragraph(caption, caption_style))
            self.story.append(Spacer(1, 0.2*inch))
        else:
            self.add_paragraph(f"<i>[Image not found: {image_path}]</i>")
    
    def add_table(self, data: List[List[str]], col_widths: Optional[List] = None):
        """Add table"""
        table = Table(data, colWidths=col_widths)
        table.setStyle(TableStyle([
            # Header row styling
            ('BACKGROUND', (0, 0), (-1, 0), rl_colors.HexColor('#3498db')),
            ('TEXTCOLOR', (0, 0), (-1, 0), rl_colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 0), (-1, 0), 12),
            
            # Data rows styling
            ('BACKGROUND', (0, 1), (-1, -1), rl_colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), rl_colors.HexColor('#2c3e50')),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            
            # Grid
            ('GRID', (0, 0), (-1, -1), 1, rl_colors.black),
            ('LINEBELOW', (0, 0), (-1, 0), 2, rl_colors.HexColor('#2c3e50')),
        ]))
        self.story.append(table)
        self.story.append(Spacer(1, 0.2*inch))
    
    def add_page_break(self):
        """Add page break"""
        self.story.append(PageBreak())
    
    def build(self):
        """Build the PDF document"""
        self.doc.build(self.story)
        print(f"PDF report generated: {self.filename}")


class PPTXReportGenerator:
    """Generate PowerPoint presentations for Korea-Switzerland finance analysis"""
    
    def __init__(self, filename: str):
        """
        Initialize PowerPoint report generator
        
        Args:
            filename: Path to save PPTX file
        
        Example:
            >>> pptx = PPTXReportGenerator('outputs/presentations/Korea_Switzerland.pptx')
            >>> pptx.add_title_slide("Korea-Switzerland Analysis", "KRW/CHF Currency Study")
            >>> pptx.save()
        """
        if not PPTX_AVAILABLE:
            raise ImportError("python-pptx is required for PowerPoint generation. Install with: pip install python-pptx")
        
        self.filename = filename
        self.prs = Presentation()
        self.prs.slide_width = Inches(10)
        self.prs.slide_height = Inches(7.5)
        
        # Color scheme
        self.colors = {
            'title': RGBColor(44, 62, 80),       # Dark blue-gray
            'accent': RGBColor(52, 152, 219),    # Blue
            'positive': RGBColor(39, 174, 96),   # Green
            'negative': RGBColor(231, 76, 60)    # Red
        }
    
    def add_title_slide(self, title: str, subtitle: str):
        """Add title slide"""
        slide_layout = self.prs.slide_layouts[0]  # Title slide layout
        slide = self.prs.slides.add_slide(slide_layout)
        
        title_shape = slide.shapes.title
        subtitle_shape = slide.placeholders[1]
        
        title_shape.text = title
        subtitle_shape.text = subtitle
        
        # Style title
        title_frame = title_shape.text_frame
        title_frame.paragraphs[0].font.size = Pt(44)
        title_frame.paragraphs[0].font.bold = True
        title_frame.paragraphs[0].font.color.rgb = self.colors['title']
        
        # Style subtitle
        subtitle_frame = subtitle_shape.text_frame
        subtitle_frame.paragraphs[0].font.size = Pt(24)
        subtitle_frame.paragraphs[0].font.color.rgb = self.colors['accent']
    
    def add_content_slide(self, title: str, content_points: List[str]):
        """
        Add content slide with bullet points
        
        Args:
            title: Slide title
            content_points: List of bullet points
        
        Example:
            >>> pptx.add_content_slide(
            ...     "Key Findings",
            ...     ["KRW depreciated 7.46%", "Exporters benefit", "Importers face pressure"]
            ... )
        """
        slide_layout = self.prs.slide_layouts[1]  # Title and content
        slide = self.prs.slides.add_slide(slide_layout)
        
        title_shape = slide.shapes.title
        body_shape = slide.placeholders[1]
        
        title_shape.text = title
        
        # Style title
        title_frame = title_shape.text_frame
        title_frame.paragraphs[0].font.size = Pt(32)
        title_frame.paragraphs[0].font.bold = True
        title_frame.paragraphs[0].font.color.rgb = self.colors['title']
        
        # Add bullet points
        text_frame = body_shape.text_frame
        text_frame.clear()  # Clear default text
        
        for i, point in enumerate(content_points):
            p = text_frame.add_paragraph() if i > 0 else text_frame.paragraphs[0]
            p.text = point
            p.level = 0
            p.font.size = Pt(18)
            p.font.color.rgb = RGBColor(44, 62, 80)
            p.space_before = Pt(12)
    
    def add_image_slide(self, title: str, image_path: str, caption: Optional[str] = None):
        """
        Add slide with image
        
        Args:
            title: Slide title
            image_path: Path to image file
            caption: Optional image caption
        """
        slide_layout = self.prs.slide_layouts[5]  # Blank layout
        slide = self.prs.slides.add_slide(slide_layout)
        
        # Add title
        title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(9), Inches(0.6))
        title_frame = title_box.text_frame
        title_frame.text = title
        title_frame.paragraphs[0].font.size = Pt(32)
        title_frame.paragraphs[0].font.bold = True
        title_frame.paragraphs[0].font.color.rgb = self.colors['title']
        
        # Add image
        if os.path.exists(image_path):
            left = Inches(1)
            top = Inches(1.2)
            width = Inches(8)
            slide.shapes.add_picture(image_path, left, top, width=width)
            
            # Add caption if provided
            if caption:
                caption_box = slide.shapes.add_textbox(Inches(1), Inches(6.5), Inches(8), Inches(0.5))
                caption_frame = caption_box.text_frame
                caption_frame.text = caption
                caption_frame.paragraphs[0].font.size = Pt(14)
                caption_frame.paragraphs[0].font.italic = True
                caption_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
        else:
            # Add placeholder text
            text_box = slide.shapes.add_textbox(Inches(2), Inches(3), Inches(6), Inches(1))
            text_frame = text_box.text_frame
            text_frame.text = f"[Image not found: {image_path}]"
            text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
    
    def add_table_slide(self, title: str, data: List[List[str]]):
        """
        Add slide with table
        
        Args:
            title: Slide title
            data: 2D list of table data (first row is header)
        """
        slide_layout = self.prs.slide_layouts[5]  # Blank
        slide = self.prs.slides.add_slide(slide_layout)
        
        # Add title
        title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(9), Inches(0.6))
        title_frame = title_box.text_frame
        title_frame.text = title
        title_frame.paragraphs[0].font.size = Pt(28)
        title_frame.paragraphs[0].font.bold = True
        title_frame.paragraphs[0].font.color.rgb = self.colors['title']
        
        # Add table
        rows = len(data)
        cols = len(data[0])
        
        left = Inches(1)
        top = Inches(1.5)
        width = Inches(8)
        height = Inches(4.5)
        
        table = slide.shapes.add_table(rows, cols, left, top, width, height).table
        
        # Populate and style table
        for i, row in enumerate(data):
            for j, cell_value in enumerate(row):
                cell = table.cell(i, j)
                cell.text = str(cell_value)
                
                # Style header row
                if i == 0:
                    cell.fill.solid()
                    cell.fill.fore_color.rgb = self.colors['accent']
                    paragraph = cell.text_frame.paragraphs[0]
                    paragraph.font.bold = True
                    paragraph.font.size = Pt(14)
                    paragraph.font.color.rgb = RGBColor(255, 255, 255)
                else:
                    paragraph = cell.text_frame.paragraphs[0]
                    paragraph.font.size = Pt(12)
                    paragraph.font.color.rgb = RGBColor(44, 62, 80)
    
    def add_two_column_slide(self, title: str, left_content: List[str], right_content: List[str]):
        """
        Add slide with two columns of content
        
        Args:
            title: Slide title
            left_content: Bullet points for left column
            right_content: Bullet points for right column
        """
        slide_layout = self.prs.slide_layouts[5]  # Blank
        slide = self.prs.slides.add_slide(slide_layout)
        
        # Add title
        title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(9), Inches(0.6))
        title_frame = title_box.text_frame
        title_frame.text = title
        title_frame.paragraphs[0].font.size = Pt(28)
        title_frame.paragraphs[0].font.bold = True
        title_frame.paragraphs[0].font.color.rgb = self.colors['title']
        
        # Left column
        left_box = slide.shapes.add_textbox(Inches(0.5), Inches(1.5), Inches(4.5), Inches(5.5))
        left_frame = left_box.text_frame
        left_frame.word_wrap = True
        
        for i, point in enumerate(left_content):
            p = left_frame.add_paragraph() if i > 0 else left_frame.paragraphs[0]
            p.text = "• " + point
            p.font.size = Pt(16)
            p.space_before = Pt(10)
        
        # Right column
        right_box = slide.shapes.add_textbox(Inches(5.2), Inches(1.5), Inches(4.5), Inches(5.5))
        right_frame = right_box.text_frame
        right_frame.word_wrap = True
        
        for i, point in enumerate(right_content):
            p = right_frame.add_paragraph() if i > 0 else right_frame.paragraphs[0]
            p.text = "• " + point
            p.font.size = Pt(16)
            p.space_before = Pt(10)
    
    def save(self):
        """Save presentation to file"""
        self.prs.save(self.filename)
        print(f"PowerPoint presentation generated: {self.filename}")


# Excel export function (simple wrapper around pandas)
def export_to_excel(dataframes: Dict[str, 'pd.DataFrame'], filename: str):
    """
    Export multiple DataFrames to Excel with separate sheets
    
    Args:
        dataframes: Dict mapping sheet names to DataFrames
        filename: Path to save Excel file
    
    Example:
        >>> import pandas as pd
        >>> data = {
        ...     'Exchange Rates': forex_df,
        ...     'Analysis Summary': summary_df
        ... }
        >>> export_to_excel(data, 'outputs/excel/korea_switzerland_data.xlsx')
    """
    try:
        import pandas as pd
        
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            for sheet_name, df in dataframes.items():
                df.to_excel(writer, sheet_name=sheet_name)
        
        print(f"Excel file generated: {filename}")
    except ImportError:
        print("ERROR: pandas or openpyxl not installed. Excel export unavailable.")
        print("Install with: pip install pandas openpyxl")


if __name__ == "__main__":
    # Test the module
    print("Testing report_generator.py module...\n")
    
    if REPORTLAB_AVAILABLE:
        print("1. Testing PDF generation...")
        pdf = PDFReportGenerator('outputs/reports/test_report.pdf')
        pdf.add_title("Test Report: Korea-Switzerland Analysis")
        pdf.add_heading("Section 1: Introduction")
        pdf.add_paragraph("This is a test paragraph for the PDF report generator.")
        pdf.add_subheading("Subsection 1.1")
        pdf.add_paragraph("More detailed information goes here.")
        
        # Add sample table
        table_data = [
            ['Metric', 'Value'],
            ['Historical Rate', '0.00067'],
            ['Current Rate', '0.00062'],
            ['Change', '-7.46%']
        ]
        pdf.add_table(table_data)
        pdf.build()
    
    if PPTX_AVAILABLE:
        print("\n2. Testing PowerPoint generation...")
        pptx = PPTXReportGenerator('outputs/presentations/test_presentation.pptx')
        pptx.add_title_slide("Korea-Switzerland Analysis", "Currency Study")
        pptx.add_content_slide("Key Findings", [
            "KRW depreciated by 7.46%",
            "Exporters benefit from cheaper goods",
            "Importers face margin pressure"
        ])
        pptx.save()
    
    print("\nReport generator tests complete!")
