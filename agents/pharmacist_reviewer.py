from autogen import ConversableAgent
from utils.llm_config import local_llm_config

pharmacist_reviewer = ConversableAgent(
    name="pharmacist_reviewer",
    llm_config=local_llm_config,
)