#!/usr/bin/env python3
"""
Create a darker version of the body_bg.png for email backgrounds
"""

from PIL import Image, ImageEnhance, ImageFilter
import os

# Paths
input_path = "/Users/lucianocosme/Projects/ucr-ento-social/assets/images/backgrounds/body_bg.png"
output_path = "/Users/lucianocosme/Projects/ucr-ento-social/assets/images/backgrounds/email_dark_bg.png"

# Open the original image
img = Image.open(input_path)

# Convert to RGBA if not already
if img.mode != 'RGBA':
    img = img.convert('RGBA')

# Create a darker version by:
# 1. Reducing brightness significantly
enhancer = ImageEnhance.Brightness(img)
img_dark = enhancer.enhance(0.15)  # Make it 15% of original brightness (very dark)

# 2. Reduce contrast to make it more subtle
contrast = ImageEnhance.Contrast(img_dark)
img_dark = contrast.enhance(0.5)  # Reduce contrast by 50%

# 3. Apply a slight blur to make it less sharp/distracting
img_dark = img_dark.filter(ImageFilter.GaussianBlur(radius=1))

# 4. Create a dark overlay
# Get the size
width, height = img_dark.size

# Create a new image with dark background
dark_bg = Image.new('RGBA', (width, height), (13, 13, 13, 255))  # #0d0d0d with full opacity

# Blend the original image with the dark background
# This creates a very subtle pattern on dark background
final = Image.blend(dark_bg, img_dark, 0.3)  # Only 30% of the pattern shows through

# Save the result
final.save(output_path, 'PNG', optimize=True)

print(f"✅ Created darker background image at: {output_path}")
print(f"   Original: {input_path}")
print(f"   New dark version: {output_path}")
print(f"   The image is now much darker and subtle for email backgrounds")