import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

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

# Query data based on selected league and team
def query_data():
    selected_league = league_var.get()
    team_name = team_entry.get().strip()  # Get team name from the input field

    if selected_league == "Select a League" and not team_name:
        messagebox.showerror("Error", "Please select a league or enter a team name!")
        return

    conn = sqlite3.connect("merged.db")
    cursor = conn.cursor()

    try:
        if team_name:
            # Filter by both league and team
            query = "SELECT * FROM Football WHERE League = ? AND (Home_Team = ? OR Away_Team = ?)"
            cursor.execute(query, (selected_league, team_name, team_name))
        else:
            # Filter by only league (if no team name entered)
            query = "SELECT * FROM Football WHERE League = ?"
            cursor.execute(query, (selected_league,))

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