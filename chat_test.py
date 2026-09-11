import os
from dotenv import load_dotenv
import anthropic

load_dotenv()

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=500,
    system="You are BioInsight, an assistant specialized in biology and lab data.",
    messages=[
        {"role": "user", "content": "Explain what GC content means in a DNA sequence, in 2 sentences."}
    ]
)

print(response.content[0].text)