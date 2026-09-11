import os
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()

AGENT_INFO = {"name": "Pattern Finder", "section": 2, "job": "sequence analysis"}

def count_bases(sequence):
    return {
        "A": sequence.count("A"),
        "T": sequence.count("T"),
        "C": sequence.count("C"),
        "G": sequence.count("G")
    }


tools = [
    {
        "name": "count_bases",
        "description": "Count how many of each base (A, T, C, G) are in a DNA sequence",
        "input_schema": {
            "type": "object",
            "properties": {
                "sequence": {"type": "string", "description": "DNA sequence to analyze"}
            },
            "required": ["sequence"]
        }
    }
]

messages = [{"role": "user", "content": "How many of each base are in ATCGGCTA? "}]

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

        if tool_name == "count_bases":
            result = count_bases(tool_input["sequence"])

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