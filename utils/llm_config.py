local_llm_config = {
    "config_list": [
        {
            "model": "llama3.1:8b",  # Ollama model name
            "base_url": "http://localhost:11434",  # Default Ollama API endpoint
            "api_key": "NotRequired",  # Dummy API key to satisfy autogen initialization
            "price": [0, 0],  # Free model, no pricing
        }
    ],
    "cache_seed": None,
}