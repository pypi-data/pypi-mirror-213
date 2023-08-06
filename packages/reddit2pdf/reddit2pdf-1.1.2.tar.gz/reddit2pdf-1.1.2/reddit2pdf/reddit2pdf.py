import logging
import os
import shutil
import tempfile

import reddit2pdf.html2pdf as html2pdf
import reddit2pdf.json2html as json2html
import reddit2pdf.url2bdfr as url2bdfr
from reddit2pdf.configuration import Configuration

logger = logging.getLogger(__name__)


def _move_collateral(
    indir: str, outdir: str, include_media: bool = False, include_html: bool = False
):
    # Get a list of files in the input directory
    files = os.listdir(indir)

    # Loop through the files and move any pdfs to the output directory
    pdf_count = 0
    output_files = {"pdf": None, "media": [], "html": None}
    for file in files:
        if file.endswith(".pdf"):
            if os.path.exists(os.path.join(outdir, file)):
                logging.warning(
                    f"PDF file already existed in outdir: {outdir}. Replacing..."
                )
                os.remove(os.path.join(outdir, file))

            if output_files["pdf"]:
                raise ValueError(
                    f"{pdf_count} PDF files were moved. Please ensure that exactly one PDF file is present in {indir}."
                )

            shutil.move(os.path.join(indir, file), os.path.join(outdir, file))
            output_files["pdf"] = os.path.join(outdir, file)
            logging.info(f"Moved PDF file {file} from {indir} to {outdir}")

        elif file.endswith(".html") and include_html:
            if os.path.exists(os.path.join(outdir, file)):
                logging.warning(
                    f"HTML file already existed in outdir: {outdir}. Replacing..."
                )
                os.remove(os.path.join(outdir, file))

            shutil.move(os.path.join(indir, file), os.path.join(outdir, file))
            output_files["html"] = os.path.join(outdir, file)
            logging.info(f"Moved HTML file {file} from {indir} to {outdir}")
        elif include_media:
            # If include_media is True, move any files with media extensions to the output directory
            media_extensions = [
                ".jpg",
                ".jpeg",
                ".png",
                ".gif",
                ".mp4",
                ".mov",
                ".avi",
                ".mp3",
                ".wav",
            ]
            if os.path.splitext(file)[1] in media_extensions:
                file_path = os.path.join(indir, file)
                file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
                if file_size_mb > 50:
                    logging.warning(
                        f"Media file {file} is larger than 50 megabytes ({file_size_mb:.2f} MB)"
                    )

                if os.path.exists(os.path.join(outdir, file)):
                    logging.debug(
                        f"Media file already existed in output. Skipping {file}"
                    )
                else:
                    shutil.move(file_path, os.path.join(outdir, file))
                    logging.info(f"Moved media file {file} from {indir} to {outdir}")
                output_files["media"].append(os.path.join(outdir, file))
    return output_files


def reddit2pdf(conf: Configuration):
    # Generate temporary directory to store all bdfr + html intermediaries
    tempdir = tempfile.mkdtemp(suffix="reddit2pdf", dir="/tmp")
    # Use BDFR to download the reddit URL to the temp directory
    bdfr_dir = url2bdfr.download_reddit_url(conf.link, tempdir)
    # Generate HTML file from resulting BDFR archive
    html_dir = json2html.generate_reddit_post_html(bdfr_dir)
    # Generate PDF file from HTML file
    pdf_path = html2pdf.generate_pdf_file(html_dir)
    logging.info(f"Generated PDF: {pdf_path}")

    if not os.path.exists(conf.outdir):
        logging.info(f"Outdir {conf.outdir} did not exist. Creating...")
        os.makedirs(conf.outdir, exist_ok=True)

    # Move desired collateral to output directory
    output_collateral = _move_collateral(
        tempdir, conf.outdir, conf.move_media, conf.move_html
    )

    # Destroy temp directory
    if not conf.unclean:
        shutil.rmtree(tempdir)

    logging.info(f"Generated collateral: {output_collateral}")
    return output_collateral
