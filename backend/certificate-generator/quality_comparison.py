#!/usr/bin/env python3
import os
from PIL import Image

def compare_quality():
    print("🔍 Certificate Quality Comparison")
    print("="*40)
    
    # Find different versions
    processed_dir = "data/certificate-templates/processed"
    
    # Look for different quality versions
    certificates = []
    for file in os.listdir(processed_dir):
        if file.startswith("certificate_SIX001") and file.endswith(".png"):
            certificates.append(file)
    
    if not certificates:
        print("❌ No certificates found for comparison")
        return
    
    print("📋 Found certificates:")
    for i, cert in enumerate(certificates, 1):
        filepath = os.path.join(processed_dir, cert)
        
        with Image.open(filepath) as img:
            file_size = os.path.getsize(filepath)
            
            print(f"\n{i}. {cert}")
            print(f"   Size: {img.size}")
            print(f"   File size: {file_size / 1024:.1f} KB")
            print(f"   Mode: {img.mode}")
            print(f"   DPI: {img.info.get('dpi', 'Not specified')}")
            
            # Quality indicators
            if "_HQ" in cert or "_PREMIUM" in cert:
                print("   Quality: Enhanced/Premium")
            elif file_size > 500000:  # 500KB+
                print("   Quality: High")
            elif file_size > 200000:  # 200KB+
                print("   Quality: Medium")
            else:
                print("   Quality: Standard")
    
    print(f"\n💡 Quality Tips:")
    print("   ✓ Larger file size = higher quality (less compression)")
    print("   ✓ RGB mode = better color depth than indexed")
    print("   ✓ Higher DPI = better print quality")
    print("   ✓ Use _HQ or _PREMIUM versions for best results")

if __name__ == "__main__":
    compare_quality()
