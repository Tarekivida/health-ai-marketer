import sys
import os
import json

# Ensure the parent directory (project root) is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import local LLM config
from utils.llm_config import local_llm_config
from agents.marketing_content_specialist import rewrite_article_with_products

print("🔍 Debugging: LLM Config ->", local_llm_config)  # Now it should work

# Sample input for testing
test_article = """La vitamine C est essentielle pour protéger la membrane cellulaire contre le stress oxydatif.
On la trouve dans de nombreux aliments, comme les agrumes et les baies.
"""

test_extracted_content = {
    "Supplément en vitamine C": [
        {
            "title": "Davitamon Vitamine C Forte Time Release 42 Comprimés",
            "url": "https://www.newpharma.be/pharmacie/davitamon/825769/davitamon-vitamine-c-forte-time-release-42-comprimes.html",
            "price": "16,49"
        },
        {
            "title": "Solgar Vitamin C 500mg 90 Comprimés À Croquer",
            "url": "https://www.newpharma.be/pharmacie/solgar/865338/solgar-vitamin-c-500mg-90-comprimes-a-croquer.html",
            "price": "37,95"
        }
    ]
}

# Run the function
try:
    rewritten_article = rewrite_article_with_products(test_article, test_extracted_content)
    print("\n🔍 **Rewritten Article Output:**")
    print(rewritten_article)
except Exception as e:
    print(f"\n❌ **Error during test:** {e}")