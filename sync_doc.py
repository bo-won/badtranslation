import re
import time
import urllib.request
from urllib.error import HTTPError, URLError
from pathlib import Path

DOC_ID = "1r97FlQiwhxuOgarlIuaYIPhX5TTORU5Nm-jXGh_beTw"

# Primary export endpoint (sometimes flaky)
EXPORT_URL = f"https://docs.google.com/document/d/{DOC_ID}/export?format=html"

# OPTIONAL but recommended: Publish-to-web fallback URL
# To get this:
# Google Doc → File → Share → Publish to web → copy the link
# It will look like https://docs.google.com/document/d/e/XXXX/pub
PUBLISHED_URL = None  # ← paste published URL here as a string if you have it

EDIT_URL = f"https://docs.google.com/document/d/{DOC_ID}/edit"

OUT = Path("index.html")  # change to Path("docs/index.html") if Pages serves /docs

CSS = """
<style>
  :root { color-scheme: light; }
  html, body { margin: 0; padding: 0; background: #fff; }
  body {
    font: 16px/1.6 system-ui, -apple-system, Segoe UI, Roboto, sans-serif;
    color: #000;
  }

  .wrap {
    max-width: 900px;
    margin: 0 auto;
    padding: 20px 16px 80px;
  }

  /* Make images responsive */
  img { max-width: 100% !important; height: auto !important; }

  /* Tables can overflow on mobile */
  table { max-width: 100%; display: block; overflow-x: auto; }

  /* Remove some Google export clutter */
  .doc-title, .doc-author, .doc-date { display: none !important; }

  /* Floating Edit button */
  .edit {
    position: fixed;
    right: 12px;
    bottom: 12px;
    padding: 10px 12px;
    background: rgba(255,255,255,0.92);
    border: 1px solid rgba(0,0,0,0.12);
    border-radius: 999px;
    font: 14px/1 system-ui, -apple-system, Segoe UI, Roboto, sans-serif;
    text-decoration: none;
    color: #000;
    z-index: 10;
  }
</style>
"""

def fetch_with_retries(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    last_err = None

    for attempt in range(1, 6):
        try:
            print(f"Fetching (attempt {attempt}):", url)
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read().decode("utf-8", errors="replace")
        except (HTTPError, URLError) as e:
            print("Fetch error:", repr(e))
            last_err = e
            time.sleep(2 ** (attempt - 1))

    raise last_err


def extract_body(doc_html: str) -> str:
    m = re.search(r"<body[^>]*>(.*)</body>", doc_html, flags=re.S | re.I)
    return m.group(1) if m else doc_html


def make_page(doc_html: str) -> str:
    body = extract_body(doc_html)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
  <title>Bad Translation</title>
  {CSS}
</head>
<body>
  <div class="wrap">
    {body}
  </div>

  <a class="edit" href="{EDIT_URL}" target="_blank" rel="noopener">Edit</a>
</body>
</html>
"""


if __name__ == "__main__":
    try:
        html = fetch_with_retries(EXPORT_URL)
    except Exception as e:
        print("Primary export failed:", repr(e))
        if PUBLISHED_URL:
            print("Trying published fallback...")
            html = fetch_with_retries(PUBLISHED_URL)
        else:
            raise

    OUT.write_text(make_page(html), encoding="utf-8")
    print("Wrote", OUT)
