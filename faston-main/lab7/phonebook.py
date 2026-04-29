import csv
import psycopg2
from connect import connect

def create_table(conn):
    """Creates the contacts table if it doesn't exist."""
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS contacts (
        id SERIAL PRIMARY KEY,
        first_name VARCHAR(50) NOT NULL,
        last_name VARCHAR(50),
        phone VARCHAR(20) UNIQUE NOT NULL
    );
    """
    with conn.cursor() as cur:
        cur.execute(create_table_sql)
    conn.commit()
    print("Table 'contacts' is ready.")

def insert_from_csv(conn, filename="contacts.csv"):
    """Reads data from a CSV and inserts it into the database."""
    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            next(csv_reader) # Skip the header row
            
            insert_sql = """
            INSERT INTO contacts (first_name, last_name, phone)
            VALUES (%s, %s, %s)
            ON CONFLICT (phone) DO NOTHING;
            """
            
            with conn.cursor() as cur:
                for row in csv_reader:
                    cur.execute(insert_sql, (row[0], row[1], row[2]))
            conn.commit()
            print(f"Data imported successfully from {filename}.")
    except FileNotFoundError:
        print(f"Error: The file {filename} was not found.")
    except Exception as e:
        print(f"An error occurred during CSV import: {e}")

def insert_from_console(conn):
    """Inserts a single contact from user input."""
    first_name = input("Enter first name: ")
    last_name = input("Enter last name (optional, press Enter to skip): ")
    phone = input("Enter phone number: ")
    
    insert_sql = "INSERT INTO contacts (first_name, last_name, phone) VALUES (%s, %s, %s)"
    
    try:
        with conn.cursor() as cur:
            cur.execute(insert_sql, (first_name, last_name, phone))
        conn.commit()
        print(f"Contact '{first_name}' added successfully!")
    except psycopg2.IntegrityError:
        conn.rollback()
        print("Error: A contact with this phone number already exists.")

def update_contact(conn):
    """Updates a contact's first name or phone number."""
    search_phone = input("Enter the current phone number of the contact to update: ")
    print("What do you want to update?")
    print("1. First Name")
    print("2. Phone Number")
    choice = input("Enter choice (1/2): ")
    
    try:
        with conn.cursor() as cur:
            if choice == '1':
                new_name = input("Enter new first name: ")
                cur.execute("UPDATE contacts SET first_name = %s WHERE phone = %s", (new_name, search_phone))
            elif choice == '2':
                new_phone = input("Enter new phone number: ")
                cur.execute("UPDATE contacts SET phone = %s WHERE phone = %s", (new_phone, search_phone))
            else:
                print("Invalid choice.")
                return
                
            if cur.rowcount > 0:
                print("Contact updated successfully!")
            else:
                print("Contact not found.")
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        print(f"Database error: {e}")

def query_contacts(conn):
    """Queries contacts based on name or phone prefix."""
    print("Search by:")
    print("1. Exact First Name")
    print("2. Phone Prefix (e.g., +7701)")
    choice = input("Enter choice (1/2): ")
    
    with conn.cursor() as cur:
        if choice == '1':
            name = input("Enter first name to search: ")
            cur.execute("SELECT first_name, last_name, phone FROM contacts WHERE first_name = %s", (name,))
        elif choice == '2':
            prefix = input("Enter phone prefix: ")
            # Using LIKE for prefix matching
            cur.execute("SELECT first_name, last_name, phone FROM contacts WHERE phone LIKE %s", (prefix + '%',))
        else:
            print("Invalid choice.")
            return

        results = cur.fetchall()
        
        if results:
            print("\n--- Search Results ---")
            for row in results:
                print(f"Name: {row[0]} {row[1] or ''} | Phone: {row[2]}")
            print("----------------------\n")
        else:
            print("No contacts found matching your criteria.")

def delete_contact(conn):
    """Deletes a contact by first name or phone number."""
    print("Delete by:")
    print("1. First Name")
    print("2. Phone Number")
    choice = input("Enter choice (1/2): ")
    
    with conn.cursor() as cur:
        if choice == '1':
            name = input("Enter the first name of the contact to delete: ")
            cur.execute("DELETE FROM contacts WHERE first_name = %s", (name,))
        elif choice == '2':
            phone = input("Enter the phone number to delete: ")
            cur.execute("DELETE FROM contacts WHERE phone = %s", (phone,))
        else:
            print("Invalid choice.")
            return

        if cur.rowcount > 0:
            print(f"Successfully deleted {cur.rowcount} contact(s).")
        else:
            print("No contact found to delete.")
    conn.commit()

def main():
    """Main menu loop."""
    conn = connect()
    if conn is None:
        return

    create_table(conn)

    while True:
        print("\n=== PhoneBook Menu ===")
        print("1. Import contacts from CSV")
        print("2. Add new contact (Console)")
        print("3. Update a contact")
        print("4. Search contacts")
        print("5. Delete a contact")
        print("6. Exit")
        
        choice = input("Choose an option (1-6): ")
        
        if choice == '1':
            insert_from_csv(conn)
        elif choice == '2':
            insert_from_console(conn)
        elif choice == '3':
            update_contact(conn)
        elif choice == '4':
            query_contacts(conn)
        elif choice == '5':
            delete_contact(conn)
        elif choice == '6':
            print("Closing connection and exiting. Goodbye!")
            conn.close()
            break
        else:
            print("Invalid input. Please try again.")

if __name__ == '__main__':
    main()