from PIL import Image, ImageDraw, ImageFont

# Open template
with Image.open('data/certificate-templates/raw/certificate-template.png') as img:
    draw = ImageDraw.Draw(img)

    # Fonts
    name_font = ImageFont.truetype("data/fonts/DejaVuSans.ttf", 36)
    date_font = ImageFont.truetype("data/fonts/DejaVuSans.ttf", 22)

    # Test positions (tune these)
    # Adjusted positions (shift left & up)
    # Final nudge left (-20px)
    draw.text((405, 380), "Rahul Sharma", font=name_font, fill="red")  # ← 20px left
    draw.text((345, 515), "2024-01-15", font=date_font, fill="red")   # ← 20px left
    draw.text((625, 515), "2024-04-15", font=date_font, fill="red")   # ← 20px left

    # Save preview
    img.save('position_preview.png', quality=100)
    print("✅ Preview saved as position_preview.png")