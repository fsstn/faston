from connect import get_connection


def show_rows(rows):
    if not rows:
        print("No data found.")
    else:
        for row in rows:
            print(row)


def search():
    pattern = input("Search: ")
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM search_phonebook(%s)", (pattern,))
    rows = cur.fetchall()

    show_rows(rows)

    cur.close()
    conn.close()


def add_user():
    name = input("Name: ")
    surname = input("Surname: ")
    phone = input("Phone: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("CALL insert_or_update_user(%s, %s, %s)", (name, surname, phone))

    conn.commit()
    cur.close()
    conn.close()

    print("Saved.")


def add_many():
    names = input("Names (comma): ").split(",")
    surnames = input("Surnames (comma): ").split(",")
    phones = input("Phones (comma): ").split(",")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("CALL insert_many_users(%s, %s, %s)", (names, surnames, phones))
    result = cur.fetchone()

    conn.commit()
    cur.close()
    conn.close()

    if result and result[0]:
        print("Invalid data:", result[0])
    else:
        print("Done.")


def paginate():
    limit = int(input("Limit: "))
    offset = int(input("Offset: "))

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM paginate_phonebook(%s, %s)", (limit, offset))
    rows = cur.fetchall()

    show_rows(rows)

    cur.close()
    conn.close()


def delete():
    name = input("Name (Enter to skip): ").strip()
    phone = input("Phone (Enter to skip): ").strip()

    name = name if name else None
    phone = phone if phone else None

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("CALL delete_phonebook_data(%s, %s)", (name, phone))

    conn.commit()
    cur.close()
    conn.close()

    print("Deleted.")


def menu():
    while True:
        print("\n--- MENU ---")
        print("1. Add/Update user")
        print("2. Search")
        print("3. Add many users")
        print("4. Pagination")
        print("5. Delete")
        print("0. Exit")

        choice = input("Choose: ")

        if choice == "1":
            add_user()
        elif choice == "2":
            search()
        elif choice == "3":
            add_many()
        elif choice == "4":
            paginate()
        elif choice == "5":
            delete()
        elif choice == "0":
            break
        else:
            print("Invalid choice")


if __name__ == "__main__":
    menu()