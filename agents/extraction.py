# Module: extraction
# Description: Extracts product and solution mentions from article text via an LLM call.

import json
import sys
import re
import requests

from utils.llm_config import local_llm_config  # Ensure correct config import

# Ensure the config exists before initializing
if not local_llm_config.get("config_list"):
    raise ValueError("❌ Error: `local_llm_config` is missing required LLM configuration.")

# Developer: extract constructs a prompt for Ollama, sends the request, and parses JSON from the response.
def extract(article):
    """
    Extracts products and solutions mentioned in the given article text using Ollama.
    Returns a JSON dictionary with relevant extracted information.
    """
    print("🔍 Extracting product and solution data from the article using Ollama...")

    try:
        # Step: Build the system prompt instructing the LLM to output structured JSON in French.
        system_message = (
            "Extrayez les produits et solutions mentionnés dans le texte fourni et retournez-les sous forme de dictionnaire JSON structuré. "
            "Format: {\"produits\": [{\"nom\": \"Nom du produit\", \"catégorie\": \"Catégorie\"}], "
            "\"solutions\": [\"Solution 1\", \"Solution 2\"]}. Le contenu doit être en français."
        )
        full_prompt = system_message + "\n\n" + article

        llm_url = local_llm_config["config_list"][0]["base_url"] + "/api/generate"
        payload = {
            "model": local_llm_config["config_list"][0]["model"],
            "prompt": full_prompt,
            "stream": False
        }

        response = requests.post(llm_url, json=payload)
        response.raise_for_status()
        raw_response = response.json().get("response", "")

        print("🔍 Raw Response from Ollama:", raw_response)

        # Use regex to extract JSON content
        json_match = re.search(r'\{.*\}', raw_response, re.DOTALL)
        if not json_match:
            print("❌ Error: No valid JSON found in the response.")
            return None

        cleaned_response = json_match.group(0).strip()

        try:
            extracted_data = json.loads(cleaned_response)
            print(json.dumps(extracted_data, indent=4))
            return extracted_data
        except json.JSONDecodeError:
            print("❌ Error: Failed to parse extracted data as JSON.")
            return None

    # Developer: Catch-all to handle unexpected extraction errors.
    except Exception as e:
        print(f"❌ Unexpected error during extraction: {e}")
        return None