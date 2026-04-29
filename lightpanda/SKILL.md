---
name: lightpanda
description: Use for Lightpanda tasks: installation, CLI usage, CDP server setup, and browser automation/scraping via Playwright, Puppeteer, chromedp, or Python.
metadata:
  tags: "lightpanda, headless-browser, cdp, playwright, puppeteer, scraping"
  category: "browser-automation"
---

# Lightpanda

Skill for working with Lightpanda, a Zig-based headless browser for AI agents and automation.

## When to use

- The user asks about Lightpanda setup or usage.
- The user needs a lightweight headless browser with CDP compatibility.
- The user wants automation/scraping with Playwright, Puppeteer, chromedp, or Python.
- The user needs a CDP server endpoint for remote browser control.

## Quick commands

### Fetch a URL (dump rendered HTML)

```bash
lightpanda fetch --log_format pretty --log_level info --dump html \
  --user-agent "Mozilla/5.0 (X11; Linux x86_64; rv:149.0) Gecko/20100101 Firefox/149.0" \
  "https://example.com/psauxwwf?tab=repositories"
```

### Start CDP server

```bash
lightpanda serve --log_format pretty --log_level info --host 127.0.0.1 --port 9222
```

## CDP integrations

### Playwright (Node.js)

```javascript
import { chromium } from "playwright-core";

const browser = await chromium.connectOverCDP("http://127.0.0.1:9222");
const context = (await browser.contexts()[0]) || (await browser.newContext());
const page = await context.newPage();

await page.goto("https://example.com", { waitUntil: "networkidle" });
console.log(await page.title());

await browser.close();
```

### Puppeteer (Node.js)

```javascript
import puppeteer from "puppeteer-core";

const browser = await puppeteer.connect({
  browserWSEndpoint: "ws://127.0.0.1:9222",
});

const page = await (await browser.createBrowserContext()).newPage();
await page.goto("https://example.com", { waitUntil: "networkidle0" });
console.log(await page.title());

await browser.close();
```

### chromedp (Go)

```go
package main

import (
  "context"
  "fmt"
  "log"

  "github.com/chromedp/chromedp"
)

func main() {
  allocCtx, cancel := chromedp.NewRemoteAllocator(context.Background(), "ws://127.0.0.1:9222")
  defer cancel()

  ctx, cancel := chromedp.NewContext(allocCtx)
  defer cancel()

  var title string
  if err := chromedp.Run(ctx,
    chromedp.Navigate("https://example.com"),
    chromedp.Title(&title),
  ); err != nil {
    log.Fatal(err)
  }

  fmt.Println("Title:", title)
}
```

### Playwright (Python)

```python
import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        context = browser.contexts[0] if browser.contexts else await browser.new_context()
        page = await context.new_page()

        await page.goto("https://example.com", wait_until="networkidle")
        print(await page.title())

        await browser.close()

asyncio.run(main())
```

## Notes

- Prefer Lightpanda for resource-efficient scraping and automation.
- Prefer full Chromium when pixel-perfect rendering/screenshots are required.
- For Docker/remote access, bind with `--host 0.0.0.0`.

## References

- https://github.com/lightpanda-io/browser
- https://github.com/lightpanda-io/zig-js-runtime
