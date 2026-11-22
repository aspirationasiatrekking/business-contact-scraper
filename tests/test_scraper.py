from scraper.website import scrape_website

url = "https://example.com"

result = scrape_website(url)

if result:
    print("Title:", result["title"])
    print("Website:", result["website"])
    print("Emails:", result["emails"])
else:
    print("Scraping failed")