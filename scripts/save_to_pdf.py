import markdown
from xhtml2pdf import pisa
from pathlib import Path
from datetime import datetime
import uuid

script = Path(__file__).resolve().parent
root = script.parent
SOURCE_FOLDER = root/"models"/"gemini-response"
TARGET_FOLDER = root/"models"/"reports"
TARGET_FOLDER.mkdir(parents=True, exist_ok=True)

def generate_random_filename(original_stem: str) -> str:
    """Creates a unique filename: original name + timestamp + random suffix."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    random_suffix = uuid.uuid4().hex[:6]
    return f"{original_stem}_{timestamp}_{random_suffix}.pdf"

def markdown_to_html(md_text: str) -> str:
    """Converts markdown text to styled HTML, ready for PDF conversion."""
    body_html = markdown.markdown(md_text, extensions=["tables", "fenced_code"])
    
    # Wrap with basic CSS styling so the PDF looks clean and professional
    html = f"""
    <html>
    <head>
    <style>
        body {{ font-family: Helvetica, Arial, sans-serif; font-size: 12px; line-height: 1.5; }}
        h1 {{ font-size: 22px; color: #1a1a1a; border-bottom: 2px solid #333; padding-bottom: 4px; }}
        h2 {{ font-size: 18px; color: #2c2c2c; margin-top: 20px; }}
        h3 {{ font-size: 15px; color: #444; }}
        table {{ border-collapse: collapse; width: 100%; margin: 10px 0; }}
        th, td {{ border: 1px solid #999; padding: 6px; text-align: left; }}
        th {{ background-color: #eee; }}
        code {{ background-color: #f2f2f2; padding: 2px 4px; font-family: monospace; }}
        ul, ol {{ margin-left: 20px; }}
    </style>
    </head>
    <body>
    {body_html}
    </body>
    </html>
    """
    return html

def convert_markdown_to_pdf(md_text: str, output_path: Path):
    html_content = markdown_to_html(md_text)
    
    with open(output_path, "wb") as pdf_file:
        pisa_status = pisa.CreatePDF(html_content, dest=pdf_file)
    
    if pisa_status.err:
        print(f"⚠️ Error converting to PDF: {output_path.name}")
    return not pisa_status.err

# ============================================================
# Process every .md file in the source folder
# ============================================================
def process_all_files():
    md_files = list(SOURCE_FOLDER.glob("*.md"))
    
    if not md_files:
        print("No .md files found in source folder.")
        return
    
    for md_file in md_files:
        with open(md_file, "r", encoding="utf-8") as f:
            text = f.read()
        
        filename = generate_random_filename(md_file.stem)
        output_path = TARGET_FOLDER / filename
        
        success = convert_markdown_to_pdf(text, output_path)
        if success:
            print(f"Converted: {md_file.name} -> {filename}")
            print(f"Successfully saved to {TARGET_FOLDER/filename} ✅")

if __name__ == "__main__":
    process_all_files()