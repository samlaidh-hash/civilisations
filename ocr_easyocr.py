"""
Extract text from expansion PDFs using EasyOCR (no Tesseract needed).
"""
from pathlib import Path
import sys
import io

EXPANSIONS_DIR = Path(r"D:\Dropbox\Free Games\2025 RPG\CLAUDE GAMES\RL_LEV\sixkingdoms\EXPANSIONS")
OUTPUT_DIR = Path(r"D:\Dropbox\Free Games\2025 RPG\CLAUDE GAMES\RL_LEV\sixkingdoms")

def main():
    try:
        import fitz
        import easyocr
        import numpy as np
    except ImportError as e:
        print("Install: pip install pymupdf easyocr")
        sys.exit(1)

    print("Loading EasyOCR (first run downloads models ~100MB)...")
    reader = easyocr.Reader(['en'], gpu=False, verbose=False)
    
    for pdf in sorted(EXPANSIONS_DIR.glob("*.pdf")):
        name = pdf.stem.replace(" ", "_")
        out = OUTPUT_DIR / f"expansion_ocr_{name}.txt"
        print(f"Processing {pdf.name}...")
        doc = fitz.open(str(pdf))
        lines = []
        for i in range(len(doc)):
            mat = fitz.Matrix(2, 2)
            pix = doc[i].get_pixmap(matrix=mat, alpha=False)
            img_array = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
            if pix.n == 4:
                img_array = img_array[:,:,:3]
            result = reader.readtext(img_array, paragraph=True)
            text = "\n".join([r[1] for r in result]) if result else ""
            lines.append(f"--- PAGE {i+1} ---\n{text}")
        doc.close()
        out.write_text("\n\n".join(lines), encoding="utf-8")
        print(f"  -> {out.name}")
    print("Done.")

if __name__ == "__main__":
    main()
