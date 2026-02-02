import re
import urllib.request
from pathlib import Path

DOC_ID = "1r97FlQiwhxuOgarlIuaYIPhX5TTORU5Nm-jXGh_beTw"
EXPORT_URL = f"https://docs.google.com/document/d/{DOC_ID}/export?format=html"

OUT = Path("index.html")  # change to Path("docs/index.html") if Pages serves /docs

CSS = """
<style>
  :root { color-scheme: light; }
  html, body { margin: 0; padding: 0; background: #fff; }
  body { font: 16px/1.55 system-ui, -apple-system, Segoe UI, Roboto, sans-serif; color: #000; }

  /* Responsive reading surface */
  .wrap { max-width: 900px; margin: 0 auto; padding: 18px 16px 64px; }

  /* Make exported Doc images responsive */
  img { max-width: 100% !important; height: auto !important; }

  /* Tables can overflow on mobile */
  table { max-width: 100%; display: block; overflow-x: auto; }

  /* Clean up some Google-export quirks */
  .doc-title, .doc-author, .doc-date { display: none !important; }
  p { margin: 0.65em 0; }
  a { color: inherit; text-decoration: underline; }

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
  }
</style>
"""

EDIT_URL_