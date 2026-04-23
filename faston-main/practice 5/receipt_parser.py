import re
import json

# 1. Чтение текста из файла raw.txt (для Windows используем r"" для пути)
with open(r'C:\Users\b_zulkharnai/\ало\raw.txt', 'r', encoding='utf-8') as file:
    lines = [line.strip() for line in file if line.strip()]  # убираем пустые строки

text = "\n".join(lines)

# 2. Извлечение цен после "Стоимость"
prices = [float(p.replace(" ", "").replace(",", "."))
          for p in re.findall(r'Стоимость\s+([\d\s]+,\d{2})', text)]

# 3. Извлечение названий продуктов (строка перед количеством x цена)
products = []
for i, line in enumerate(lines):
    if re.search(r'\d+,\d{2}', line) and 'x' in line:
        product_line = lines[i-1].strip()
        products.append(product_line)

# 4. Общая сумма
total_amount = sum(prices)

# 5. Дата и время
date_match = re.search(r'\b\d{2}\.\d{2}\.\d{4}\b', text)
time_match = re.search(r'\b\d{2}:\d{2}:\d{2}\b', text)
date = date_match.group(0) if date_match else None
time = time_match.group(0) if time_match else None

# 6. Способ оплаты
payment_match = re.search(r'\b(Банковская карта|CASH|CARD|CREDIT|DEBIT)\b', text, re.IGNORECASE)
payment_method = payment_match.group(0) if payment_match else None

# 7. Структура JSON
receipt_data = {
    "products": products,
    "prices": prices,
    "total": total_amount,
    "date": date,
    "time": time,
    "payment_method": payment_method
}

# 8. Сохраняем в файл
with open(r'C:\Users\b_zulkharnai\ало\parsed_receipt.json', 'w', encoding='utf-8') as json_file:
    json.dump(receipt_data, json_file, ensure_ascii=False, indent=4)

# 9. Печать на экран
print(json.dumps(receipt_data, ensure_ascii=False, indent=4))