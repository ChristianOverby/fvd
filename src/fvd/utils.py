"""
Utility functions for the fvd package

Functions:
- safe_filename(s: str) -> str: 
    Converts a URL string into a filename-safe format by removing URL schemes and replacing special characters.
- truncate(s: str, limit: int = 32) -> str: 
    Truncates a string to a specified character limit without cutting off words in the middle.
"""

import re

def safe_filename(s:str) -> str:
    """
    Convert a URL string into a filename-safe format
    
    Parameters
    ----------
    s : str
        The input string to convert into a safe filename
    
    Returns
    ----------
    str
        A filename-safe version of the input string
    """
    s = re.sub(r'^[a-zA-Z]+://', '', s)   # remove http://, https://, ftp://
    s = re.sub(r'[ø]', 'oe', s)
    s = re.sub(r'[Ø]', 'Oe', s)
    s = re.sub(r'[å]', 'aa', s)
    s = re.sub(r'[Å]', 'Aa', s)
    s = re.sub(r'[æ]', 'ae', s)
    s = re.sub(r'[Æ]', 'Ae', s)
    s = re.sub(r"[^a-zA-Z0-9_-]+", "_", s)
    return s.strip('_')

def truncate(s:str, limit:int=32)-> str:
    """
    Tries to truncates a string to a specified character limit without cutting off words in the middle. 

    Parameters
    ----------
    s : str
        The string to truncate
    limit : int, optional
        The maximum number of characters to keep (default is 32)
    
    Returns
    ----------
    str
        The truncated string
    """
    # Honestly a pretty bad way to truncate works for now...
    s = s.replace('\n', ' ')
    truncated = re.search(fr'(.{{0,{limit}}})(?!\w)', s, re.DOTALL).group(1)

    return truncated