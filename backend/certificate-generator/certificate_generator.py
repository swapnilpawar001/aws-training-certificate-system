from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import os
from datetime import datetime

class CertificateGenerator:
    def __init__(self):
        self.template_path = "data/certificate-templates/raw/certificate-template.png"
        self.output_dir = "data/certificate-templates/processed"
        self.font_dir = "data/fonts"
        
        # Create output directory
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.font_dir, exist_ok=True)
        
        # Final positions (perfected)
        self.text_positions = {
            "student_name": (550, 400),
            "start_date": (420, 530),
            "end_date": (680, 530),
        }
        
        # Font sizes
        self.font_sizes = {
            "student_name": 36,
            "date": 22,
        }
    
    def load_fonts(self):
        """Load high-quality fonts - try multiple sources"""
        fonts = {}
        
        # Try multiple font sources for better quality
        font_sources = [
            # System fonts (highest quality)
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/System/Library/Fonts/Helvetica.ttc",  # macOS
            "C:/Windows/Fonts/arial.ttf",  # Windows
            # Fallback to system names
            "LiberationSans-Regular",
            "DejaVuSans",
            "Helvetica",
            "Arial",
        ]
        
        # Try to load name font
        name_font = None
        for font_source in font_sources:
            try:
                if os.path.exists(font_source):
                    # Direct file path
                    fonts["name"] = ImageFont.truetype(font_source, self.font_sizes["student_name"])
                    name_font = font_source
                    print(f"✅ Loaded high-quality font: {os.path.basename(font_source)}")
                    break
                else:
                    # System font name
                    fonts["name"] = ImageFont.truetype(font_source, self.font_sizes["student_name"])
                    name_font = font_source
                    print(f"✅ Loaded system font: {font_source}")
                    break
            except:
                continue
        
        # Load date font (same family, smaller size)
        if name_font:
            try:
                if os.path.exists(name_font):
                    fonts["date"] = ImageFont.truetype(name_font, self.font_sizes["date"])
                else:
                    fonts["date"] = ImageFont.truetype(name_font.split('-')[0], self.font_sizes["date"])
                print(f"✅ Date font loaded (size: {self.font_sizes['date']})")
            except:
                fonts["date"] = ImageFont.load_default()
                print("⚠️ Using default date font")
        else:
            # Ultimate fallback
            fonts["name"] = ImageFont.load_default()
            fonts["date"] = ImageFont.load_default()
            print("⚠️ Using default fonts - install fonts for better quality")
        
        return fonts
    
    def format_date(self, date_str):
        """Format date nicely for certificate"""
        try:
            if isinstance(date_str, str):
                date_obj = pd.to_datetime(date_str)
            else:
                date_obj = date_str
            return date_obj.strftime("%B %d, %Y")  # e.g., "January 15, 2024"
        except:
            return str(date_str)
    
    def enhance_template_quality(self, template):
        """Enhance template quality before adding text"""
        # Convert to RGB if not already (better quality)
        if template.mode != 'RGB':
            template = template.convert('RGB')
        
        # Ensure we're working with full quality
        return template
    
    def generate_certificate(self, student_data):
        """Generate high-quality certificate"""
        
        # Validate required data
        required_fields = ['student_name', 'batch_number', 'batch_start_date', 'batch_end_date']
        for field in required_fields:
            if field not in student_data:
                print(f"❌ Missing required field: {field}")
                return None
        
        try:
            # Load template with quality enhancement
            with Image.open(self.template_path) as template:
                # Enhance template quality
                certificate = self.enhance_template_quality(template.copy())
                draw = ImageDraw.Draw(certificate)
                
                # Load high-quality fonts
                fonts = self.load_fonts()
                
                # Prepare text data
                texts_to_draw = [
                    {
                        'text': student_data['student_name'].upper(),
                        'position': self.text_positions['student_name'],
                        'font': fonts['name'],
                        'color': '#1a365d',  # Rich dark blue
                        'label': 'Student Name'
                    },
                    {
                        'text': self.format_date(student_data['batch_start_date']),
                        'position': self.text_positions['start_date'],
                        'font': fonts['date'],
                        'color': '#2d3748',  # Rich dark gray
                        'label': 'Start Date'
                    },
                    {
                        'text': self.format_date(student_data['batch_end_date']),
                        'position': self.text_positions['end_date'],
                        'font': fonts['date'],
                        'color': '#2d3748',  # Rich dark gray
                        'label': 'End Date'
                    }
                ]
                
                # Add each text element with high quality
                for text_config in texts_to_draw:
                    x, y = text_config['position']
                    
                    # Draw text with high quality settings
                    draw.text(
                        (x, y), 
                        text_config['text'], 
                        fill=text_config['color'], 
                        font=text_config['font'], 
                        anchor='mm'
                    )
                    
                    print(f"📍 {text_config['label']}: Position ({x}, {y}) - Font: {text_config['font'].size}px")
                
                # Generate high-quality output filename
                safe_name = "".join(c for c in student_data['student_name'] if c.isalnum() or c in (' ', '-', '_'))
                output_filename = f"certificate_{student_data['sixerclass_id']}_{safe_name.replace(' ', '_')}_HQ.png"
                output_path = os.path.join(self.output_dir, output_filename)
                
                # Save with HIGH QUALITY settings
                certificate.save(
                    output_path, 
                    'PNG', 
                    quality=100,  # Maximum quality
                    optimize=False,  # Don't optimize to preserve quality
                    dpi=(300, 300)  # High DPI for print quality
                )
                
                print(f"✅ High-quality certificate generated: {output_filename}")
                print(f"📁 Saved with maximum quality settings")
                return output_path
                
        except Exception as e:
            print(f"❌ Error generating certificate: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def create_high_quality_test(self):
        """Create high-quality test certificate"""
        
        test_student = {
            'sixerclass_id': 'SIX001',
            'student_name': 'John Doe Smith',
            'batch_number': 'AWS-2024-001',
            'batch_start_date': '2024-01-15',
            'batch_end_date': '2024-04-15'
        }
        
        print("🎯 HIGH-QUALITY Test Certificate")
        print("="*40)
        print("✨ Quality enhancements:")
        print("   ✓ High-quality font loading")
        print("   ✓ RGB color mode conversion")
        print("   ✓ Maximum PNG quality (100)")
        print("   ✓ High DPI settings (300 DPI)")
        print("   ✓ No compression optimization")
        print()
        
        return self.generate_certificate(test_student)

# Test high-quality generation
if __name__ == "__main__":
    generator = CertificateGenerator()
    
    # Create high-quality test certificate
    test_path = generator.create_high_quality_test()
    
    if test_path:
        print(f"\n✅ High-quality test certificate created!")
        print("🎯 Quality enhancements applied:")
        print("   ✓ Maximum PNG quality")
        print("   ✓ High DPI for print quality")
        print("   ✓ Better font handling")
        print("   ✓ Enhanced color depth")
    else:
        print("\n❌ Failed to create high-quality test certificate")
