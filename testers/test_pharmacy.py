from utils.llm_config import local_llm_config
from agents.pharmacist_expert import pharmacist_expert
import requests

print("\n🔍 Debugging: Loaded LLM Config ->", local_llm_config)

# Ensure the config exists before initializing
if not local_llm_config.get("config_list"):
    raise ValueError("❌ Error: `local_llm_config` is missing required LLM configuration.")

if pharmacist_expert is None:
    raise RuntimeError("❌ Error: `pharmacist_expert` failed to initialize.")

print("\n✅ Debugging: `pharmacist_expert` initialized successfully!")

# Direct LLM Test...
print("\n🔍 Direct LLM Test...")

llm_url = local_llm_config["config_list"][0]["base_url"] + "/v1/completions"
payload = {
    "model": local_llm_config["config_list"][0]["model"],
    "prompt": "Write a short article about hair loss.",
    "max_tokens": 150
}

try:
    response = requests.post(llm_url, json=payload)
    response.raise_for_status()
    print("\n✅ LLM API Test Response:", response.json())
except Exception as e:
    print("\n❌ Error in Direct LLM API Call:", e)

# Debugging: Print agent attributes to verify it's loaded correctly
print("\n🔍 Debugging: `pharmacist_expert` Properties ->", dir(pharmacist_expert))

# Removed Testing `pharmacist_expert` chat function as it's no longer needed.