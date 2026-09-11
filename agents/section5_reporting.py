import matplotlib.pyplot as plt
import json
import os
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()

SECTION_5_AGENTS = [
    {"name": "Chart Maker", "job": "turn biological analysis results into visual charts"},
    {"name": "Report Writer", "job": "combine biological analysis results into one clear, organized report"}
]

def make_bar_chart(data_dict, title, output_path):
    plt.figure()
    plt.bar(data_dict.keys(), data_dict.values())
    plt.title(title)
    plt.savefig(output_path)
    plt.close()

def write_report(all_results):
    summary_text = json.dumps(all_results, indent=2)
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=800,
        system=f"You are {SECTION_5_AGENTS[1]['name']}, a BioInsight agent whose job is to {SECTION_5_AGENTS[1]['job']}. Use headers and keep it clear.",
        messages=[{"role": "user", "content": summary_text}]
    )
    return response.content[0].text

if __name__ == "__main__":
    chart_data = {"A": 4, "T": 4, "C": 4, "G": 4}
    make_bar_chart(chart_data, "Base Composition", "base_chart.png")
    print("Chart saved as base_chart.png")

    fake_results = {
    "sequence_stats": {"id": "seq1", "length": 16, "gc_content": 50.0},
    "outliers": []
}
    report = write_report(fake_results)
    print(report)