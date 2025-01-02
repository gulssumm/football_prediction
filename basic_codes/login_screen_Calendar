import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from datetime import datetime
import calendar

# Authenticate user
def authenticate_user(username, password):
    conn = sqlite3.connect("merged.db")
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

def convert_date_format(date_str):
    # Convert from yyyy-mm-dd to "May 2001, Monday 28th May"
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")  # Convert string to datetime object
    # Format the date
    formatted_date = date_obj.strftime("%B %Y, %A %dth %B")
    return formatted_date        

def query_data():
    selected_league = league_var.get()
    team_name = team_entry.get().strip()
    selected_date = date_var.get()

    if selected_league == "Select a League" and not team_name and not selected_date:
        messagebox.showerror("Error", "Please select a league, enter a team name, or select a date!")
        return

    # Convert the selected date from yyyy-mm-dd to the database format
    if selected_date:
        selected_date = convert_date_format(selected_date)

    conn = sqlite3.connect("merged.db")
    cursor = conn.cursor()

    try:
        # Construct the base query
        query = "SELECT * FROM Football WHERE 1=1"
        params = []

        # Add conditions based on user input
        if selected_league != "Select a League":
            query += " AND LOWER(League) LIKE ?"
            params.append(f"%{selected_league.lower()}%")
        if team_name:
            query += " AND (LOWER(Home_Team) LIKE ? OR LOWER(Away_Team) LIKE ?)"
            params.extend([f"%{team_name.lower()}%", f"%{team_name.lower()}%"])
        if selected_date:
            query += " AND LOWER(Date) LIKE ?"
            params.append(f"%{selected_date.lower()}%")

        # Debugging: Print query and parameters
        print("Executing Query:", query)
        print("With Parameters:", params)

        cursor.execute(query, tuple(params))
        results = cursor.fetchall()

        # Clear previous results
        for i in tree.get_children():
            tree.delete(i)

        # Display new results
        if results:
            for row in results:
                tree.insert("", "end", values=row)
        else:
            messagebox.showinfo("No Results", "No data found matching the criteria.")

        conn.close()
    except sqlite3.Error as e:
        messagebox.showerror("Query Error", f"An error occurred: {e}")

# Query screen
def open_query_screen():
    query_screen = tk.Tk()
    query_screen.title("Query Data")

    # League selection dropdown
    tk.Label(query_screen, text="Select a League:").pack(pady=5)
    global league_var
    league_var = tk.StringVar()
    league_var.set("Select a League")

    league_dropdown = ttk.Combobox(query_screen, textvariable=league_var, state="readonly")
    league_dropdown['values'] = [
        "Championship", "League One", "Premier League", "Ligue 1", "Bundesliga",
        "Serie A", "La Liga", "Trendyol 1. Lig", "Trendyol Süper Lig"
    ]
    league_dropdown.pack(pady=5)

    # Team name input field
    tk.Label(query_screen, text="Enter a Team Name (Optional):").pack(pady=5)
    global team_entry
    team_entry = tk.Entry(query_screen)
    team_entry.pack(pady=5)

    # Date selection
    tk.Label(query_screen, text="Select a Date (Optional):").pack(pady=5)
    global date_var
    date_var = tk.StringVar()
    date_entry = DateEntry(query_screen, textvariable=date_var, date_pattern="yyyy-mm-dd", width=12)
    date_entry.pack(pady=5)

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
root.geometry("400x300")
root.configure(bg="lightblue")

style = ttk.Style()
style.configure("TLabel", font=("Helvetica", 12))
style.configure("TButton", font=("Helvetica", 12), background="blue")
style.configure("TCombobox", font=("Helvetica", 12))

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