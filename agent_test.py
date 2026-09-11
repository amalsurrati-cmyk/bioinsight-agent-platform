import os
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()

def get_weather(city):
    return f"The weather in {city} is sunny and 30°C."

tools = [
    {
        "name": "get_weather",
        "description": "Get the current weather for a city",
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "City name"}
            },
            "required": ["city"]
        }
    }
]

messages = [{"role": "user", "content": "What's the weather like in Jeddah?"}]

response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=500,
    tools=tools,
    messages=messages
)

for block in response.content:
    if block.type == "tool_use":
        tool_name = block.name
        tool_input = block.input
        print(f"Model wants to call: {tool_name} with {tool_input}")

        if tool_name == "get_weather":
            result = get_weather(tool_input["city"])

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
            