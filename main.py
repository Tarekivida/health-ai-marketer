#!/usr/bin/env python
import sys
import json
import os
import traceback
import datetime
from agents.pharmacist_expert import pharmacist_expert, generate_article
from agents.extraction import extract
from agents.product_research_agent import product_research_agent, research_products
from agents.product_scraper_agent import fetch_product_details
from agents.marketing_content_specialist import rewrite_article_with_products
from agents.pharmacist_reviewer import pharmacist_reviewer

__all__ = [
    "pharmacist_expert",
    "extract",
    "product_research_agent",
    "fetch_product_details",
    "marketing_content_specialist",
    "pharmacist_reviewer",
]

# Developer: Entry script orchestrating the full article generation and marketing pipeline.

# Developer: Utility function to save text content to a markdown file.
def save_to_markdown(folder, filename, content):
    """Helper function to save content to a markdown file."""
    filepath = os.path.join(folder, filename)
    with open(filepath, "w", encoding="utf-8") as file:
        file.write(content)

# Developer: Coordinates user input, article generation, product extraction, scraping, and content rewriting.
def run_pipeline():
    topic = input("Enter the health topic you want to write about: ").strip()
    if not topic:
        print("❌ Error: Topic cannot be empty.")
        sys.exit(1)

    # Ensure all output is stored in ./articles/TOPIC
    base_path = os.path.join(os.getcwd(), "articles", topic.replace(" ", "_"))
    os.makedirs(base_path, exist_ok=True)

    # Generate a timestamped subfolder to store this run’s output
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    folder_path = os.path.join(base_path, timestamp)
    os.makedirs(folder_path, exist_ok=True)

    # Step 1: Generate the health article based on user topic.
    print(f"\n🚀 Generating article for topic: {topic}...\n")
    try:
        article = generate_article(topic)
        print(f"\n✅ Article generated successfully!\n{article}\n")

        # Save article to file
        save_to_markdown(folder_path, "article.txt", f"# Article\n\n{article}")
    except Exception as e:
        print(f"\n❌ Error generating article: {e}")
        sys.exit(1)

    # Step 2: Extract product information from the generated article.
    print("\n🔍 Extracting products and solutions...\n")
    try:
        product_json = extract(article)
        if product_json is None:
            print("\n❌ Error: No products extracted. Stopping execution.")
            sys.exit(1)

        formatted_products = json.dumps(product_json, indent=2, ensure_ascii=False)
        print(f"\n✅ Product extraction successful!\n{formatted_products}\n")

        # Save extracted products to file
        save_to_markdown(folder_path, "extracted_products.txt", f"# Extracted Products\n\n```json\n{formatted_products}\n```")
    except Exception as e:
        print(f"\n❌ Error in product extraction: {e}")
        sys.exit(1)

    # Step 3: Research actual products matching the extracted data.
    print("\n🔍 Finding matching products from Newpharma...\n")
    try:
        matching_products = research_products(json.dumps(product_json))
        matching_products = json.loads(matching_products)

        formatted_matching = json.dumps(matching_products, indent=2, ensure_ascii=False)
        print(f"\n✅ Matching products found!\n{formatted_matching}\n")

        # Save matching products to file
        save_to_markdown(folder_path, "matching_products.txt", f"# Matching Products\n\n```json\n{formatted_matching}\n```")
    except Exception as e:
        print(f"\n❌ Error in product research: {e}")
        sys.exit(1)

    # Step 4: Scrape details for each matched product via fetch_product_details.
    print("\n🔍 Extracting product content...\n")
    extracted_content = {}
    try:
        for category, products in matching_products.items():
            extracted_content[category] = []
            for product in products:
                product_details = fetch_product_details(product["url"])  # Updated to use fetch_product_details
                extracted_content[category].append(product_details)

        formatted_scraped = json.dumps(extracted_content, indent=2, ensure_ascii=False)
        print(f"\n✅ Product content extracted!\n{formatted_scraped}\n")

        # Save scraped product content to file
        save_to_markdown(folder_path, "scraped_info.txt", f"# Scraped Product Info\n\n```json\n{formatted_scraped}\n```")
    except Exception as e:
        print(f"\n❌ Error in product scraping: {e}")
        sys.exit(1)

    # Step 5: Rewrite the article to include product recommendations for marketing.
    print("\n🔍 Rewriting content for marketing...\n")
    try:
        final_content = rewrite_article_with_products(article, extracted_content)

        formatted_final = json.dumps(final_content, indent=2, ensure_ascii=False)
        print(f"\n✅ Marketing content finalized!\n{formatted_final}\n")

        # Save marketing content to file
        save_to_markdown(folder_path, "marketing_content.txt", f"# Marketing Content\n\n{formatted_final}")
    except Exception as e:
        print(f"\n❌ Error in marketing content adaptation: {e}")
        sys.exit(1)

    print("\n✅ All steps completed successfully!\n")

if __name__ == "__main__":
    # Developer: Execute run_pipeline when script is run directly.
    try:
        run_pipeline()
    except Exception as e:
        print("\n❌ Unexpected error occurred:")
        traceback.print_exc()
        sys.exit(1)