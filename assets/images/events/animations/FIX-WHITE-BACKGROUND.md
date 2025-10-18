# Fix White Background in Photoshop - QUICK GUIDE

## The Problem
The PNG files were exported as PNG-8 with a white background color embedded. They need to be re-exported as PNG-24 with full alpha transparency.

## Quick Fix (Do this for ALL files in this folder):

### Method 1: Batch Re-export in Photoshop

1. **Open Photoshop**
2. **File → Scripts → Image Processor**
3. **Select folder**: Choose this folder (`animations/`)
4. **Settings**:
   - File Type: **PNG**
   - Save in same location: **YES**
   - Convert Profile to sRGB: **CHECK**
5. **Click RUN**

Then manually for each file:
1. Open the processed image
2. **File → Export → Export As...**
3. Format: **PNG**
4. **CHECK** "Transparency"
5. **Uncheck** "Smaller File (8-bit)"
6. Click **Export**

### Method 2: Individual File Fix (Faster)

For each PNG file in this folder:

1. **Double-click** to open in Photoshop
2. **Select → All** (Cmd+A)
3. **Edit → Copy Merged** (Shift+Cmd+C)
4. **File → New** (Photoshop will auto-detect size)
   - IMPORTANT: Background Contents: **TRANSPARENT**
5. **Edit → Paste** (Cmd+V)
6. **File → Export → Export As...**
   - Format: **PNG**
   - **CHECK** Transparency
   - **UNCHECK** Smaller File (8-bit)
   - Click **Export**
7. Save over the original file

### Method 3: Use "Remove.bg" style tool (EASIEST!)

1. Go to https://www.remove.bg (or use Photoshop's Remove Background)
2. Upload each PNG file
3. Download the result
4. Replace the file in this folder

## Files to Fix:
- bat_1.png
- bird_1.png
- cat_1.png
- espantalho.png
- ghost_1.png
- gohst_2.png
- spider_web.png

## How to check if fixed:
Open the PNG in Preview (Mac) or any image viewer. The checkerboard pattern should show through where there's transparency, NOT white.

## After fixing:
Refresh the page: http://138.23.14.176:8000/coffee-hour-halloween.html
The animations should now float with transparent backgrounds!
