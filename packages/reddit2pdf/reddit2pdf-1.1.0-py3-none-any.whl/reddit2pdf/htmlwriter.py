import logging
import os
import pkgutil
import shutil
import subprocess
import time

import jinja2
import markdown

import reddit2pdf.library as library

logger = logging.getLogger(__name__)

templateLoader = jinja2.ChoiceLoader(
    [
        jinja2.FileSystemLoader(searchpath="./reddit2pdf/templates"),
        jinja2.PackageLoader("reddit2pdf", "templates"),
    ]
)
templateEnv = jinja2.Environment(loader=templateLoader)
templateEnv.add_extension("jinja2.ext.debug")
templateEnv.filters["markdown"] = markdown.markdown


def float_to_datetime(value):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(value))


templateEnv.filters["float_to_datetime"] = float_to_datetime


# Copy media from the input folder to the file structure of the html pages
def copy_media(source_path, output_path):
    if output_path.endswith("mp4"):
        try:
            # This fixes mp4 files that won't play in browsers
            command = [
                "ffmpeg",
                "-nostats",
                "-loglevel",
                "0",
                "-i",
                source_path,
                "-c:v",
                "copy",
                "-c:a",
                "copy",
                "-y",
                output_path,
            ]
            logging.debug(f"Running {command}")
            subprocess.call(command)
        except Exception as e:
            logging.error("FFMPEG failed: " + str(e))
    else:
        shutil.copyfile(source_path, output_path)
    logging.debug(f"Moved {source_path} to {output_path}")


# Search the input folder for media files containing the id value from an archive
def find_matching_media(post, input_folder, output_folder):
    paths = []

    for dirpath, dnames, fnames in os.walk(output_folder):
        for f in fnames:
            if post["id"] in f and not f.endswith(".json") and not f.endswith(".html"):
                logging.debug(f"Existing media found: {os.path.join(dirpath + f)}")
                paths.append(f)
    if len(paths) > 0:
        logging.debug(f"Existing media found for {post['id']} = {paths}")
        post["paths"] = paths
        return post
    for dirpath, dnames, fnames in os.walk(input_folder):
        for f in fnames:
            if post["id"] in f and not f.endswith(".json"):
                logging.debug(f"New matching media found: {os.path.join(dirpath + f)}")
                copy_media(os.path.join(dirpath, f), os.path.join(output_folder, f))
                paths.append(f)
    post["paths"] = paths
    return post


# Creates the html for a post using the jinja2 template and writes it to a file
def write_post_to_file(post, output_folder):
    template = templateEnv.get_template("page.html")
    post["filename"] = post["id"] + ".html"
    post["filepath"] = os.path.join(output_folder, post["id"] + ".html")

    with open(post["filepath"], "w", encoding="utf-8") as file:
        file.write(template.render(post=post))
    logging.debug(f"Wrote {post['filepath']}")


def populate_css_file(output):
    css_output_path = os.path.join(output, "style.css")
    css_input_path = "./templates/style.css"
    if os.path.exists(css_input_path):
        shutil.copyfile(css_input_path, css_output_path)
    else:
        try:
            data = pkgutil.get_data(__name__, "templates/style.css")
            with open(css_output_path, "wb") as file:
                file.write(data)
        except Exception as e:
            logger.error(e)


def remove_css_file(output):
    css_output_path = os.path.join(output, "style.css")
    if os.path.exists(css_output_path):
        os.remove(css_output_path)


def combine_to_single_html(filepath):
    # monolith https://teddit.net/r/ObsidianMD/comments/12gfs0k/my_new_look_using_callouts/ -o test.html
    cmd = f"monolith {filepath} -o {filepath}"

    # Run the command with logging
    library.run_command(cmd)

    # Check that the html file exists in the directory
    assert os.path.exists(filepath), f"HTML file '{filepath}' does not exist"

    logging.debug(f"Created HTML archive file: {filepath}")
    return filepath
