from re import match, search

from bs4 import BeautifulSoup as bs
from jsbeautifier import beautify
from requests import get


def get_MaxStream_download_link(url):
    try:
        soup = bs(get(url).content, "html.parser")
        script = [
            script.contents[0]
            for script in soup.findAll("script", {"type": "text/javascript"})
            if match("eval", (c := script.contents) and str(c[0]) or "")
        ][0]
        script_unpacked = beautify(script)
        return search(r"src:\s+\"(.*)\"", script_unpacked).group(1)
    except Exception:
        return None
