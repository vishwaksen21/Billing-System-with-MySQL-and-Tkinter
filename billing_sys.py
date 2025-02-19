import mysql.connector
from tkinter import *
from tkinter import ttk

conn = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="give_your_password",
    database="projects"
)
cursor = conn.cursor()

billing_systems = ["restaurant", "bus", "phone", "medical_store"]

for system in billing_systems:
    cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS {system} (
        id INT AUTO_INCREMENT PRIMARY KEY,
        item_name VARCHAR(255) UNIQUE,
        price DECIMAL(10, 2),
        quantity INT
    )
    """)

    cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS {system}_bills (
        id INT AUTO_INCREMENT PRIMARY KEY,
        item_name VARCHAR(255),
        price_per_unit DECIMAL(10, 2),
        quantity INT,
        total_price DECIMAL(10, 2)
    )
    """)

example_items = {
    "restaurant": [
        ("Chicken Sandwich", 6.99, 40),
        ("Pasta Carbonara", 12.99, 25),
        ("Salmon Steak", 18.99, 15),
        ("Caesar Salad", 8.99, 30),
    ],
    "bus": [
        ("Airport Shuttle", 5.5, 100),
        ("City Day Pass", 10.99, 50),
        ("Family Weekly Pass", 25.99, 10),
        ("VIP Monthly Pass", 49.99, 20),
    ],
    "phone": [
        ("Wireless Earbuds", 39.99, 15),
        ("Power Bank", 24.99, 20),
        ("Bluetooth Speaker", 29.99, 10),
        ("Phone Stand", 9.99, 40),
    ],
    "medical_store": [
        ("Allergy Medication", 12.99, 30),
        ("First Aid Kit", 29.99, 10),
        ("Vitamin C Tablets", 7.99, 50),
        ("Thermometer", 15.99, 25),
    ],
}

for system, items in example_items.items():
    for item in items:
        item_name, price, quantity = item
        cursor.execute(f"INSERT IGNORE INTO {system} (item_name, price, quantity) VALUES (%s, %s, %s)", (item_name, price, quantity))
        conn.commit()

quantity_entries = {}
result_labels = {}

root = Tk()
root.title("Billing System")

notebook = ttk.Notebook(root)
notebook.grid(row=0, column=0, padx=10, pady=10, columnspan=3)

billing_system_tabs = {}

for i, billing_system in enumerate(billing_systems):
    billing_system_tab = ttk.Frame(notebook)
    notebook.add(billing_system_tab, text=f"{billing_system.capitalize()} Billing")

    tree = ttk.Treeview(billing_system_tab, columns=("ID", "Item Name", "Price", "Quantity"))
    tree.heading("#0", text="ID")
    tree.heading("#1", text="Item Name")
    tree.heading("#2", text="Price")
    tree.heading("#3", text="Quantity")
    tree.grid(row=0, column=0, padx=10, pady=10)

    refresh_button = ttk.Button(billing_system_tab, text=f"Refresh {billing_system.capitalize()} Items", command=lambda bs=billing_system: display_items(bs))
    refresh_button.grid(row=1, column=0, pady=10)

    quantity_label = ttk.Label(billing_system_tab, text="Enter Quantity:")
    quantity_label.grid(row=2, column=0)
    quantity_entry = ttk.Entry(billing_system_tab)
    quantity_entry.grid(row=2, column=1)

    generate_bill_button = ttk.Button(billing_system_tab, text=f"Generate {billing_system.capitalize()} Bill", command=lambda bs=billing_system: generate_bill(bs))
    generate_bill_button.grid(row=2, column=2, padx=10)

    result_label = ttk.Label(billing_system_tab, text="")
    result_label.grid(row=3, column=0, columnspan=3, pady=10)

    billing_system_tabs[billing_system] = tree
    quantity_entries[billing_system] = quantity_entry
    result_labels[billing_system] = result_label

def display_items(billing_system):
    cursor.execute(f"SELECT * FROM {billing_system}")
    items = cursor.fetchall()
    tree = billing_system_tabs[billing_system]
    tree.delete(*tree.get_children())
    for item in items:
        tree.insert("", "end", values=item)

def generate_bill(billing_system):
    selected_item = billing_system_tabs[billing_system].selection()
    if not selected_item:
        result_labels[billing_system].config(text="Please select an item.")
        return

    item_id = billing_system_tabs[billing_system].item(selected_item)["values"][0]
    quantity = quantity_entries[billing_system].get()

    try:
        quantity = int(quantity)
        if quantity <= 0:
            raise ValueError("Quantity must be a positive integer.")
    except ValueError as e:
        result_labels[billing_system].config(text=str(e))
        return

    cursor.execute(f"SELECT item_name, price FROM {billing_system} WHERE id = %s", (item_id,))
    item = cursor.fetchone()

    if item:
        item_name, price = item
        total_price = price * quantity

        cursor.execute(f"""
        INSERT INTO {billing_system}_bills (item_name, price_per_unit, quantity, total_price)
        VALUES (%s, %s, %s, %s)
        """, (item_name, price, quantity, total_price))
        conn.commit()

        display_items(billing_system)
        result_labels[billing_system].config(text=f"Bill generated successfully! Total Price: ${total_price}")
    else:
        result_labels[billing_system].config(text="Invalid item selection.")

root.mainloop()

conn.close()