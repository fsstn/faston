import json

# open JSON file and load data
with open("sample-data.json") as f:
    data = json.load(f)

print("Interface Status")
print("=" * 80)
print(f"{'DN':50} {'Description':20} {'Speed':8} {'MTU':6}")
print("-" * 50 + " " + "-" * 20 + " " + "-" * 8 + " " + "-" * 6)

# go through all interfaces inside imdata
for item in data["imdata"]:
    attrs = item["l1PhysIf"]["attributes"]

    dn = attrs.get("dn", "")
    descr = attrs.get("descr", "")
    speed = attrs.get("speed", "")
    mtu = attrs.get("mtu", "")

    # print formatted row
    print(f"{dn:50} {descr:20} {speed:8} {mtu:6}")