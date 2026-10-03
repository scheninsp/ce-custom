---
name: vic3-web-fetch
description: Fetch Victoria 3 Wiki or other permitted web pages with the project's Playwright browser script, saving rendered HTML and metadata under Docs/netdata. Use when current webpage text is needed and the MediaWiki API should not be used.
---

# Victoria 3 Web Fetch

Use this skill to retrieve webpage content through a normal Chromium browser session. Do not use the site's Wiki API for this workflow.

## Requirements

The project script requires Playwright and its Chromium browser:

```bash
pip install playwright
playwright install chromium
```

## Standard command

Run from the repository root:

```bash
python Docs/scripts/fetch_vic3_html.py --url "https://vic3.paradoxwikis.com/Market#Tariffs_and_subventions"
```

If no `--url` is supplied, the script uses the Market page and its `Tariffs_and_subventions` anchor by default.

## Output

The script writes timestamped files to `Docs/netdata/`:

- `.html`: complete rendered HTML returned by Playwright after page scripts run
- `.png`: full-page screenshot for checking page state or an access challenge
- `.txt`: URL, page title, HTTP status, timestamp, and any error

Images are blocked by default, but image tags and URLs that are part of the HTML may still occur in the saved document. To allow image requests, use:

```bash
python Docs/scripts/fetch_vic3_html.py --url "URL" --keep-images
```

## Access challenges

If the site presents a browser verification page, do not attempt to bypass it. Retry with a visible browser:

```bash
python Docs/scripts/fetch_vic3_html.py --url "URL" --headed
```

The user may complete any permitted manual verification in the opened browser and press Enter in the terminal. Do not implement CAPTCHA solving, fingerprint evasion, proxy rotation, or other bypasses.

## After fetching

1. Inspect the `.txt` metadata file and screenshot.
2. Read the saved `.html` with the repository file-reading tools.
3. Extract only the text or sections needed for the user's question.
4. Prefer the newest successful capture and avoid repeated requests.
5. Keep fetched data in `Docs/netdata/`; do not commit unrelated generated files unless requested.

## Limitations

The script saves the final DOM using Playwright's `page.content()`. It does not create a full offline copy of every CSS, JavaScript, or network resource. A timeout may still produce a partial HTML capture, which must be checked using the metadata and screenshot.
