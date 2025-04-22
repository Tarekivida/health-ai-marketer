from agents.pharmacist_expert import pharmacist_expert
from agents.extraction import extract
from agents.product_research_agent import product_research_agent
from agents.product_scraper_agent import fetch_product_details
from agents.pharmacist_reviewer import pharmacist_reviewer
import sys
import os

# Package: agents
# Developer: Import new agent modules here when extending functionality.

# Add project root directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.marketing_content_specialist import rewrite_article_with_products


__all__ = [
    "pharmacist_expert",
    "extract",
    "product_research_agent",
    "fetch_product_details",
    "marketing_content_specialist",
    "pharmacist_reviewer",
]