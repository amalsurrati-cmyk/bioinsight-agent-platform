def atgc_content(sequence):
    a_count = sequence.count('A') 
    t_count = sequence.count('T') 
    g_count = sequence.count('G') 
    c_count = sequence.count('C') 
    return round((a_count + t_count + g_count + c_count) / len(sequence) * 100, 2)


def count_bases(sequence):
    return {
        'A': sequence.count('A'),
        'T': sequence.count('T'),
        'G': sequence.count('G'),
        'C': sequence.count('C')
    }


print(atgc_content("ATCGGCTA"))

agent_config = {'sample_id': 'S001', 'value': 42.5, 'flagged': 'False'}
if agent_config['flagged'] == 'True':
    print(f"Sample {agent_config['sample_id']} is flagged.")
else:
    print(f"Sample {agent_config['sample_id']} is normal.")

import json
tool_call = {'agent': 'sample_id', 'action': 'compute_atgc_content', 'sequence': 'ATCGGCTA'}
json_string = json.dumps(tool_call)
print(json_string)

parsed_back = json.loads(json_string)
print(parsed_back["action"])

print(count_bases("ATCGGCTA"))