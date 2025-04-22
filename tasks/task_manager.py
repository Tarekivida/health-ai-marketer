import yaml
import os
from agents import (
    pharmacist_expert,
    product_extraction_agent,
    product_research_agent,
    product_scraper_agent,
    marketing_content_specialist,
    pharmacist_reviewer
)

# Load task definitions
def load_tasks():
    yaml_path = "tasks/task_definitions.yaml"
    
    if not os.path.exists(yaml_path):
        raise FileNotFoundError(f"\n❌ Error: Missing {yaml_path}. Ensure the file exists in the 'tasks' folder.")

    with open(yaml_path, "r") as file:
        return yaml.safe_load(file)["tasks"]

# Mapping agent names to objects
AGENT_MAP = {
    "pharmacist_expert": pharmacist_expert,
    "product_extraction_agent": product_extraction_agent,
    "product_research_agent": product_research_agent,
    "product_scraper_agent": product_scraper_agent,
    "marketing_content_specialist": marketing_content_specialist,
    "pharmacist_reviewer": pharmacist_reviewer,
}

print("\n🔍 Debugging: AGENT_MAP ->", AGENT_MAP)  # Debugging

def execute_task(task):
    agent = AGENT_MAP.get(task["agent"])
    
    if agent is None:
        raise ValueError(f"\n❌ Error: Agent '{task['agent']}' is not properly initialized in AGENT_MAP.")
    
    print(f"\n🚀 Executing task: {task['name']} with {task['agent']}...")
    print(f"\n🔍 Debugging: Retrieved agent -> {agent}")  # Debugging agent instance

    if not hasattr(agent, "initiate_chat"):
        raise AttributeError(f"\n❌ Error: Agent '{task['agent']}' does not have 'initiate_chat' method.")

    try:
        response = agent.initiate_chat(None, message=task["description"])
        print(f"\n🔍 Debugging: Agent '{task['agent']}' Response -> {response}")

        if response is None:
            raise ValueError(f"\n❌ Error: Agent '{task['agent']}' returned None from initiate_chat().")

    except AttributeError as e:
        print(f"\n❌ Error: Agent '{task['agent']}' failed during execution. Check its initialization.")
        raise e

    return response

# Run all tasks in sequence
def run_all_tasks():
    tasks = load_tasks()
    results = {}

    print("\n🔄 Running all tasks sequentially...\n")

    for task in tasks:
        print(f"\n🔍 Running task: {task['name']} with agent {task['agent']}...")
        if task["agent"] not in AGENT_MAP or AGENT_MAP[task["agent"]] is None:
            print(f"\n❌ Skipping task '{task['name']}' - Agent '{task['agent']}' is not initialized.")
            continue
        try:
            results[task["name"]] = execute_task(task)
        except Exception as e:
            print(f"\n❌ Error executing task '{task['name']}': {e}")
    
    return results

if __name__ == "__main__":
    task_results = run_all_tasks()
    print("\n✅ All tasks completed successfully!\n")
    
    for task_name, result in task_results.items():
        print(f"\n🔹 {task_name} Result:\n{result}\n")