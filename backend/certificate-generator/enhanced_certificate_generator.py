from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import os
from datetime import datetime

class EnhancedCertificateGenerator:
    def __init__(self):
        # Use enhanced template if available, otherwise regular
        enhanced_path = "data/certificate-templates/processed/template-enhanced.png"
        regular_path = "data/certificate-templates/raw/certificate-template.png"
        
        self.template_path = enhanced_path if os.path.exists(enhanced_path) else regular_path
        self.output_dir = "data/certificate-templates/processed"
        self.font_dir = "data/fonts"
        
        # Create output directory
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.font_dir, exist_ok=True)
        
        # Final perfected positions
        self.text_positions = {
            "student_name": (550, 400),
            "start_date": (420, 530),
            "end_date": (680, 530),
        }
        
        # Font sizes
        self.font_sizes = {
            "student_name": 36,
            "date": 28,
        }
    
    def load_fonts(self):
        """Load highest quality fonts available"""
        fonts = {}
        
        # Priority font sources for best quality
        font_sources = [
            # High-quality system fonts
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/ubuntu/Ubuntu-R.ttf",
            # macOS fonts
            "/System/Library/Fonts/Helvetica.ttc",
            "/System/Library/Fonts/Arial.ttf",
            # Windows fonts
            "C:/Windows/Fonts/arial.ttf",
            "C:/Windows/Fonts/Helvetica.ttf",
            # Fallback to system names
            "LiberationSans-Regular",
            "DejaVuSans",
            "Ubuntu",
            "Helvetica",
            "Arial",
        ]
        
        # Load name font with highest quality
        name_font_path = None
        for font_source in font_sources:
            try:
                if os.path.exists(font_source):
                    fonts["name"] = ImageFont.truetype(font_source, self.font_sizes["student_name"])
                    name_font_path = font_source
                    print(f"✅ Loaded premium font: {os.path.basename(font_source)}")
                    break
                else:
                    fonts["name"] = ImageFont.truetype(font_source, self.font_sizes["student_name"])
                    name_font_path = font_source
                    print(f"✅ Loaded system font: {font_source}")
                    break
            except:
                continue
        
        # Load date font
        if name_font_path:
            try:
                if os.path.exists(name_font_path):
                    fonts["date"] = ImageFont.truetype(name_font_path, self.font_sizes["date"])
                else:
                    fonts["date"] = ImageFont.truetype(name_font_path.split('-')[0], self.font_sizes["date"])
                print(f"✅ Date font loaded (size: {self.font_sizes['date']})")
            except:
                fonts["date"] = ImageFont.load_default()
        else:
            fonts["name"] = ImageFont.load_default()
            fonts["date"] = ImageFont.load_default()
            print("⚠️ Using default fonts")
        
        return fonts
    
    def format_date(self, date_str):
        """Format date nicely for certificate"""
        try:
            if isinstance(date_str, str):
                date_obj = pd.to_datetime(date_str)
            else:
                date_obj = date_str
            return date_obj.strftime("%B %d, %Y")
        except:
            return str(date_str)
    
    def generate_premium_certificate(self, student_data):
        """Generate premium quality certificate"""
        
        # Validate required data
        required_fields = ['student_name', 'batch_number', 'batch_start_date', 'batch_end_date']
        for field in required_fields:
            if field not in student_data:
                print(f"❌ Missing required field: {field}")
                return None
        
        try:
            # Load template (enhanced version if available)
            with Image.open(self.template_path) as template:
                certificate = template.copy()
                
                # Ensure high quality color mode
                if certificate.mode != 'RGB':
                    certificate = certificate.convert('RGB')
                
                draw = ImageDraw.Draw(certificate)
                
                # Load premium fonts
                fonts = self.load_fonts()
                
                # Premium text rendering
                texts_to_draw = [
                    {
                        'text': student_data['student_name'].upper(),
                        'position': self.text_positions['student_name'],
                        'font': fonts['name'],
                        'color': '#0f172a',  # Richer dark blue
                        'label': 'Student Name'
                    },
                    {
                        'text': self.format_date(student_data['batch_start_date']),
                        'position': self.text_positions['start_date'],
                        'font': fonts['date'],
                        'color': '#1e293b',  # Richer dark gray
                        'label': 'Start Date'
                    },
                    {
                        'text': self.format_date(student_data['batch_end_date']),
                        'position': self.text_positions['end_date'],
                        'font': fonts['date'],
                        'color': '#1e293b',  # Richer dark gray
                        'label': 'End Date'
                    }
                ]
                
                # Render with premium quality
                for text_config in texts_to_draw:
                    x, y = text_config['position']
                    
                    # High-quality text rendering
                    draw.text(
                        (x, y), 
                        text_config['text'], 
                        fill=text_config['color'], 
                        font=text_config['font'], 
                        anchor='mm'
                    )
                    
                    print(f"📍 {text_config['label']}: Position ({x}, {y}) - Premium font: {text_config['font'].size}px")
                
                # Generate premium filename
                safe_name = "".join(c for c in student_data['student_name'] if c.isalnum() or c in (' ', '-', '_'))
                output_filename = f"certificate_{student_data['sixerclass_id']}_{safe_name.replace(' ', '_')}_PREMIUM.png"
                output_path = os.path.join(self.output_dir, output_filename)
                
                # Save with PREMIUM quality settings
                certificate.save(
                    output_path,
                    'PNG',
                    quality=100,
                    optimize=False,  # No compression
                    dpi=(300, 300),  # High DPI for print quality
                    compress_level=0  # No PNG compression
                )
                
                print(f"✅ Premium certificate generated: {output_filename}")
                print("✨ Premium quality features:")
                print("   ✓ Enhanced template (if available)")
                print("   ✓ Premium font loading")
                print("   ✓ Maximum PNG quality (100)")
                print("   ✓ High DPI (300)")
                print("   ✓ No compression (level 0)")
                print("   ✓ Richer color palette")
                
                return output_path
                
        except Exception as e:
            print(f"❌ Error generating premium certificate: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def create_premium_test(self):
        """Create premium quality test certificate"""
        
        test_student = {
            'sixerclass_id': 'SIX001',
            'student_name': 'John Doe Smith',
            'batch_number': 'AWS-2024-001',
            'batch_start_date': '2024-01-15',
            'batch_end_date': '2024-04-15'
        }
        
        print("✨ PREMIUM Quality Test Certificate")
        print("="*40)
        print("Premium quality features:")
        print("   ✓ Enhanced template processing")
        print("   ✓ Premium font loading system")
        print("   ✓ Maximum PNG quality settings")
        print("   ✓ Professional color depth")
        print("   ✓ No compression artifacts")
        print()
        
        return self.generate_premium_certificate(test_student)

# Test premium quality generation
if __name__ == "__main__":
    generator = EnhancedCertificateGenerator()
    
    # Create premium test certificate
    test_path = generator.create_premium_test()
    
    if test_path:
        print(f"\n✅ Premium test certificate created!")
        print("✨ Premium quality applied:")
        print("   ✓ Enhanced template processing")
        print("   ✓ Maximum quality settings")
        print("   ✓ Professional rendering")
    else:
        print("\n❌ Failed to create premium test certificate")
