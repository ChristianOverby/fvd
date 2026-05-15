"""
This module provides functionality to scrape HTML content from webpages using Selenium WebDriver.
It includes methods to create a WebDriver instance, inject cookies from a local Firefox browser,
scroll to the bottom of a page to load dynamic content, and save the scraped HTML to a file.
Functions:
- find_video_urls(html: str) -> tuple:
    Parses the HTML content of a Facebook media page to find video URLs and their titles.
"""


from bs4 import BeautifulSoup
from .utils import truncate, safe_filename


def find_video_urls(html: str) -> tuple:
    """
    Parse HTML content of a Facebook page media page to find video URLs and their titles

    Parameters
    ----------
    html : str
        The HTML content of the Facebook media page to parse'
    
    Returns
    ----------
    tuple
        A tuple containing a list of video URLs and a list of corresponding video titles
    """
    soup = BeautifulSoup(html, "html.parser")

    urls = []
    titles = []

    for a in soup.find_all("a", href=True):
        href = a["href"]

        if "facebook.com" not in href:
            continue

        if "/videos/" not in href and "watch/?v=" not in href:
            continue

        img = a.find("img")

        if img and img.get("alt"):
            title = safe_filename(truncate(img["alt"]))
        else:
            title = safe_filename(truncate(href))

        urls.append(href)
        titles.append(title)

    print(titles)
    return urls, titles