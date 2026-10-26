from src.tools.tools import web_search, scrape_url

url = "give me latest news in AI"
results = web_search.invoke(url)
print(results)
url="https://aiweekly.co"
search_results = scrape_url.invoke(url)
print(search_results)