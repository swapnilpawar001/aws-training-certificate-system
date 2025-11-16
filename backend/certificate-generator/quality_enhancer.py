#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import os

class QualityEnhancer:
    def __init__(self):
        self.template_path = "data/certificate-templates/raw/certificate-template.png"
        self.output_dir = "data/certificate-templates/processed"
    
    def analyze_current_quality(self):
        """Analyze the current template quality"""
        
        with Image.open(self.template_path) as img:
            print("🔍 Template Quality Analysis")
            print("="*35)
            print(f"   Format: {img.format}")
            print(f"   Mode: {img.mode}")
            print(f"   Size: {img.size}")
            print(f"   DPI: {img.info.get('dpi', 'Not specified')}")
            
            # Check color depth
            if img.mode == 'RGBA':
                print("   Color depth: 32-bit (RGBA)")
            elif img.mode == 'RGB':
                print("   Color depth: 24-bit (RGB)")
            elif img.mode == 'P':
                print("   Color depth: 8-bit (Indexed)")
            elif img.mode == 'L':
                print("   Color depth: 8-bit (Grayscale)")
            
            # Check file size
            import os
            file_size = os.path.getsize(self.template_path)
            print(f"   File size: {file_size / 1024:.1f} KB")
            
            return img.info
    
    def enhance_template(self, input_path, output_path):
        """Apply various quality enhancements"""
        
        with Image.open(input_path) as img:
            # Start with original
            enhanced = img.copy()
            
            print("✨ Applying quality enhancements...")
            
            # 1. Convert to RGB if needed (better color depth)
            if enhanced.mode != 'RGB':
                enhanced = enhanced.convert('RGB')
                print("   ✓ Converted to RGB (24-bit color)")
            
            # 2. Enhance sharpness slightly
            enhancer = ImageEnhance.Sharpness(enhanced)
            enhanced = enhancer.enhance(1.1)  # Subtle sharpness increase
            print("   ✓ Enhanced sharpness (+10%)")
            
            # 3. Enhance contrast slightly
            enhancer = ImageEnhance.Contrast(enhanced)
            enhanced = enhancer.enhance(1.05)  # Subtle contrast increase
            print("   ✓ Enhanced contrast (+5%)")
            
            # 4. Save with maximum quality
            enhanced.save(
                output_path,
                'PNG',
                quality=100,
                optimize=False,
                dpi=(300, 300)
            )
            print("   ✓ Saved with maximum quality settings")
            
            return output_path

    def create_quality_comparison(self):
        """Create comparison between standard and enhanced quality"""
        
        output_enhanced = os.path.join(self.output_dir, "template-enhanced.png")
        
        # Enhance the template
        self.enhance_template(self.template_path, output_enhanced)
        
        print(f"\n✅ Enhanced template saved: {output_enhanced}")
        print("🎯 Use the enhanced template for better certificate quality!")

# Quality analysis and enhancement
if __name__ == "__main__":
    enhancer = QualityEnhancer()
    
    # Analyze current quality
    enhancer.analyze_current_quality()
    
    # Create enhanced version
    enhancer.create_quality_comparison()
