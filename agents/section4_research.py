import os
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()

SECTION_4_AGENTS = [
    {"name": "Literature Scout", "job": "search for relevant scientific information on a biology topic"},
    {"name": "Summarizer", "job": "summarize research findings in plain, non-technical language"}
]

def literature_search(question):
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=800,
        system=f"You are {SECTION_4_AGENTS[0]['name']}, a BioInsight agent whose job is to {SECTION_4_AGENTS[0]['job']}.",
        tools=[{"type": "web_search_20250305", "name": "web_search"}],
        messages=[{"role": "user", "content": question}]
    )
    for block in response.content:
        if block.type == "text":
            return block.text
    return None

def summarize_findings(raw_text):
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=300,
        system=f"You are {SECTION_4_AGENTS[1]['name']}, a BioInsight agent whose job is to {SECTION_4_AGENTS[1]['job']}. Summarize in 3 sentences maximum.",
        messages=[{"role": "user", "content": raw_text}]
    )
    return response.content[0].text

if __name__ == "__main__":
    research_result = literature_search("What is known about GC content and DNA thermal stability?")
    print("--- Full research ---")
    print(research_result)

    summary = summarize_findings(research_result)
    print("--- Summary ---")
    print(summary)