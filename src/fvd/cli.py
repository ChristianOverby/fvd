"""
This module provides a command-line interface for downloading videos from Facebook.
It uses the Typer library to create commands for single and bulk video downloads.
Commands:
- single: Download a single Facebook video using its URL.
    Arguments:
        - url (str): The Facebook video URL to process.
        - output_dir (str): Directory to save the downloaded video (default: current directory).
        - format (str): Video export format (default: "mp4").
        - custom_title (str | None): Custom filename for the downloaded video (optional).
        - impersonate (str): Browser impersonation to allow file download (default: "chrome-99").
- bulk: Download multiple videos from a Facebook media page URL.
    Arguments:
        - url (str): The Facebook media page URL to process.
        - output_dir (str): Directory to save the downloaded videos (default: current directory).
        - format (str): Video export format (default: "mp4").
        - wait_time (float): Time to wait for JavaScript to load before scrolling the page (default: 2.0 seconds).
        - scroll (bool): Whether or not to scroll the page (default: True).
        - scroll_iterations (int): Maximum number of scrolls before exiting (default: 20).
        - impersonate (str): Browser impersonation to allow file download (default: "chrome-99").
        - headless (bool): Whether or not to run the browser in headless mode (default: True).
Usage:
Run the script from the command line to access the commands.
"""
from pathlib import Path

import typer
from rich.console import Console
from fvd.downloader import single_download
from fvd.scraper import dump_html
from fvd.parser import find_video_urls

app = typer.Typer(rich_markup_mode="rich")

console = Console()


@app.command()
def single(
    url: str = typer.Argument(..., help="The Facebook video URL to process"),
    output_dir: str = typer.Option(
        ".", "--out", "-o", help="Directory to save the downloaded video"
    ),
    format: str = typer.Option("mp4", "--type", help="Video export format"),
    custom_title: str | None = typer.Option(
        None, "--title", "-t", help="Custom filename"
    ),
    impersonate: str = typer.Option(
        "chrome-99", help="Browser impersonation to get file download allowed"    ),
) -> None:
    """
    Download a Facebook video by fetching media off a Facebook video url
    """
    confirm = input("This script will read your Firefox Facebook session cookies. Continue? [y/n]")
    if confirm.lower() != "y":
        raise SystemExit("Cancelled.")
    console.print(f"Step 1: Fetching media from [bold blue]{url}[/bold blue]")
    path = single_download(
        url,
        custom_title=custom_title,
        format=format,
        impersonate=impersonate,
        output_dir=output_dir,
    )
    console.print(
        f"Step 2: Video downloaded to [bold green]{path.resolve()}[/bold green]"
    )


@app.command()
def bulk(
    url: str = typer.Argument(..., help="The Facebook media page URL to process"),
    output_dir: str = typer.Option(
        ".", "--out", "-o", help="Directory to save the downloaded video"
    ),
    format: str = typer.Option("mp4", "--type", help="Video export format"),
    wait_time: float = typer.Option(
        2.0, help="Time to wait for javascript to load before scrolling the page"
    ),
    scroll: bool = typer.Option(True, help="Whether or not to scroll"),
    scroll_iterations: int = typer.Option(
        20, help="Maximum amount of scrolls before exit"
    ),
    impersonate: str = typer.Option(
        "chrome-99", help="Browser impersonation to get file download allowed"
    ),
    headless: bool = typer.Option(
        True, help="Whether or not to run the automated browser in headless mode"
    ),
) -> None:
    """
    Download Facebook videos from a facebook group media url

    Attempts to extract downloadable video URLs from the page and
    save the selected format using the configured browser impersonation.
    """
    console.print(
        f"Step 1: Scraping the media html from [bold blue]{url}[/bold blue]..."
    )
    confirm = input("This script will read your Firefox Facebook session cookies. Continue? [[y/n]]")
    if confirm.lower() != "y":
        raise SystemExit("Cancelled.")
    html = dump_html(
        url,
        wait_time=wait_time,
        scroll=scroll,
        scroll_max=scroll_iterations,
        headless=headless,
    )
    console.print(f"Step 2: Parsing the media html for video urls")
    urls, titles = find_video_urls(html)
    for i, (url, title) in enumerate(zip(urls, titles), start=1):
        console.print(
            f"Downloading video {i}/{len(urls)}: [bold blue]{title}[/bold blue] from [bold blue]{url}[/bold blue]..."
        )
        single_download(
            url,
            custom_title=title,
            format=format,
            impersonate=impersonate,
            output_dir=output_dir,
        )
    path = Path(output_dir).resolve()
    console.print(f"Step 3: All videos downloaded to [bold green]{path}[/bold green]")


if __name__ == "__main__":
    app()


