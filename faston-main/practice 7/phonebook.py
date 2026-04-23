import csv
from connect import get_connection
from psycopg2 import errors

def create_table():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(100) NOT NULL,
            phone VARCHAR(20) NOT NULL UNIQUE
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

def insert_from_csv(filename):
    conn = get_connection()
    cur = conn.cursor()
    with open(filename, "r") as f:
        command = "INSERT INTO phonebook (first_name, phone) VALUES (%s, %s)"
        reader = csv.reader(f)
        for row in reader:
            name, phone = row
            try:
                cur.execute(command, (name, phone))
            except errors.UniqueViolation:
                print("Номер уже существует!")
    conn.commit()
    cur.close()
    conn.close()
    print("Contacts inserted from CSV.")

def insert_from_console():
    name = input("Enter name: ")
    phone = input("Enter phone: ")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO phonebook (first_name, phone) VALUES (%s, %s)",
        (name, phone)
    )
    conn.commit()
    cur.close()
    conn.close()
    print("Contact inserted.")

def update_contact():
    value = input("Enter existing name or phone of contact to update: ")
    field = input("What do you want to update? (name/phone): ").strip().lower()
    new_value = input("Enter new value: ")
    conn = get_connection()
    cur = conn.cursor()

    if field == "name":
        cur.execute(
            "UPDATE phonebook SET first_name = %s WHERE first_name = %s OR phone = %s",
            (new_value, value, value)
        )
    elif field == "phone":
        cur.execute(
            "UPDATE phonebook SET phone = %s WHERE first_name = %s OR phone = %s",
            (new_value, value, value)
        )
    else:
        print("Invalid field.")
        cur.close()
        conn.close()
        return

    conn.commit()
    cur.close()
    conn.close()
    print("Contact updated.")

def query_all():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM phonebook ORDER BY id")
    rows = cur.fetchall()
    if rows:
        for row in rows:
            print(row)
    else:
        print("No contacts found.")
    cur.close()
    conn.close()

def query_by_name():
    name = input("Enter name filter: ")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM phonebook WHERE first_name ILIKE %s ORDER BY id",
        (f"%{name}%",)
    )
    rows = cur.fetchall()
    if rows:
        for row in rows:
            print(row)
    else:
        print("No matching contacts found.")
    cur.close()
    conn.close()

def query_by_phone_prefix():
    prefix = input("Enter phone prefix: ")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM phonebook WHERE phone LIKE %s ORDER BY id",
        (f"{prefix}%",)
    )
    rows = cur.fetchall()
    if rows:
        for row in rows:
            print(row)
    else:
        print("No matching contacts found.")
    cur.close()
    conn.close()

def delete_contact():
    value = input("Enter username or phone number to delete: ")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM phonebook WHERE first_name = %s OR phone = %s",
        (value, value)
    )
    conn.commit()
    cur.close()
    conn.close()
    print("Contact deleted if it existed.")

def menu():
    create_table()
    while True:
        print("\n--- PhoneBook Menu ---")
        print("1. Insert data from CSV")
        print("2. Insert data from console")
        print("3. Update contact name or phone")
        print("4. Query all contacts")
        print("5. Query by name")
        print("6. Query by phone prefix")
        print("7. Delete by username or phone")
        print("0. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            insert_from_csv("contacts.csv")
        elif choice == "2":
            insert_from_console()
        elif choice == "3":
            update_contact()
        elif choice == "4":
            query_all()
        elif choice == "5":
            query_by_name()
        elif choice == "6":
            query_by_phone_prefix()
        elif choice == "7":
            delete_contact()
        elif choice == "0":
            print("Goodbye.")
            break
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    menu()