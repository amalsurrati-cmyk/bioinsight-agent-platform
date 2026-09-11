import os
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()

AGENT_INFO = {"name": "File Detective", "section": 1, "job": "detect what kind of biological data file was uploaded"}

def detect_file_type_from_content(first_line):
    if first_line.startswith(">"):
        return "sequence"
    else:
        return "tabular"

def detect_file_type(filepath):
    extension = os.path.splitext(filepath)[1].lower()

    if extension in [".fasta", ".fa"]:
        return "sequence"
    elif extension in [".csv", ".tsv", ".xlsx"]:
        return "tabular"
    else:
        return "unknown"
print(detect_file_type_from_content(">"))
print(detect_file_type_from_content("sample_id,value"))

tools = [
    {
        "name": "detect_file_type",
        "description": "Detect what type of biological data a file contains based on its filename/extension",
        "input_schema": {
            "type": "object",
            "properties": {
                "filepath": {"type": "string", "description": "The file name or path to check"}
            },
            "required": ["filepath"]
        }
    }
]

messages = [{"role": "user", "content": "What kind of file is sample_id.value?"}]

response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=500,
    system=f"You are {AGENT_INFO['name']}, a BioInsight agent whose job is to {AGENT_INFO['job']}.",
    tools=tools,
    messages=messages
)

for block in response.content:
    if block.type == "tool_use":
        tool_name = block.name
        tool_input = block.input
        print(f"[{AGENT_INFO['name']}] Model wants to call: {tool_name} with {tool_input}")

        if tool_name == "detect_file_type":
            result = detect_file_type(tool_input["filepath"])

            messages.append({"role": "assistant", "content": response.content})
            messages.append({
                "role": "user",
                "content": [{
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result
                }]
            })

            final_response = client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=500,
                tools=tools,
                messages=messages
            )
            print(final_response.content[0].text)