# fvd

FVD (Facebook Video Downloader) is a Python wrapper around the `yt-dlp` module.

[![Python Version](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Release](https://img.shields.io/badge/release-v1.0-orange.svg)](https://github.com/ChristianOverby/fvd)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
## Introduction

FVD is a small CLI utility for bulk downloading media from Facebook groups and individual Facebook video URLs.

It simplifies authenticated downloads from private groups by using your existing logged-in Firefox session.

## License

FVD is released under the MIT License. See [LICENSE](LICENSE).

## Requirements

* Python 3.12+
* Firefox
* FFmpeg

FVD currently supports cookie extraction from Firefox only.

## Installation

This project uses [`uv`](https://github.com/astral-sh/uv) for dependency management.

### From source

1. **Clone the repository**

```bash
git clone https://github.com/ChristianOverby/fvd.git
cd fvd
```

2. **Install dependencies**

```bash
uv sync
```

Alternatively, create a virtual environment and install with:

```bash
pip install .
```

FVD depends on Firefox and FFmpeg being installed and available on your system.

## Usage

Before using this tool, please ensure you are comfortable with how it handles your data. FVD accesses your local Facebook session cookies to authenticate requests. Currently, FVD requires browser cookies for authentication. There is no built-in alternative authentication method.
Cookies are not stored or uploaded outside requests made directly to Facebook.
You will be prompted to confirm cookie access before downloading begins.

Downloaded files are saved to the current working directory unless otherwise specified.

Run the CLI with:
```bash
uv run fvd
```

View available commands and options:
```bash
uv run fvd --help
```

* Note
   If you installed with pip the CLI can be run with:
    ```bash
    fvd
    ```

Before downloading private content, open Firefox and log in to Facebook.

### Bulk download

Use `bulk` to download media from a Facebook group media page.

Example:

```bash
uv run fvd bulk https://www.facebook.com/groups/1234567891012345/media/videos
```

### Single download

Use `single` to download a single Facebook video.

Example:

```bash
uv run fvd single https://www.facebook.com/username/videos/1234567891012345/
```


## Security

Review the source code before use if you are handling sensitive accounts.

FVD does not store extracted cookies outside runtime memory or upload them anywhere other than authenticated requests made directly to Facebook.


## Disclaimer

FVD is an unofficial tool and is not affiliated with or endorsed by Facebook or Meta Platforms.

This tool accesses your local Firefox Facebook session cookies to authenticate requests as your logged-in account. By using this tool, you accept responsibility for your account security and browser session.

Use of this tool may be subject to Facebook's terms of service and applicable local laws. Use at your own discretion.
