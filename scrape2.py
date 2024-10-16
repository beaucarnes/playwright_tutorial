from playwright.sync_api import sync_playwright

def scrape_quotes(playwright):
    browser = playwright.chromium.launch()
    page = browser.new_page()
    page.goto('http://quotes.toscrape.com')

    quotes = page.locator('.text').all_text_contents()
    for quote in quotes:
        print(quote)

    browser.close()

with sync_playwright() as playwright:
    scrape_quotes(playwright)