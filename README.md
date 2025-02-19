# Billing-System-with-MySQL-and-Tkinter

This is a Python-based billing system that uses Tkinter for the GUI and MySQL as the database backend. The system supports multiple billing categories, such as restaurants, bus tickets, phone accessories, and medical stores. Users can view available items, select a quantity, and generate bills dynamically.

Features
✅ Multi-Category Billing – Supports different billing systems (Restaurant, Bus, Phone, Medical Store)
✅ MySQL Integration – Stores and retrieves items and transactions efficiently
✅ Tkinter GUI – Provides an intuitive and interactive interface for users
✅ Automatic Database Setup – Creates required tables and inserts sample data if they do not exist
✅ Item Selection & Quantity Input – Users can select items and specify the quantity before billing
✅ Real-Time Updates – Refresh items and update the interface dynamically


conn = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="yourpassword", #give your created password
    database="projects"
)
Step 3: Run the Application
