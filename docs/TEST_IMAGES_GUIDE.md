# Test Image Guide for Handwritten Equation Solver

## What to Upload

### ✅ Supported Formats
- **File types**: PNG, JPG, JPEG
- **Recommended**: PNG (better quality)

### ✅ Supported Symbols
The model recognizes:
- **Digits**: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9
- **Operators**: + (addition), - (subtraction), × (multiplication), ÷ (division)

### ✅ Example Equations to Try

**Simple equations:**
- `2 + 3` → Result: 5
- `5 - 2` → Result: 3
- `4 × 3` → Result: 12
- `8 ÷ 2` → Result: 4

**Slightly more complex:**
- `12 + 5` → Result: 17
- `15 - 7` → Result: 8
- `3 × 4` → Result: 12
- `20 ÷ 4` → Result: 5

## Creating Test Images

### Option 1: Draw on Paper and Take Photo
1. Write a simple equation on paper with a dark pen/marker
2. Make sure symbols are:
   - **Well-spaced** (leave gaps between symbols)
   - **Clear and readable**
   - **Large enough** (each symbol at least 1-2cm tall)
3. Take a photo with good lighting
4. Crop to just the equation
5. Upload to the app

### Option 2: Use a Drawing App
1. Use any drawing app (Notes app, Paint, etc.)
2. Write the equation clearly
3. Save as PNG or JPG
4. Upload

### Option 3: Use Sample Images from Dataset
If you have access to the training dataset, you can:
- Pick individual symbol images from `data/data/dataset/`
- Combine them into an equation image
- Or use the individual symbol images one at a time

## Image Requirements

### ✅ Good Image Characteristics:
- **High contrast**: Dark symbols on light background
- **Well-spaced**: At least 20-30 pixels between symbols
- **Clear handwriting**: Not too messy or ambiguous
- **Good lighting**: No shadows or dark spots
- **Centered**: Equation roughly centered in image
- **Simple background**: White or light background works best

### ❌ What to Avoid:
- Too small or cramped symbols
- Overlapping or touching symbols
- Very messy handwriting
- Poor contrast (gray on gray)
- Complex backgrounds with noise
- Blurry or low-resolution images

## Quick Test Tips

### For Best Results:
1. **Start simple**: Try `2 + 3` first
2. **One operator at a time**: Don't try `2 + 3 + 4` yet
3. **Clear spacing**: Leave gaps between digits and operators
4. **Use familiar digits**: Write clearly recognizable numbers

### Testing the Model:
1. Upload a simple equation like `5 + 3`
2. Click "🔮 Solve Equation"
3. Check if it:
   - Detects the symbols correctly
   - Recognizes them properly
   - Calculates the result correctly

## Example Workflow

**Step 1**: Create a simple test image
- Write: `2 + 3` on paper
- Take photo or scan
- Save as `test_equation.png`

**Step 2**: Upload to app
- Go to http://localhost:8501
- Click "Browse files"
- Select your image

**Step 3**: Solve
- Click "🔮 Solve Equation"
- Check the results:
  - Recognized equation: Should show "2+3" or "2 + 3"
  - Solution: Should show "5"

## Troubleshooting

### If recognition fails:
- Try a simpler equation (single digits)
- Increase spacing between symbols
- Use darker, thicker pen strokes
- Check image quality (resolution and contrast)

### If symbols are detected incorrectly:
- Write more clearly
- Increase spacing
- Try different handwriting style
- Use the visualization to see what symbols were detected

## Notes

- The model was trained on **individual symbols**, so it works best with:
  - **Clear separation** between symbols
  - **Standard handwriting** styles
  - **Simple layouts** (horizontal equations)

- Complex equations with parentheses or multiple operators may need better segmentation

Happy testing! 🎉

