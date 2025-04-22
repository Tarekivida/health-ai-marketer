import requests
from autogen import ConversableAgent
from utils.llm_config import local_llm_config  # Import correct LLM config

# Developer: Uses ConversableAgent to rewrite articles, integrating product recommendations for SEO.

# Ensure the config exists before initializing
if not local_llm_config.get("config_list"):
    raise ValueError("❌ Error: `local_llm_config` is missing required LLM configuration.")

# Initialize the ConversableAgent
marketing_content_specialist = ConversableAgent(
    name="marketing_content_specialist",
    system_message="Vous êtes un spécialiste en marketing. Votre mission est de réécrire les articles pour intégrer les produits pertinents et optimiser le contenu pour le SEO.",
    llm_config=local_llm_config
)

# Developer: Builds LLM prompt to inject product mentions into the given article text.
def rewrite_article_with_products(article, extracted_content):
    if not article or not isinstance(article, str):
        raise ValueError("❌ Error: A valid article string is required.")
    if not extracted_content or not isinstance(extracted_content, dict):
        raise ValueError("❌ Error: Extracted content must be a valid dictionary.")

    # Step 1: Extract Relevant Products
    relevant_products = []
    for category, products in extracted_content.items():
        for prod in products:
            if prod["title"].lower() in article.lower():  # Simple keyword matching
                relevant_products.append(prod)

    if not relevant_products:
        print("⚠️ No directly relevant products found. Proceeding with general integration.")

    # Step 2: Format Product Mentions
    product_mentions = "\n\n".join(
        [f"- [{prod['title']}]({prod['url']}) - {prod['price']}€" for prod in relevant_products]
    ) or "No specific products matched. Please provide a general recommendation."

    # Step 3: Improved LLM Prompt
    prompt = f"""
    Vous êtes un spécialiste en marketing de contenu. Votre mission est de réécrire l'article suivant tout en intégrant de manière naturelle toutes les recommandations de produits extraites, y compris leurs liens et leurs prix.

    **Article original :**
    {article}

    **Produits à intégrer :**
    {product_mentions}

    **Directives :**
    - Assurez-vous que TOUS les produits extraits sont intégrés dans l'article.
    - Les recommandations de produits doivent être insérées de manière fluide et naturelle.
    - Mentionnez les noms des produits, leurs liens et leurs prix sans que cela paraisse promotionnel.
    - Préservez le style et le ton original de l’article.
    - Optimisez le contenu pour le SEO tout en le rendant captivant et informatif.

    Réécrivez l’article en respectant ces instructions.
    """

    # Step 4: Generate Rewritten Article with LLM
    print("🔍 Debugging: Sending LLM Prompt...")
    print(prompt)  # Print the actual LLM input

    try:
        import requests
        llm_url = local_llm_config["config_list"][0]["base_url"] + "/api/generate"
        payload = {
            "model": local_llm_config["config_list"][0]["model"],
            "prompt": prompt,
            "stream": False
        }
        llm_response = requests.post(llm_url, json=payload)
        llm_response.raise_for_status()
        raw_response = llm_response.json().get("response", "")
        rewritten_article = raw_response

        print("🔍 Rewritten Article:\n", rewritten_article)
        return rewritten_article

    except Exception as e:
        raise RuntimeError(f"❌ Error in marketing content adaptation: {e}")

print("\n✅ Debugging: `marketing_content_specialist` initialized successfully!")