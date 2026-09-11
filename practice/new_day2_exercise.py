def gc_content(sequence):
    g_count = sequence.count('G') 
    c_count = sequence.count('C') 
    return round((g_count + c_count) / len(sequence) * 100, 2)
print(gc_content("AGCTAGCAGCTAGCAGCTAGC")) 

agent_in_section_2 = ['sequence Reader', 'sequence Analyzer', 'sequence Visualizer','Pattern Finder']
agent_config = {'name': 'Sequence Reader', 'section': 2, 'job': 'parse sequence and compute stats'}

for agent in agent_in_section_2:
    print(f'checking status of {agent}')

import json

tool_call = {'agent': 'Sequence Reader', 'action': 'compute_gc_content', 'sequence': 'AGCTAGCAGCTAGCAGCTAGC'}
json_string = json.dumps(tool_call)
print(json_string)

parsed_back = json.loads(json_string)
print(parsed_back['action'])

def safe_gc_content(sequence):
    try:
        g_count = sequence.count('G')
        c_count = sequence.count('C')
        return round((g_count + c_count) / len(sequence) * 100, 2)
    except ZeroDivisionError:
        print("Error: empty sequence, cannot compute GC content")
        return None

print(safe_gc_content("ATCGGCTA")) 
print(safe_gc_content(""))