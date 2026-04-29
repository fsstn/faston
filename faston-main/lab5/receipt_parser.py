import re
import json


def parse_receipt(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = f.read()

    # ---------------------------------------------------
    # 1️⃣ Extract Date and Time
    # Format in receipt:
    # Время: 18.04.2019 11:13:58
    # ---------------------------------------------------

    datetime_match = re.search(
        r'Время:\s+(\d{2}\.\d{2}\.\d{4})\s+(\d{2}:\d{2}:\d{2})',
        data
    )

    date = datetime_match.group(1) if datetime_match else "Unknown"
    time = datetime_match.group(2) if datetime_match else "Unknown"

    # ---------------------------------------------------
    # 2️⃣ Extract ALL products
    #
    # Receipt structure for each item:
    #
    # 1.
    # Product Name
    # 2,000 x 154,00
    # 308,00
    # Стоимость
    # 308,00
    #
    # We match:
    # - item number
    # - product name
    # - quantity
    # - unit price
    # - total price
    # ---------------------------------------------------

    item_pattern = re.findall(
        r'\d+\.\s*\n'                      # Item number (1. 2. 3.)
        r'(.+?)\n'                          # Product name (lazy match)
        r'(\d+,\d+)\s*x\s*'                 # Quantity (example: 2,000)
        r'([\d\s]+,\d{2})\n'                # Unit price (example: 1 200,00)
        r'([\d\s]+,\d{2})',                 # Total price
        data
    )

    items = []

    for match in item_pattern:
        name = match[0].strip()
        quantity = float(match[1].replace(",", "."))
        unit_price = float(match[2].replace(" ", "").replace(",", "."))
        total_price = float(match[3].replace(" ", "").replace(",", "."))

        items.append({
            "product": name,
            "quantity": quantity,
            "unit_price": unit_price,
            "total_price": total_price
        })

    # ---------------------------------------------------
    # 3️⃣ Extract GRAND TOTAL
    #
    # Format:
    # ИТОГО:
    # 18 009,00
    # ---------------------------------------------------

    total_match = re.search(
        r'ИТОГО:\s*\n([\d\s]+,\d{2})',
        data
    )

    grand_total = (
        float(total_match.group(1).replace(" ", "").replace(",", "."))
        if total_match else 0.0
    )

    # ---------------------------------------------------
    # 4️⃣ Detect Payment Method
    #
    # If receipt contains:
    # "Банковская карта:"
    # we assume payment by Card
    # ---------------------------------------------------

    if re.search(r'Банковская карта:', data):
        payment_method = "Card"
    else:
        payment_method = "Unknown"

    # ---------------------------------------------------
    # 5️⃣ Build Final JSON Structure
    # ---------------------------------------------------

    receipt_json = {
        "store": "EUROPHARMA",
        "date": date,
        "time": time,
        "items": items,
        "summary": {
            "total_items": len(items),
            "grand_total": grand_total,
            "payment_method": payment_method
        }
    }

    return receipt_json


# ---------------------------------------------------
# Run Parser
# ---------------------------------------------------

if __name__ == "__main__":
    result = parse_receipt("raw.txt")
    print(json.dumps(result, indent=4, ensure_ascii=False))