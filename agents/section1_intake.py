import os
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()

import pandas as pd

SECTION_1_AGENTS = [
    {"name": "File Detective", "job": "detect what kind of biological data file was uploaded"},
    {"name": "Data Cleaner", "job": "clean and validate uploaded data"}
]

def detect_file_type(filepath):
    extension = os.path.splitext(filepath)[1].lower()

    if extension in [".fasta", ".fa"]:
        return "sequence"
    elif extension in [".csv", ".tsv", ".xlsx"]:
        return "tabular"
    else:
        return "unknown"

def check_data_quality(filepath):
    df = pd.read_csv(filepath)

    missing_counts = df.isnull().sum()
    duplicate_rows = df.duplicated().sum()
    mean_value = df['value'].mean()
    std_value = df['value'].std()
    outliers = df[(df['value'] < (mean_value - 3 * std_value)) | (df['value'] > (mean_value + 3 * std_value))]

    report = {
        "total_rows": len(df),
        "missing_values": missing_counts.to_dict(),
        "duplicate_rows": int(duplicate_rows),
        "outliers": outliers[["sample_id", "value"]].to_dict(orient="records")
    }

    return report
if __name__ == "__main__":
    print(check_data_quality("sample_data.csv"))

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

    messages = [{"role": "user", "content": "What kind of file is sample_data.csv?"}]

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=500,
        system=f"You are {SECTION_1_AGENTS[0]['name']}, a BioInsight agent whose job is to {SECTION_1_AGENTS[0]['job']}.",
        tools=tools,
        messages=messages
    )

    for block in response.content:
        if block.type == "tool_use":
            tool_name = block.name
            tool_input = block.input
            print(f"[{SECTION_1_AGENTS[0]['name']}] Model wants to call: {tool_name} with {tool_input}")
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