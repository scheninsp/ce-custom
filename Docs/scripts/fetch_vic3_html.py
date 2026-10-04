from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright


DEFAULT_URL = "https://vic3.paradoxwikis.com/Market#Tariffs_and_subventions"
ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = ROOT / "Docs" / "netdata"


def safe_name(value: str) -> str:
    value = re.sub(r"[^A-Za-z0-9._-]+", "_", value)
    return value.strip("._-") or "page"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="使用 Playwright 访问 Victoria 3 Wiki 并保存完整渲染 HTML。"
    )
    parser.add_argument("--url", default=DEFAULT_URL)
    parser.add_argument("--headed", action="store_true", help="显示浏览器窗口")
    parser.add_argument("--keep-images", action="store_true", help="不拦截图片请求")
    parser.add_argument("--wait-ms", type=int, default=3000)
    args = parser.parse_args()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    stem = f"{safe_name(args.url.split('#')[0].rstrip('/').split('/')[-1])}_{stamp}"
    html_path = OUTPUT_DIR / f"{stem}.html"
    screenshot_path = OUTPUT_DIR / f"{stem}.png"
    meta_path = OUTPUT_DIR / f"{stem}.txt"

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=not args.headed)
        context = browser.new_context(
            viewport={"width": 1366, "height": 900},
            locale="en-US",
            timezone_id="UTC",
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/131.0.0.0 Safari/537.36"
            ),
        )

        if not args.keep_images:
            def route_handler(route):
                if route.request.resource_type == "image":
                    route.abort()
                else:
                    route.continue_()

            context.route("**/*", route_handler)

        page = context.new_page()
        status = "unknown"
        error = ""

        try:
            response = page.goto(
                args.url,
                wait_until="domcontentloaded",
                timeout=60_000,
            )
            if response is not None:
                status = str(response.status)

            page.wait_for_selector("#mw-content-text", timeout=30_000)
            page.wait_for_timeout(max(args.wait_ms, 0))
            page.evaluate(
                """
                async () => {
                    window.scrollTo(0, document.body.scrollHeight);
                    await new Promise(resolve => setTimeout(resolve, 1000));
                    window.scrollTo(0, 0);
                }
                """
            )

            if args.headed:
                input("如需手动完成验证，请完成后按 Enter 继续保存：")

        except PlaywrightTimeoutError as exc:
            error = f"timeout: {exc}"
            print(f"警告：页面等待超时，将保存当前页面：{exc}", file=sys.stderr)
        except Exception as exc:
            error = f"{type(exc).__name__}: {exc}"
            print(f"页面访问失败，将尝试保存当前页面：{exc}", file=sys.stderr)
        finally:
            try:
                html_path.write_text(page.content(), encoding="utf-8")
                page.screenshot(path=str(screenshot_path), full_page=True)
                meta_path.write_text(
                    f"url={args.url}\n"
                    f"title={page.title()}\n"
                    f"status={status}\n"
                    f"saved_at_utc={datetime.now(timezone.utc).isoformat()}\n"
                    f"error={error}\n",
                    encoding="utf-8",
                )
                print(f"HTML: {html_path}")
                print(f"截图: {screenshot_path}")
                print(f"元数据: {meta_path}")
            finally:
                context.close()
                browser.close()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
