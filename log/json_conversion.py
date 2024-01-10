import json

# Read data from all.log file
with open('all.log', 'r') as file:
    log_entries = file.read().strip()

# Modify the delimiter to properly split JSON objects
json_objects = []
start = 0
for end in range(len(log_entries)):
    if log_entries[end] == '}':
        json_objects.append(json.loads(log_entries[start:end+1]))
        start = end + 1

# Write formatted data into a new JSON file
with open('formatted_all.log.json', 'w') as file:
    file.write(json.dumps(json_objects, indent=4))
