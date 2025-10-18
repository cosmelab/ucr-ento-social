# Halloween Animation Assets

This directory contains transparent PNG images extracted from the Spooktacular Coffee Hour flyer for animated effects on the event page.

## Required Images to Extract in Photoshop

Extract these elements from `/assets/images/events/Mauck_Lab_Coffee_Hour_original.png` with **transparent backgrounds**:

### 1. bat.png
- Extract one or both bat silhouettes from the flyer
- Recommended size: 80-100px wide
- Format: PNG with transparency
- Usage: Will float and rotate across the page

### 2. ghost.png
- Extract one of the ghost characters
- Recommended size: 70-80px wide
- Format: PNG with transparency
- Usage: Will bounce and fade in/out

### 3. pumpkin.png
- Extract the jack-o-lantern or decorative pumpkin
- Recommended size: 90-100px wide
- Format: PNG with transparency
- Usage: Will swing back and forth

### 4. spiderweb.png
- Extract spider web from corners
- Recommended size: 150px wide
- Format: PNG with transparency
- Usage: Will appear in top-right corner

### 5. Optional extras:
- black-cat.png - The black cat silhouette
- witch.png - The witch on broomstick
- mummy.png - The mummy character

## Photoshop Steps

1. Open `Mauck_Lab_Coffee_Hour_original.png` in Photoshop
2. For each element:
   - Use the **Magic Wand Tool** or **Lasso Tool** to select the element
   - If the flyer has a white background, use **Select > Subject** or manually select
   - Copy the selection (Cmd+C)
   - Create a new document with transparent background
   - Paste (Cmd+V)
   - Crop to desired size
   - **File > Export > Export As...**
   - Choose PNG format
   - Enable "Transparency"
   - Save to this directory with the appropriate name

## Alternative: Use Mauck_Lab_Coffee_Hour_transparent.png

Since you already have a transparent version, you can:
1. Open `Mauck_Lab_Coffee_Hour_transparent.png`
2. Individual elements should be easier to select/extract
3. Use the same extraction process above

## Current Animation Effects

Once images are added, the coffee-hour-halloween.html page will automatically:
- **Bats**: Float left-right with gentle rotation
- **Ghosts**: Bounce slowly and fade in/out
- **Pumpkin**: Swing like hanging decoration
- **Spider web**: Static in corner with reduced opacity

## Testing

After adding images:
1. Refresh http://138.23.14.176:8000/coffee-hour-halloween.html
2. Check animations on both desktop and iPhone
3. Adjust opacity/size in CSS if needed (lines 85-126 in coffee-hour-halloween.html)

## Image Quality Tips

- Keep file sizes small (< 50KB each) for fast mobile loading
- Use PNG-8 with transparency for smaller files if colors are limited
- PNG-24 for better quality if file size isn't an issue
- Images will be resized by CSS, so don't need to be exact dimensions
