from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os
from datetime import datetime
from werkzeug.utils import secure_filename
from PIL import Image

class FinalPDFCertificateGenerator:
    def __init__(self):
        self.template_path = 'certificate-templates/raw/certificate-template.png'
        
    def get_image_dimensions(self):
        """Get original image dimensions"""
        if os.path.exists(self.template_path):
            with Image.open(self.template_path) as img:
                return img.size  # (width, height)
        return (1056, 816)  # Your known dimensions
        
    def create_final_certificate(self, student_data, output_path):
        """Create final PDF with perfect positioning"""
        try:
            # Get image dimensions
            img_width, img_height = self.get_image_dimensions()
            
            # Create PDF with exact image dimensions (no stretching!)
            custom_page_size = (img_width, img_height)
            c = canvas.Canvas(output_path, pagesize=custom_page_size)
            
            # Draw image at exact size - NO SCALING
            c.drawImage(self.template_path, 0, 0, width=img_width, height=img_height)
            
            # Add text with YOUR PERFECT coordinates
            c.setFont("Helvetica-Bold", 28)
            c.setFillColorRGB(0, 0, 0)  # Black
            
            # PERFECT POSITIONS (from your testing)
            c.drawString(405, 400, student_data['student_name'].upper())
            
            c.setFont("Helvetica", 18)
            c.drawString(345, 277, str(student_data['batch_start_date']))
            c.drawString(625, 277, str(student_data['batch_end_date']))
            
            # Add certificate metadata
            c.setFont("Helvetica", 12)
            c.drawString(50, 50, f"Batch: {student_data['batch_number']}")
            c.drawString(50, 35, f"SixerClass ID: {student_data['sixerclass_id']}")
            c.drawString(400, 35, f"Issued on: {datetime.now().strftime('%B %d, %Y')}")
            
            # Save perfect PDF
            c.save()
            
            print(f"✅ Final perfect PDF certificate created: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"❌ Final PDF generation error: {e}")
            return None
