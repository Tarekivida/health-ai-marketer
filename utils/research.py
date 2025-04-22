import requests

def search_products(query):
    """Search for products using an external API or search engine."""
    searx_url = "http://localhost:8888/search"  # Update with correct SearXNG instance
    params = {"q": query, "format": "json", "categories": "shopping"}
    
    response = requests.get(searx_url, params=params)
    if response.status_code != 200:
        return {"error": "Failed to fetch search results"}

    results = response.json().get("results", [])
    return [{"title": res["title"], "link": res["url"]} for res in results]