"""Extract text from all expansion PDFs."""
from pathlib import Path
from pypdf import PdfReader

EXPANSIONS_DIR = Path(r"D:\Dropbox\Free Games\2025 RPG\CLAUDE GAMES\RL_LEV\sixkingdoms\EXPANSIONS")
OUTPUT_DIR = Path(r"D:\Dropbox\Free Games\2025 RPG\CLAUDE GAMES\RL_LEV\sixkingdoms")

def extract_pdf(pdf_path):
    reader = PdfReader(str(pdf_path))
    parts = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        parts.append(f"--- PAGE {i+1} ---\n{text}")
    return "\n\n".join(parts)

def main():
    pdfs = list(EXPANSIONS_DIR.glob("*.pdf"))
    for pdf in pdfs:
        name = pdf.stem.replace(" ", "_")
        out = OUTPUT_DIR / f"expansion_{name}.txt"
        try:
            text = extract_pdf(pdf)
            out.write_text(text, encoding="utf-8")
            print(f"Extracted {pdf.name} -> {out.name} ({len(text)} chars)")
        except Exception as e:
            print(f"Error {pdf.name}: {e}")

if __name__ == "__main__":
    main()
