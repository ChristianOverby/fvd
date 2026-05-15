"""
This module provides functionality to scrape HTML content from webpages using Selenium WebDriver.
It includes methods to create a WebDriver instance, access cookies from a local Firefox browser,
scroll to the bottom of a page to load dynamic content, and save the accessed HTML to a file.
Functions:
- _create_driver(headless: bool) -> webdriver.Firefox:
    Creates a Firefox WebDriver instance with optional headless mode.
- access_cookies(driver: webdriver.Firefox) -> None:
    Injects cookies from the local Firefox browser into the Selenium WebDriver instance.
- _scroll_to_bottom(driver: webdriver.Firefox, wait_time: float, scroll_max: int) -> None:
    Continuously scrolls to the bottom of the page to load all dynamic content.
- dump_html(url: str, scroll: bool, wait_time: float, scroll_max: int, headless: bool) -> str:
    Dumps the HTML content of a webpage using Selenium WebDriver with cookies from the local Firefox browser.
- save_html(url: str, output_dir: str, scroll: bool, wait_time: float, scroll_max: int) -> Path:
    Saves the dumped HTML content of a webpage to a file in the specified output directory.
"""

import time
from pathlib import Path

import browser_cookie3
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .utils import safe_filename


def _create_driver(headless:bool = True) -> webdriver.Firefox:
    """
    Create Firefox webdriver instance

    Parameters
    ----------
    headless : bool, optional
        Whether to run the browser in headless mode (default is True)

    Returns
    ----------
    webdriver.Firefox
        A firefox selenium webdriver
    """
    firefox_options = Options()
    if headless:
        firefox_options.add_argument("--headless")
    return webdriver.Firefox(options=firefox_options)


def access_cookies(driver: webdriver.Firefox) -> None:
    """
    Inject cookies from the local Firefox browser into the Selenium WebDriver instance

    Parameters
    ----------
    driver : webdriver.Firefox
        The Selenium WebDriver instance to inject cookies into
    
    """
    driver.get("https://www.facebook.com")

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )
    cookies = browser_cookie3.firefox(domain_name="facebook.com")

    for cookie in cookies:
        cookie_dict = {
            "name": cookie.name,
            "value": cookie.value,
            "path": cookie.path,
            "domain": cookie.domain,
            "secure": bool(cookie.secure),
            "httpOnly": bool(cookie.has_nonstandard_attr("HttpOnly")),
        }
        if cookie.expires:
            cookie_dict["expiry"] = cookie.expires
        if cookie.has_nonstandard_attr("SameSite"):
            cookie_dict["samesite"] = cookie.get_nonstandard_attr("SameSite")

        try:
            driver.add_cookie(cookie_dict)
        except Exception as e:
            print(f"Error adding cookie: {e}")
            pass


def _scroll_to_bottom(
    driver: webdriver.Firefox, wait_time: float = 2.0, scroll_max: int = 20
) -> None:
    """
    Continously scroll to the bottom of the page to load all dynamic content

    Parameters
    ----------
    driver : webdriver.Firefox
        The Selenium WebDriver instance
    wait_time : float, optinal
        Time to wait for new content to load after scrolling (default is 2 seconds)
    scroll_max : int, optional
        Maximum number of scroll attempts to prevent infinite scrolling (default is 20)
    """
    for _ in range(scroll_max):
        last_height = driver.execute_script("return document.body.scrollHeight")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(wait_time)  # Wait for new content to load

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break


def dump_html(
    url: str,
    scroll: bool = True,
    wait_time: float = 2.0,
    scroll_max: int = 20,
    headless: bool = True,
) -> str:
    """
    Dump the HTML content of a webpage using Selenium WebDriver with cookies from the local Firefox browser.

    Parameters
    ----------
    url : str
        The URL of the webpage to dump
    scroll : bool, optional
        Whether to scroll to the bottom of the page to load all content (default is True)
    wait_time : float, optional
        Time to wait for new content to load after scrolling (default is 2 seconds)
    scroll_max : int, optional
        Maximum number of scroll attempts to prevent infinite scrolling (default is 20)
    headless : bool, optional
        Whether to run the browser in headless mode (default is True)
        
    Returns
    ----------
    str
        A string containing the html of the url
    """
    driver = _create_driver(headless=headless)

    try:
        access_cookies(driver)
        driver.get(url)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        if scroll:
            _scroll_to_bottom(driver, wait_time=wait_time, scroll_max=scroll_max)
        return driver.page_source

    finally:
        driver.quit()


def save_html(
    url: str,
    output_dir: str = ".",
    scroll: bool = True,
    wait_time: float = 2.0,
    scroll_max: int = 20,
) -> Path:
    """
    Save the dumped HTML content of a facebook page to a file in the specified output directory. The filename is generated from the URL.

    Parameters
    ----------
    url : str
        The URL of the webpage to dump
    output_dir : str, optional
        The directory to put the scraped html (default is the current working directory)
    scroll : bool, optional
        Whether to scroll to the bottom of the page to load all content (default is True)
    wait_time : float, optional
        Time to wait for new content to load after scrolling (default is 2 seconds)
    scroll_max : int, optional
        Maximum number of scroll attempts to prevent infinite scrolling (default is 20)

    Returns
    ----------
    Path
        The absolute path to the saved HTML file
    """
    # not yet implemnted in the CLI
    html = dump_html(url, scroll=scroll, wait_time=wait_time, scroll_max=scroll_max)
    filename = safe_filename(url)
    output_path = Path(f"{output_dir}") / f"{filename}.html"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    output_path.write_text(html, encoding="utf-8")

    return output_path
