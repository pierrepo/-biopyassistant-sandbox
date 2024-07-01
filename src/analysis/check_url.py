""" Check if a URL is valid and if an anchor is valid.

This script reads a file containing URLs and checks if each URL is valid. If the URL is valid, it also checks if the anchor is valid.

Usage:
======
    python src/analysis/check_url.py <file_name>

Arguments:
==========
    file_name: str
        The path to the file containing URLs.

Example:
========
    python src/analysis/check_url.py chroma_db_chunks_details.txt

This command will read the file `chroma_db_chunks_details.txt` and check each URL in the file. 
If the URL is valid, it will also check if the anchor is valid.

"""

import sys
from urllib.parse import urlparse
from urllib.request import urlopen

from loguru import logger


def get_url(file_name):
    logger.info(f"Reading URLs from file: {file_name}")
    urls = set()
    with open(file_name, 'r') as f:
        for line in f:
            if "Url:" in line:
                url = line.split("Url:")[1].strip()
                urls.add(url)
    logger.success(f"Found {len(urls)} URLs in the file.")

    return urls


def is_valid_url(url):
    try:
        r = urlopen(url)
        return r.status == 200
    except Exception as e:
        return False


def is_valid_anchor(url):
    anchor = urlparse(url).fragment
    r = urlopen(url)
    if anchor not in str(r.read()):
        logger.info(f"Checking URL: {url}")
        logger.error("Anchor: ERROR")
       

if __name__ == "__main__":
    # Get the file name from the command line
    if len(sys.argv) != 2:
        sys.exit("Error! Need exactly one argument: the path to the file containing URLs.")
    
    file_name = sys.argv[1]

    # Get the URLs from the file and check each URL
    urls = get_url(file_name)
    for url in urls:
        if not is_valid_url(url):
            logger.info(f"Checking URL: {url}")
            logger.error("URL: ERROR")
        else:
            if "#" in url:
                is_valid_anchor(url)

    logger.success("Done checking URLs.")
    
