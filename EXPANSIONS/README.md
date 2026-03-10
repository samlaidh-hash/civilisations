# Expansion PDFs - Extraction Status

## Files Found
- **20190211_BARBARIANS ALL_X-1a.pdf** → Barbarians expansion
- **20190211_COC ALL_X-1a.pdf** → Cradle of Civilization (COC)
- **20190211_GODS KINGS ALL_X-1a.pdf** → Gods and Kings
- **20190211_OWL AGE_ALL_X-1a.pdf** → Owl and Eagle

## Issue: Image-Only PDFs
These expansion PDFs contain **no embedded text**—they appear to be image-based (card scans/layouts). Standard PDF text extraction (pypdf, PyMuPDF) returns empty pages.

## Solution: OCR Extraction
To extract card text, use OCR (Optical Character Recognition):

### 1. Install Tesseract OCR
- **Windows**: Download from https://github.com/UB-Mannheim/tesseract/wiki
- Install and ensure `tesseract` is on your PATH

### 2. Install Python dependencies
```bash
pip install pymupdf pytesseract pillow
```

### 3. Run the OCR script
```bash
cd "D:\Dropbox\Free Games\2025 RPG\CLAUDE GAMES\RL_LEV\sixkingdoms"
python ocr_expansions.py
```

This will create `expansion_ocr_*.txt` files with extracted text.

### 4. After extraction
Once you have the OCR output files, the card implementation can proceed. Share the extracted text or run the implementation step with the OCR output available.

## Alternative: Manual Card Data
If OCR quality is poor, you can create a JSON or text file listing the expansion cards (name, cost, type, ability, etc.) and the implementation can use that directly.
