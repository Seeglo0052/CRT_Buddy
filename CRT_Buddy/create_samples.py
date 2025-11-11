"""
Example Generator - Create sample Y2K images for testing
"""
from PIL import Image, ImageDraw, ImageFont
import os

def create_sample_images():
    """Create sample test images"""
    output_dir = "samples"
    os.makedirs(output_dir, exist_ok=True)
    
    print("Creating sample images for testing...")
    
    # Sample 1: Simple gradient
    img1 = Image.new('RGB', (600, 400))
    draw = ImageDraw.Draw(img1)
    for y in range(400):
        ratio = y / 400
        r = int(255 * (1 - ratio))
        g = int(255 * ratio * 0.5)
        b = int(255 * ratio)
        draw.line([(0, y), (600, y)], fill=(r, g, b))
    
    try:
        font = ImageFont.truetype("arial.ttf", 60)
    except:
        font = ImageFont.load_default()
    
    draw.text((150, 170), "TEST", fill='#ffffff', font=font)
    img1.save(os.path.join(output_dir, "sample_gradient.png"))
    print("[OK] Created: sample_gradient.png")
    
    # Sample 2: Colorful pattern
    img2 = Image.new('RGB', (600, 400), '#000000')
    draw = ImageDraw.Draw(img2)
    
    colors = ['#ff00ff', '#00ffff', '#ffff00', '#00ff00']
    for i in range(0, 600, 30):
        for j in range(0, 400, 30):
            color = colors[(i // 30 + j // 30) % len(colors)]
            draw.rectangle([i, j, i+25, j+25], fill=color)
    
    img2.save(os.path.join(output_dir, "sample_pattern.png"))
    print("[OK] Created: sample_pattern.png")
    
    # Sample 3: Simple face
    img3 = Image.new('RGB', (600, 400), '#0066cc')
    draw = ImageDraw.Draw(img3)
    
    # Face
    draw.ellipse([200, 100, 400, 300], fill='#ffcc99', outline='#000000', width=3)
    # Eyes
    draw.ellipse([250, 160, 280, 190], fill='#000000')
    draw.ellipse([320, 160, 350, 190], fill='#000000')
    # Smile
    draw.arc([240, 180, 360, 260], start=0, end=180, fill='#000000', width=3)
    
    img3.save(os.path.join(output_dir, "sample_face.png"))
    print("[OK] Created: sample_face.png")
    
    print(f"\nSample images saved to '{output_dir}/' folder")
    print("You can use these to test CRT Buddy!")

if __name__ == "__main__":
    create_sample_images()
    input("\nPress Enter to exit...")
