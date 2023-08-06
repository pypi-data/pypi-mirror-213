import logging
import os

import reddit2pdf.library as library


def download_reddit_url(url: str, download_dir: str = None) -> str:
    """
    Downloads a Reddit URL using bulk-downloader-for-reddit and saves it to the specified directory.

    :param url: The Reddit URL to download.
    :param dir: The directory where the downloaded files should be saved.
    """
    # Create directory if required
    if not os.path.exists(download_dir):
        logging.info(f"Directory did not exist. Creating {download_dir}")
        os.mkdir(download_dir)

    assert library.is_reddit_url(url), f"Url was not a reddit URL: {url}"

    # BDFR only takes http start
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    # Define the command to execute
    # Primarily running on macos
    # Set format to JSON for easy python loading
    # Adust filename for readability
    # Required separate log. Assumes no download to same download_dir simultaneously
    # Adjust default folder scheme since we dont care about nested folders
    # NULL folder scheme to prevent subdirs
    cmd = f"bdfr clone {download_dir} --filename-restriction-scheme linux \
        --authenticate --format json --file-scheme {{SUBREDDIT}}_{{POSTID}} \
        --link {url} --log {os.path.join(download_dir, 'bdfr.log')} --folder-scheme ''"

    # Run the command with logging
    library.run_command(cmd)

    # Check that the JSON file exists in the directory
    json_file = os.path.join(
        download_dir, f"{url.split('/')[-5]}_{url.split('/')[-3]}.json"
    )
    assert os.path.exists(json_file), f"JSON file '{json_file}' does not exist"

    return download_dir
