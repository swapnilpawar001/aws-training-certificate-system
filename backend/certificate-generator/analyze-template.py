#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
import os

def analyze_template():
    """Analyze uploaded template and create position guide"""
    
    template_dir = "data/certificate-templates/raw"
    
    # Find your template
    templates = []
    for file in os.listdir(template_dir):
        if file.lower().endswith(('.png', '.jpg', '.jpeg')):
            templates.append(file)
    
    if not templates:
        print("❌ No template found!")
        return False
    
    template_path = os.path.join(template_dir, templates[0])
    print(f"📁 Analyzing: {templates[0]}")
    
    try:
        with Image.open(template_path) as img:
            width, height = img.size
            print(f"📐 Template dimensions: {width} x {height}")
            
            # Create analysis with coordinate grid
            analysis = img.copy()
            draw = ImageDraw.Draw(analysis)
            
            # Add coordinate grid for positioning
            for x in range(0, width, 50):
                draw.line([(x, 0), (x, height)], fill="rgba(255,0,0,128)", width=1)
                if x % 100 == 0:
                    draw.text((x+2, 10), str(x), fill='red')
            
            for y in range(0, height, 50):
                draw.line([(0, y), (width, y)], fill="rgba(255,0,0,128)", width=1)
                if y % 100 == 0:
                    draw.text((5, y+2), str(y), fill='red')
            
            # Save analysis
            output_dir = "data/certificate-templates/processed"
            os.makedirs(output_dir, exist_ok=True)
            analysis_path = os.path.join(output_dir, "template-analysis.jpg")
            analysis.save(analysis_path, quality=95)
            
            print(f"✅ Analysis saved: {analysis_path}")
            print("🎯 Use this image to find exact text positions!")
            
            # Suggest default positions
            print(f"\n📍 Suggested text positions for {width}x{height} template:")
            print(f"   Student name: ({width//2}, {height//2})")
            print(f"   Batch number: ({width//2}, {height//2 + 60})")
            print(f"   Start date: ({width//3}, {height//2 + 120})")
            print(f"   End date: ({2*width//3}, {height//2 + 120})")
            
            return True
            
    except Exception as e:
        print(f"❌ Error analyzing template: {e}")
        return False

if __name__ == "__main__":
    analyze_template()
