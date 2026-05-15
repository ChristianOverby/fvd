"""
Module for downloading videos from Facebook using yt-dlp.
Functions:
- single_download(url: str, custom_title: str | None = None, format: str = 'mp4', 
                output_dir: str = ".", impersonate: str = 'chrome-99') -> Path:
    Downloads a single video from a Facebook video URL using yt-dlp and returns the path to the downloaded file.
- ulk_parallel(data: tuple, format: str = 'mp4', impersonate: str = 'chrome-99', 
              output_dir: str = ".") -> None:
    A parallel download of the files on a Facebook media page. To be implemented.
"""
import yt_dlp
from pathlib import Path
from yt_dlp.networking.impersonate import ImpersonateTarget

from fvd.utils import truncate

def single_download(url:str, 
                    custom_title:str | None = None, 
                    format:str='mp4',
                    output_dir:str = ".",
                    impersonate:str='chrome-99',
                    )->Path:
    """
    Download a single video from a Facebook video URL using yt-dlp.

    Parameters
    ----------
    url : str
        The Facebook video URL to download.
    custom_title : str | None, optional
        A custom filename for the downloaded video (default is None, which uses the video's title and id).
    format : str, optional
        The video format (default is 'mp4').
    output_dir : str, optional
        The directory to save the downloaded video (default is the current directory).
    impersonate : str, optional
        The browser impersonation target to use for downloading (default is 'chrome-99').
    
    Returns
    ----------
    Path
        The path to the downloaded video file.
    """

    # Define the filename template
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    filename = f"{truncate(custom_title, 20)}" if custom_title else "%(title)s [%(id)s]"

    template = str(out_path / f"{filename}")

    ydl_opts = {    
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': format,
        'cookiesfrombrowser': ("firefox",),
        'impersonate': ImpersonateTarget.from_str(impersonate),
        'outtmpl': template,
        'remux_video': format,
    }
    
    try:
        # Initialize and run yt-dlp
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Downloading video from: {url}")
            ydl.download([url])
    except Exception as e:
        print(f"Error downloading video: {e}")

    return out_path

def bulk_parallel(data:tuple, 
                  format:str='mp4', 
                  impersonate:str='chrome-99',
                  output_dir:str = "."
                  )->None:
    pass
    # A parallel download of the files on a facebook media page. To be implemented