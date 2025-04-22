import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.product_research_agent import research_products

# Contenu fictif pour le test avec une structure correcte
dummy_data = {
    "products": [  # Change "produits" to "products"
        {"name": "Vitamine D", "category": "Nutrition"},  # Change "nom" to "name" and "catégorie" to "category"
        {"name": "Fer", "category": "Minéraux"},
        {"name": "Zinc", "category": "Minéraux"},
        {"name": "Biotine", "category": "Vitamines et minéraux essentiels"},
        {"name": "Acide folique", "category": "Vitamines et minéraux essentiels"}
    ],
    "solutions": ["Suppléments alimentaires"]
}

def test_product_search():
    print("🔍 Running Product Search Test...")
    
    # Exécuter la recherche de produits
    search_results = research_products(json.dumps(dummy_data))

    # Vérifier si la sortie est un dictionnaire valide
    if isinstance(search_results, str):
        try:
            result_json = json.loads(search_results)
            print("✅ Test Passed: Output is valid JSON.")
            print(json.dumps(result_json, indent=2, ensure_ascii=False))
        except json.JSONDecodeError:
            print("❌ Test Failed: Output is not valid JSON.")
    else:
        print("❌ Test Failed: Output is not a valid JSON string.")

if __name__ == "__main__":
    test_product_search()