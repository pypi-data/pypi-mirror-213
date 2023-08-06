import logging
import os
import shlex
import subprocess
from urllib.parse import urlparse

import requests

logger = logging.getLogger(__name__)


def run_command(
    cmd: str, cwd: str = None, ignore_errors: bool = False, is_dry_run: bool = False
):
    logging.info(f"Running  command: {cmd}")

    if is_dry_run:
        logging.info("Dry run mode. Skipping command execution")
        return ([], [], 0)

    try:
        process = subprocess.Popen(
            shlex.split(cmd),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            cwd=cwd,
        )

        stdout_lines = []
        stderr_lines = []

        # Stream stdout and stderr to Python logging and capture the output
        is_finished = False
        while True:
            for stdout_line in process.stdout.readlines():
                stdout_line = stdout_line.strip()
                logging.debug(stdout_line)
                stdout_lines.append(stdout_line)

            for stderr_line in process.stderr.readlines():
                stderr_line = stderr_line.strip()
                logging.debug(stderr_line)
                stderr_lines.append(stderr_line)

            if is_finished:
                break
            if process.poll() is not None:
                is_finished = True

        exit_code = process.returncode
        output = (stdout_lines, stderr_lines, exit_code)
        return output
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        if ignore_errors:
            logging.warning("Ignoring error and returning empty output.")
            return ([], [], 1)
        else:
            raise


def url_checker(domains):
    def decorator(func):
        def wrapper(url):
            # Handle RFC 1808
            if not url.startswith("http"):
                url = "https://" + url

            parsed_url = urlparse(url)
            domain = parsed_url.netloc
            logging.debug(f"Checking {url=} of {domain=} for {domains=}")
            return any(subdomain in domain for subdomain in domains)

        return wrapper

    return decorator


@url_checker(
    ["www.reddit.com", "www.redd.it", "www.redditmedia.com", "www.reddituploads.com"]
)
def is_reddit_url(url):
    """
    Check if the given URL is from Reddit.

    Args:
        url (str): The URL to check.

    Returns:
        bool: True if the URL is from Reddit, False otherwise.
    """
    pass


def is_url_accessible(url):
    """
    Check if a URL is accessible.

    Args:
        url (str): The URL to check.

    Returns:
        bool: True if the URL is accessible, False otherwise.
    """
    try:
        response = requests.head(url)
        is_accessible = response.status_code == 200
        logging.debug(f"{url=} was accessible: {is_accessible}")
        return is_accessible
    except requests.exceptions.RequestException:
        logging.warning(f"Was unable to access url: {url}")
        return False


def get_json_file_path(directory_path):
    if not os.path.exists(directory_path):
        raise FileNotFoundError(f"Unable to find directory: {directory_path}")

    json_files = [f for f in os.listdir(directory_path) if f.endswith(".json")]
    if len(json_files) != 1:
        raise ValueError("There should be exactly one JSON file in the directory.")
    return os.path.join(directory_path, json_files[0])


# Check for path, create if does not exist
def ensure_path_exists(path):
    path = os.path.join(path, "")
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)
        logging.debug(f"Created {dir}")
    return dir
