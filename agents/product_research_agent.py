# Module: product_research_agent
# Description: Searches and researches products on Newpharma using a ConversableAgent and SearxNG.
from autogen import ConversableAgent
from utils.llm_config import local_llm_config
# Using Ollama configuration via local_llm_config for any potential LLM interactions.
import requests
import json

# Developer: Initialize the product_research_agent with local LLM configuration for downstream prompts.
# Initialize the agent
product_research_agent = ConversableAgent(
    name="product_research_agent",
    llm_config=local_llm_config,
)

# Developer: search_newpharma_products sends a query to SearxNG and filters top Newpharma results.
# Function to search for Newpharma products using SearxNG
def search_newpharma_products(product_name):
    search_url = "http://localhost:8080/search"
    params = {
        "q": f"{product_name} site:newpharma.be",
        "format": "json",
        "engines": "google",  # Use Google engine from SearxNG
        "categories": "general",
        "language": "fr"
    }

    try:
        response = requests.get(search_url, params=params)
        response.raise_for_status()
        search_results = response.json()

        # Extract up to 3 URLs from results
        products = [
            {"name": result["title"], "url": result["url"]}
            for result in search_results.get("results", [])
            if "newpharma.be" in result.get("url", "") 
            and not any(excluded in result.get("url", "") for excluded in ["/cat/", "/brands/", "/cnt/"])
        ][:3]  # Limit to top 3 results

        return products if products else None
    except requests.RequestException as e:
        print(f"❌ Error querying SearxNG: {e}")
        return None

# Developer: research_products parses JSON from LLM output and looks up matching product URLs on Newpharma.
# Function to process extracted products and find their URLs
def research_products(extracted_json):
    try:
        # Clean and extract JSON from the response
        cleaned_json = extracted_json.split('```json')[-1].split('```')[0].strip()
        extracted_data = json.loads(cleaned_json)

        if not isinstance(extracted_data, dict) or "produits" not in extracted_data:
            raise ValueError("❌ Extracted data is not in the expected format.")

        researched_products = {}

        for product in extracted_data["produits"]:  # Update key to match the extracted JSON
            product_name = product.get("nom")  # Update to "nom" instead of "name"
            if product_name:
                print(f"🔍 Searching for: {product_name} on Newpharma...")
                search_results = search_newpharma_products(product_name)
                if search_results:
                    researched_products[product_name] = search_results  # Now contains up to 3 results

        result_json = json.dumps(researched_products, indent=2, ensure_ascii=False)
        print(f"\n✅ Matching products found!\n{json.dumps(json.loads(result_json), indent=2, ensure_ascii=False)}\n")
        return result_json

    except json.JSONDecodeError:
        print("❌ Error: Failed to parse extracted data as JSON.")
        return None