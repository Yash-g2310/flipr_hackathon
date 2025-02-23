import asyncio
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError

url = "https://www.ndtv.com/search?searchtext="
async def ndtv_topic_scraper(url: str, topics: list, max_articles: int = 10):

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        links = []
        for topic in topics:
            formatted_topic = topic.lower().replace(" ", "-")
            search_url = f"{url}{formatted_topic}"

            try:
                await page.goto(search_url, timeout=20000)  # Timeout handling
                await page.wait_for_selector(".SrchLstPg_ttl", timeout=10000)

                # Extract links
                topic_links = await page.eval_on_selector_all(
                    "a.SrchLstPg_ttl", "elements => elements.map(el => el.href)"
                )
                topic_links = topic_links[:min(max_articles, len(topic_links))]
                links.append((topic_links, topic))

            except PlaywrightTimeoutError:
                print(f"❌ Timeout! Skipping: {search_url}")
                continue

        news = []
        for topic_links, topic in links:
            for url in topic_links:
                page = await browser.new_page()
                try:
                    await page.goto(url, timeout=20000)

                    # Extract article details
                    heading = await page.text_content("h1.sp-ttl") or "N/A"
                    time = await page.text_content("span.pst-by_lnk") or "N/A"
                    content = " ".join(await page.locator("div.Art-exp_cn p").all_inner_texts())

                    news.append({"title": heading, "date_time": time, "content": content, "topic": topic})
                
                except PlaywrightTimeoutError:
                    print(f"❌ Timeout! Skipping: {url}")
                    continue

                await page.close()

        # Close the browser
        await browser.close()

        return news
