import os
from dotenv import load_dotenv
import anthropic

load_dotenv()

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=500,
    system="You are Stem Cell Specialist, an assistant specialized in bone regeneration and stem cell research.",
    messages=[
        {"role": "user", "content": "Explain what is the role of ascorbic acid in bone regeneration."}
    ]
)

print(response.content[0].text)
