import requests
from autogen import ConversableAgent
from utils.llm_config import local_llm_config  # Import correct LLM config

# Developer: Uses ConversableAgent to generate structured medical articles via an external LLM.

# Ensure the config exists before initializing
if not local_llm_config.get("config_list"):
    raise ValueError("❌ Error: `local_llm_config` is missing required LLM configuration.")

# Initialize the ConversableAgent
pharmacist_expert = ConversableAgent(
    name="pharmacist_expert",
    system_message="Vous êtes un pharmacien expérimenté. Votre mission est de rédiger des articles de santé précis et éthiques.",
    llm_config=local_llm_config
)

# Developer: Constructs and sends a structured prompt to the LLM API, handling validation and errors.
# Function to generate an article based on the topic
def generate_article(topic):
    # Ensure topic is correctly passed and enforced
    if not topic or not isinstance(topic, str):
        raise ValueError("❌ Error: A valid topic string is required.")

    llm_url = local_llm_config["config_list"][0]["base_url"] + "/api/generate"
    test_payload = {
        "model": local_llm_config["config_list"][0]["model"],
        "prompt": f"""
        You are a medical expert writing an informative article strictly on the topic: **{topic}**.
        
        The article must be structured as follows:
        
        **Title:** {topic}
        
        **Introduction**
        - Provide a concise overview of {topic}.
        
        **Causes**
        - Explain the primary causes related to {topic}.
        
        **Symptoms**
        - Describe key symptoms associated with {topic}.
        
        **Treatment Options**
        - Discuss available treatment options, both medical and lifestyle-based.
        
        **Prevention Strategies**
        - Outline preventive measures.
        
        You must strictly follow the topic "{topic}" and avoid unrelated content.
        """,
        "stream": False
    }

    try:
        response = requests.post(llm_url, json=test_payload)
        response.raise_for_status()
        article = response.json().get("response", "")

        # Debugging output to ensure topic adherence
        print(f"\n🔍 Generated Article for '{topic}':\n", article)
        return article  # Return the generated article
    except Exception as e:
        raise RuntimeError(f"❌ LLM API connection failed: {e}")

print("\n✅ Debugging: `pharmacist_expert` initialized successfully!")