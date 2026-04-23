import json

# Read the JSON file
with open('sample-data.json', 'r') as file:
    data = json.load(file)

# Print the header
print("Interface Status")
print("=" * 50)
print(f"{'DN':<50} {'Description':<20} {'Speed':<10} {'MTU':<10}")
print(f"{'-'*50} {'-'*20} {'-'*10} {'-'*10}")

# Process each interface in the imdata array
for item in data['imdata']:
    attributes = item['l1PhysIf']['attributes']
    dn = attributes['dn']
    descr = attributes['descr'] if attributes['descr'] else ""  # Handle empty description
    speed = attributes['speed']
    mtu = attributes['mtu']
    
    # Print the formatted output
    print(f"{dn:<50} {descr:<20} {speed:<10} {mtu:<10}")