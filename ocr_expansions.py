"""
OCR expansion PDFs - run when Tesseract is installed.
Expansion PDFs are image-based; pypdf/PyMuPDF extract no text.
Install: https://github.com/UB-Mannheim/tesseract/wiki
Then: pip install pymupdf pytesseract pillow
"""
from pathlib import Path
import sys

EXPANSIONS_DIR = Path(r"D:\Dropbox\Free Games\2025 RPG\CLAUDE GAMES\RL_LEV\sixkingdoms\EXPANSIONS")
OUTPUT_DIR = Path(r"D:\Dropbox\Free Games\2025 RPG\CLAUDE GAMES\RL_LEV\sixkingdoms")

def main():
    try:
        import fitz  # pymupdf
        import pytesseract
        from PIL import Image
        import io
    except ImportError as e:
        print("Install: pip install pymupdf pytesseract pillow")
        print(e)
        sys.exit(1)

    try:
        pytesseract.get_tesseract_version()
    except Exception:
        print("Tesseract OCR not found. Install from:")
        print("https://github.com/UB-Mannheim/tesseract/wiki")
        sys.exit(1)

    for pdf in EXPANSIONS_DIR.glob("*.pdf"):
        name = pdf.stem.replace(" ", "_")
        out = OUTPUT_DIR / f"expansion_ocr_{name}.txt"
        print(f"Processing {pdf.name}...")
        doc = fitz.open(str(pdf))
        lines = []
        for i in range(len(doc)):
            mat = fitz.Matrix(2, 2)
            pix = doc[i].get_pixmap(matrix=mat, alpha=False)
            img = Image.open(io.BytesIO(pix.tobytes("png")))
            text = pytesseract.image_to_string(img)
            lines.append(f"--- PAGE {i+1} ---\n{text}")
        doc.close()
        out.write_text("\n\n".join(lines), encoding="utf-8")
        print(f"  -> {out.name}")
    print("Done.")

if __name__ == "__main__":
    main()
