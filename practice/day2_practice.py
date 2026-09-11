name = 'Alice'
age = 30
is_agent = True
def greet (name) :
    return f'Hello,{name}!'
print(greet('World'))
tools = ['search', 'calculator', 'wather']
agent_config = {'name': 'agent', 'model': 'claude', 'max_turns': 5}
for tool in tools:
    print(f'Available tool: {tool}')

import json
data = {'action': 'search', 'query': 'weather in Jeddah'}
json_string = json.dumps(data)
print(json_string)

parsed_back = json.loads(json_string)
print(parsed_back['action'])

try:
        result = 10 / 0
except ZeroDivisionError as e:
        print(f'Error caught: {e}')
