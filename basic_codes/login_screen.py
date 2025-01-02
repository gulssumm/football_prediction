import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
<<<<<<< HEAD
=======
from dateutil import parser
from datetime import datetime
>>>>>>> aebac98c807f843c9f0d88a0ae34d9dc52a6d0e6

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
        #messagebox.showinfo("Login Successful", "Welcome!")
        root.destroy()  # Close login screen
        open_query_screen()  # Open query screen
    else:
        messagebox.showerror("Login Failed", "Invalid username or password!")

<<<<<<< HEAD
# Query data based on selected league and team
def query_data():
    selected_league = league_var.get()
    team_name = team_entry.get().strip()  # Get team name from the input field

    if selected_league == "Select a League" and not team_name:
        messagebox.showerror("Error", "Please select a league or enter a team name!")
        return

=======
def convert_date_format(date_str):
    # Convert from yyyy-mm-dd to "May 2001, Monday 28th May"
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")  # Convert string to datetime object
    # Format the date
    formatted_date = date_obj.strftime("%B %Y, %A %dth %B")
    return formatted_date


def query_data():
    selected_league = league_var.get()
    team_name = team_entry.get().strip()
    initial_year = initial_year_var.get().strip()
    end_year = end_year_var.get().strip()

    if not team_name and not initial_year and not end_year:
        messagebox.showerror("Error", "Please enter a team name or specify a year range!")
        return

    # Validate initial and end years
    try:
        initial_year = int(initial_year) if initial_year else None
        end_year = int(end_year) if end_year else None

        if initial_year and end_year and initial_year > end_year:
            initial_year, end_year = end_year, initial_year  # Swap years if in wrong order
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numeric years!")
        return

>>>>>>> aebac98c807f843c9f0d88a0ae34d9dc52a6d0e6
    conn = sqlite3.connect("merged.db")
    cursor = conn.cursor()

    try:
<<<<<<< HEAD
        if team_name:
            # Filter by both league and team
            query = "SELECT * FROM Football WHERE League = ? AND (Home_Team = ? OR Away_Team = ?)"
            cursor.execute(query, (selected_league, team_name, team_name))
        else:
            # Filter by only league (if no team name entered)
            query = "SELECT * FROM Football WHERE League = ?"
            cursor.execute(query, (selected_league,))

=======
        # Fetch all rows and filter dates in Python
        cursor.execute("SELECT * FROM Football")
>>>>>>> aebac98c807f843c9f0d88a0ae34d9dc52a6d0e6
        results = cursor.fetchall()

        filtered_results = []
        for row in results:
            row_id, league, date_str, home_team, away_team, home_score, away_score = row
            year = extract_year(date_str)

            if year:
                if selected_league != "Select a League" and selected_league.lower() not in league.lower():
                    continue
                if team_name and team_name.lower() not in (home_team.lower() + away_team.lower()):
                    continue
                if initial_year and end_year and not (initial_year <= year <= end_year):
                    continue
                if initial_year and not end_year and year < initial_year:
                    continue
                if end_year and not initial_year and year > end_year:
                    continue

                filtered_results.append(row)

        # Clear previous results
        for i in tree.get_children():
            tree.delete(i)

<<<<<<< HEAD
        # Display new results
        for row in results:
            tree.insert("", "end", values=row)
=======
        # Display filtered results
        if filtered_results:
            for row in filtered_results:
                tree.insert("", "end", values=row)
        else:
            messagebox.showinfo("No Results", "No data found matching the criteria.")
>>>>>>> aebac98c807f843c9f0d88a0ae34d9dc52a6d0e6

    except sqlite3.Error as e:
        messagebox.showerror("Query Error", f"An error occurred: {e}")
    finally:
        conn.close()


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

<<<<<<< HEAD
=======
    # Year selection (initial year)
    tk.Label(query_screen, text="Enter Initial Year:").pack(pady=5)
    global initial_year_var
    initial_year_var = tk.StringVar()
    initial_year_entry = tk.Entry(query_screen, textvariable=initial_year_var, width=12)
    initial_year_entry.pack(pady=5)

    # Year selection (end year)
    tk.Label(query_screen, text="Enter End Year:").pack(pady=5)
    global end_year_var
    end_year_var = tk.StringVar()
    end_year_entry = tk.Entry(query_screen, textvariable=end_year_var, width=12)
    end_year_entry.pack(pady=5)

>>>>>>> aebac98c807f843c9f0d88a0ae34d9dc52a6d0e6
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

def extract_year(date_str):
    try:
        # Attempt to parse the date using `dateutil.parser`
        date_obj = parser.parse(date_str, fuzzy=True)
        return date_obj.year
    except (ValueError, TypeError):
        return None  # Return None if parsing fails


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