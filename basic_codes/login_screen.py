import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk


# Authenticate user
def authenticate_user(username, password):
    conn = sqlite3.connect("../SPAIN/spain_laliga.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users WHERE username = ? AND password = ?", (username, password))
    result = cursor.fetchone()
    conn.close()
    return result is not None


# Handle login
def login():
    username = username_entry.get()
    password = password_entry.get()

    if authenticate_user(username, password):
        messagebox.showinfo("Login Successful", "Welcome!")
        root.destroy()  # Close login screen
        open_query_screen()  # Open query screen
    else:
        messagebox.showerror("Login Failed", "Invalid username or password!")


# Query data
def query_data():
    query = query_entry.get()
    if not query.strip():
        messagebox.showerror("Error", "Please enter a query!")
        return

    conn = sqlite3.connect("spain_laliga.db")
    cursor = conn.cursor()

    try:
        cursor.execute(query)
        results = cursor.fetchall()

        # Clear previous results
        for i in tree.get_children():
            tree.delete(i)

        # Display new results
        for row in results:
            tree.insert("", "end", values=row)

        conn.close()
    except sqlite3.Error as e:
        messagebox.showerror("Query Error", f"An error occurred: {e}")


# Query screen
def open_query_screen():
    query_screen = tk.Tk()
    query_screen.title("Query Data")

    # Query label and entry
    tk.Label(query_screen, text="Enter your SQL Query:").pack(pady=5)
    global query_entry
    query_entry = tk.Entry(query_screen, width=50)
    query_entry.pack(pady=5)

    # Query button
    query_button = tk.Button(query_screen, text="Run Query", command=query_data)
    query_button.pack(pady=10)

    # Results table
    global tree
    columns = ["ID", "League", "Date", "Home_Team", "Away_Team", "Home_Score", "Away_Score"]
    tree = ttk.Treeview(query_screen, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)
    tree.pack(pady=10, fill="both", expand=True)

    query_screen.mainloop()


# Login screen
root = tk.Tk()
root.title("Login Screen")

# Username label and entry
tk.Label(root, text="Username:").pack(pady=5)
username_entry = tk.Entry(root)
username_entry.pack(pady=5)

# Password label and entry
tk.Label(root, text="Password:").pack(pady=5)
password_entry = tk.Entry(root, show="*")
password_entry.pack(pady=5)

# Login button
login_button = tk.Button(root, text="Login", command=login)
login_button.pack(pady=20)

root.mainloop()
