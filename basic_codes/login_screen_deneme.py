import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
from dateutil import parser
import threading
import csv
import os
from scrape_all_leagues import scrape_league  # Ensure this module is available

# Authenticate user
def authenticate_user(username, password):
    conn = sqlite3.connect("merged.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users WHERE username = ? AND password = ?", (username, password))
    result = cursor.fetchone()
    conn.close()
    return result is not None

# Extract year from date string
def extract_year(date_str):
    try:
        date_obj = parser.parse(date_str, fuzzy=True)
        return date_obj.year
    except (ValueError, TypeError):
        return None

# Query data from the database
def query_data():
    selected_league = league_var.get()
    team_name = team_entry.get().strip()
    initial_year = initial_year_var.get().strip()
    end_year = end_year_var.get().strip()

    try:
        initial_year = int(initial_year) if initial_year else None
        end_year = int(end_year) if end_year else None

        conn = sqlite3.connect("merged.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Football")
        results = cursor.fetchall()

        filtered_results = []
        for row in results:
            league, date_str, home_team, away_team, home_score, away_score = row[1:]
            year = extract_year(date_str)

            if year:
                if selected_league != "Select a League" and selected_league.lower() not in league.lower():
                    continue
                if team_name and team_name.lower() not in (home_team.lower() + away_team.lower()):
                    continue
                if initial_year and end_year and not (initial_year <= year <= end_year):
                    continue
                filtered_results.append(row)

        for i in tree.get_children():
            tree.delete(i)

        if filtered_results:
            for row in filtered_results:
                tree.insert("", "end", values=row)
        else:
            messagebox.showinfo("No Results", "No data found matching the criteria.")
        conn.close()

    except sqlite3.Error as e:
        messagebox.showerror("Query Error", f"An error occurred: {e}")

# Generate URLs
def generate_real_urls(league_name, initial_year, end_year):
    base_url = "https://football-data.com"
    league_map = {
        "Championship": "championship",
        "League One": "league-one",
        "Premier League": "premier-league",
        "Ligue 1": "ligue-1",
        "Bundesliga": "bundesliga",
        "Serie A": "serie-a",
        "La Liga": "la-liga",
        "Trendyol 1. Lig": "trendyol-1-lig",
        "Trendyol Süper Lig": "trendyol-super-lig"
    }

    if league_name not in league_map:
        raise ValueError(f"Unsupported league: {league_name}")

    league_slug = league_map[league_name]
    urls = [f"{base_url}/{league_slug}-{year}" for year in range(initial_year, end_year + 1)]
    return urls

# Save URLs to a file
def save_urls_to_file(urls, league_name, initial_year, end_year):
    file_name = f"../basic_codes/URLS/urls_{league_name.replace(' ', '_').upper()}.txt"
    with open(file_name, 'w') as file:
        for url in urls:
            file.write(url + "\n")
    print(f"Saved URLs to {file_name}")

# Load scraped data into UI
def load_scraped_data_to_ui(csv_file):
    try:
        for i in tree.get_children():
            tree.delete(i)

        if not os.path.exists(csv_file):
            raise FileNotFoundError(f"CSV file {csv_file} not found.")

        with open(csv_file, newline="") as csvfile:
            reader = csv.reader(csvfile)
            header = next(reader, None)
            for row in reader:
                tree.insert("", "end", values=row)

    except FileNotFoundError:
        messagebox.showerror("File Error", "Scraped data file not found!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while loading the data: {e}")

# Scrape data from generated URLs
def scrape_data():
    try:
        initial_year = int(initial_year_var.get())
        end_year = int(end_year_var.get())
        league_name = league_var.get()

        urls = generate_real_urls(league_name, initial_year, end_year)
        csv_file = f"{initial_year}_{end_year}_{league_name.replace(' ', '_').lower()}.csv"

        # Save URLs to file for record
        save_urls_to_file(urls, league_name, initial_year, end_year)

        # Call the scrape_league function from scrape_all_leagues
        scrape_league(urls, league_name, initial_year, end_year)

        # Load scraped data to UI
        load_scraped_data_to_ui(csv_file)

    except ValueError:
        messagebox.showerror("Error", "Please enter valid numeric years!")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")

# Start live scraping
def start_scraping():
    scraping_thread = threading.Thread(target=scrape_data)
    scraping_thread.daemon = True
    scraping_thread.start()

# Open the query screen
def open_query_screen():
    query_screen = tk.Tk()
    query_screen.title("Football Matches")

    tk.Label(query_screen, text="Select a League:").pack(pady=5)
    global league_var
    league_var = tk.StringVar()
    league_var.set("Select a League")

    league_dropdown = ttk.Combobox(query_screen, textvariable=league_var, state="readonly")
    league_dropdown["values"] = [
        "Championship", "League One", "Premier League", "Ligue 1", "Bundesliga",
        "Serie A", "La Liga", "Trendyol 1. Lig", "Trendyol Süper Lig"
    ]
    league_dropdown.pack(pady=5)

    tk.Label(query_screen, text="Enter a Team Name (Optional):").pack(pady=5)
    global team_entry
    team_entry = tk.Entry(query_screen)
    team_entry.pack(pady=5)

    tk.Label(query_screen, text="Enter Initial Year:").pack(pady=5)
    global initial_year_var
    initial_year_var = tk.StringVar()
    initial_year_entry = tk.Entry(query_screen, textvariable=initial_year_var, width=12)
    initial_year_entry.pack(pady=5)

    tk.Label(query_screen, text="Enter End Year:").pack(pady=5)
    global end_year_var
    end_year_var = tk.StringVar()
    end_year_entry = tk.Entry(query_screen, textvariable=end_year_var, width=12)
    end_year_entry.pack(pady=5)

    tk.Button(query_screen, text="GET DATA FROM DB", command=query_data).pack(pady=10)

    global tree
    columns = ["League", "Date", "Home_Team", "Away_Team", "Home_Score", "Away_Score"]
    tree = ttk.Treeview(query_screen, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)
    tree.pack(pady=10, fill="both", expand=True)

    tk.Label(query_screen, text="Fetch Data from Website:").pack(pady=10)
    tk.Button(query_screen, text="START WEB SCRAPING", command=start_scraping).pack(pady=5)

    query_screen.mainloop()

# Handle login
def login():
    username = username_entry.get()
    password = password_entry.get()

    if authenticate_user(username, password):
        root.destroy()  # Close login screen
        open_query_screen()  # Open query screen
    else:
        messagebox.showerror("Login Failed", "Invalid username or password!")

# Login screen
root = tk.Tk()
root.title("Login Screen")
root.geometry("400x300")
root.configure(bg="lightblue")

tk.Label(root, text="Username:").pack(pady=5)
username_entry = tk.Entry(root)
username_entry.pack(pady=5)

tk.Label(root, text="Password:").pack(pady=5)
password_entry = tk.Entry(root, show="*")
password_entry.pack(pady=5)

tk.Button(root, text="Login", command=login).pack(pady=20)

root.mainloop()
