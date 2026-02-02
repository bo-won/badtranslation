import re
import urllib.request
from pathlib import Path

DOC_ID = "1r97FlQiwhxuOgarlIuaYIPhX5TTORU5Nm-jXGh_beTw"
EXPORT_URL = f"https://docs.google.com/document/d/{DOC_ID}/export?format=html"
EDIT_URL = f"https://docs.google.com/document/d/{DOC_ID}/edit"

OUT = Path("index.html")  # change to Path("docs/index.html") if your Pages source is /docs

CSS = """
<style>
  :root { color-scheme: light; }
  html, body { margin: 0; padding: 0; background: #fff; }
  body { font: 16px/1.55 system-ui, -apple-system, Segoe UI, Roboto, sans-serif; color: #000; }

  .wrap { max-width: 900px; margin: 0 auto; padding: 18px 16px 64px; }

  /* Make exported Doc images responsive */
  img { max-width: 100% !important; height: auto !important; }

  /* Tables can overflow on mobile */
  table { max-width: 100%; display: block; overflow-x: auto; }

  /* Optional: small fixed “Edit” link */
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

def fetch_html(url: str) -> str:
  req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
  with urllib.request.urlopen(req) as r:
    return r.read().decode("utf-8", errors="replace")

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
  html = fetch_html(EXPORT_URL)
  OUT.write_text(make_page(html), encoding="utf-8")
  print("Wrote", OUT)
