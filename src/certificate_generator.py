from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os
from datetime import datetime
from PIL import Image

class CertificateGenerator:
    def __init__(self, template_dir=None):
        # Use provided template directory or try to find it
        if template_dir:
            self.template_path = os.path.join(template_dir, 'certificate-template.png')
        else:
            # Try multiple template paths for backward compatibility
            possible_paths = [
                'data/templates/certificate-template.png',
                '../data/templates/certificate-template.png',
                'aws-final-deployment/certificate-templates/raw/certificate-template.png',
                'certificate-templates/raw/certificate-template.png',
                'aws-final-deployment/production/data/certificate-templates/raw/certificate-template.png'
            ]
            
            self.template_path = None
            for path in possible_paths:
                if os.path.exists(path):
                    self.template_path = path
                    break
        
        if not self.template_path or not os.path.exists(self.template_path):
            print("❌ Certificate template not found!")
        else:
            print(f"✅ Using template: {self.template_path}")
    
    def format_date(self, date_str):
        """Convert date to dd-mm-yyyy format"""
        try:
            # Parse the date string (assuming it's in YYYY-MM-DD format)
            if isinstance(date_str, str):
                date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                return date_obj.strftime('%d-%m-%Y')
            return str(date_str)
        except:
            return str(date_str)
        
    def get_image_dimensions(self):
        """Get original image dimensions"""
        if self.template_path and os.path.exists(self.template_path):
            with Image.open(self.template_path) as img:
                return img.size  # (width, height)
        return (1056, 816)  # Default dimensions
        
    def create_certificate(self, student_data, output_path):
        """Create PDF certificate with template overlay"""
        try:
            if not self.template_path:
                print("❌ No template available")
                return False
                
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Get image dimensions
            img_width, img_height = self.get_image_dimensions()
            
            # Create PDF with exact image dimensions
            custom_page_size = (img_width, img_height)
            c = canvas.Canvas(output_path, pagesize=custom_page_size)
            
            # Draw template image at exact size
            c.drawImage(self.template_path, 0, 0, width=img_width, height=img_height)
            
            # Dynamic center alignment for student name
            name_font_size = 32
            c.setFont("Helvetica-Bold", name_font_size)
            c.setFillColorRGB(0, 0, 0)  # Black text
            
            # Define name area boundaries (matching your underlined space)
            name_start_x = 269   # Left boundary of underlined space
            name_end_x = 1280    # Right boundary of underlined space
            name_y = 600         # Y position
            
            # Calculate center position for name
            name_text = student_data['student_name'].upper()
            name_width = c.stringWidth(name_text, "Helvetica-Bold", name_font_size)
            name_center_x = name_start_x + (name_end_x - name_start_x - name_width) / 2
            
            # Draw centered name
            c.drawString(name_center_x, name_y, name_text)
            
            # Dates at perfect positions with dd-mm-yyyy format
            c.setFont("Helvetica", 26)
            start_date = self.format_date(student_data['batch_start_date'])
            end_date = self.format_date(student_data['batch_end_date'])
            c.drawString(565, 418, start_date)
            c.drawString(965, 418, end_date)
            
            # Additional info
            c.setFont("Helvetica", 12)
            c.drawString(50, 50, f"Batch: {student_data['batch_number']}")
            c.drawString(50, 35, f"ID: {student_data['sixerclass_id']}")
            c.drawString(400, 35, f"Issued: {datetime.now().strftime('%d-%m-%Y')}")
            
            c.save()
            print(f"✅ Template-based certificate created: {output_path}")
            return True
            
        except Exception as e:
            print(f"❌ Certificate generation error: {e}")
            return False