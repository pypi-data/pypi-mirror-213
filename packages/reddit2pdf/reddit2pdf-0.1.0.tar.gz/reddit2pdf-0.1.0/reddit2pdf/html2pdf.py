import logging
import os
from pathlib import Path

import reddit2pdf.library as library

logger = logging.getLogger(__name__)


# Input: Path to directory containing HTML, media, and CSSfiles
# Output: PDF File path
# Note: HTML sources from same directory.
def generate_pdf_file(html_dir: str) -> Path:
    html_path = Path(html_dir)
    pdf_path = html_path / "output.pdf"

    # Add the HTML file and output PDF file to the command
    html_files = [f for f in html_path.glob("*.html")]
    logging.debug(f"Found HTML files: {html_files}")
    if len(html_files) != 1:
        raise ValueError("There should be exactly one HTML file in the directory.")

    # wkhtmltopdf --enable-local-file-access <html_file> test.pdf
    cmd = f"wkhtmltopdf --enable-local-file-access \
        --margin-bottom 0 --margin-left 0 --margin-right 0 --margin-top 0 \
        {html_files[0]} {pdf_path}"

    # Run the command with logging
    library.run_command(cmd)

    # Check that the PDF file exists in the directory
    assert os.path.exists(pdf_path), f"PDF file '{pdf_path}' does not exist"

    return pdf_path
