"""Extract text from PDF for card parsing."""
import sys
from pathlib import Path

try:
    from pypdf import PdfReader
except ImportError:
    print("Install pypdf: pip install pypdf")
    sys.exit(1)

def extract_pdf_text(pdf_path):
    reader = PdfReader(pdf_path)
    text_parts = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        text_parts.append(f"--- PAGE {i+1} ---\n{text or '(no text)'}")
    return "\n\n".join(text_parts)

if __name__ == "__main__":
    base = Path(__file__).parent
    pdfs = list(base.glob("*.pdf")) + list(base.parent.glob("*.pdf"))
    for pdf in pdfs:
        print(f"\n{'='*60}\nFILE: {pdf.name}\n{'='*60}")
        try:
            text = extract_pdf_text(pdf)
            print(text[:15000])  # First ~15k chars
            if len(text) > 15000:
                print(f"\n... (truncated, total {len(text)} chars)")
        except Exception as e:
            print(f"Error: {e}")
