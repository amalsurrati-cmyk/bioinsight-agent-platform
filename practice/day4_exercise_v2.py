import os
from typing import Any
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()

AGENT_INFO = {"name": "Metabolite Finder", "section": 2, "job": "pathway analysis"}

def metabolite_maping(pathway):
    return {
        "pathway": Any,
        "metabolites": ["Ascorbate", "Proline", "Intermediate Metabolites"]}


tools = [
    {
        "name": "metabolite_maping",
        "description": "list all intermediate metabolites involved in ascorbate degradation to proline in KEGG pathway",
        "input_schema": {
            "type": "object",
            "properties": {
                "pathway": {"type": "string", "description": "KEGG pathway to analyze"}
            },
            "required": ["pathway"]
        }
    }
]

messages = [{"role": "user", "content": "List all intermediate metabolites involved in ascorbate degradation to proline in KEGG pathway? "}]

response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=500,
    system=f"You are {AGENT_INFO['name']}, a BioInsight agent for {AGENT_INFO['job']}.",
    tools=tools,
    messages=messages
)

for block in response.content:
    if block.type == "tool_use":
        tool_name = block.name
        tool_input = block.input
        print(f"[{AGENT_INFO['name']}] Model wants to call: {tool_name} with {tool_input}")

        if tool_name == "metabolite_maping":
            result = metabolite_maping(tool_input["pathway"])

            messages.append({"role": "assistant", "content": response.content})
            messages.append({
                "role": "user",
                "content": [{
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": str(result)
                }]
            })

            final_response = client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=500,
                tools=tools,
                messages=messages
            )
            print(final_response.content[0].text)