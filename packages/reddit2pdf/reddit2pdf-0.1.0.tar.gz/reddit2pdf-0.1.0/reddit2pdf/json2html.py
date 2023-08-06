import json
import logging
import os

import reddit2pdf.bdfrjsonhelper as bdfrjsonhelper
import reddit2pdf.htmlwriter as htmlwriter
import reddit2pdf.library as library

logger = logging.getLogger(__name__)


# Input: Path to BDFR download directory containing the JSON file + any media
# Output: Path to temporary directory containing HTML + media (should be the same folder)
def generate_reddit_post_html(bdfr_json_dir: str) -> str:
    if not os.path.exists(bdfr_json_dir):
        raise ValueError(f"BDFR directory did not exist: {bdfr_json_dir}")

    bdfr_json_path = library.get_json_file_path(bdfr_json_dir)

    with open(bdfr_json_path) as fh:
        post = json.load(fh)
        logging.debug(f"Loaded {bdfr_json_path}")

        if post.get("id") is not None:
            logging.debug(f"Imported  {bdfr_json_path}")

        try:
            post = bdfrjsonhelper.handle_comment_links(post)
            post = bdfrjsonhelper.recover_deleted_comments(post)
            post = bdfrjsonhelper.recover_deleted_post(post)
            post = bdfrjsonhelper.get_sub_from_post(post)

            # Move + log media
            post = htmlwriter.find_matching_media(post, bdfr_json_dir, bdfr_json_dir)

            # Create HTML collateral
            htmlwriter.write_post_to_file(post, bdfr_json_dir)
            htmlwriter.populate_css_file(bdfr_json_dir)
        except Exception as e:
            logging.error(f"Processing post {post['id']} has failed due to: {str(e)}")

    return bdfr_json_dir
