from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

# Set up Selenium WebDriver
options = webdriver.ChromeOptions()
# options.add_argument("--headless")  # Uncomment to run in headless mode
driver = webdriver.Chrome(options=options)

def filter_urls_by_year(urls, initial_year, end_year):
    filtered_urls = []
    for url in urls:
        url = url.strip()  # Clean up the URL

        # Extract the year part from the URL
        year_part = url.split("/")[-1]  # Adjust this based on your URL structure
        try:
            first_year, second_year = map(int, year_part.split("-"))
            full_second_year = 2000 + second_year
            if initial_year <= first_year <= end_year or initial_year <= full_second_year <= end_year:
                filtered_urls.append(url)
        except ValueError:
            print(f"Skipping URL with invalid year format: {url}")

    print(f"Filtered URLs: {filtered_urls}")
    return filtered_urls

def scrape_league(url_file, league_name, initial_year, end_year):
    # Initialize empty lists to store the extracted data
    leagues = []
    dates = []
    home_teams = []
    away_teams = []
    home_scores = []
    away_scores = []

    # Read URLs from the file
    with open(url_file, "r") as file:
        urls = file.readlines()

    # Filter the URLs based on the year range
    filtered_urls = filter_urls_by_year(urls, initial_year, end_year)

    # Loop through each URL and scrape the data
    for url in filtered_urls:
        print(f"Processing URL: {url}")

        try:
            driver.get(url)
            driver.implicitly_wait(5)

            # Extract matches
            matches = driver.find_elements(By.CLASS_NAME, "fixres__item")
            for match in matches:
                try:
                    date = driver.find_element(By.CLASS_NAME, "fixres__header1").text.strip()
                    teams = match.find_elements(By.CLASS_NAME, "swap-text__target")
                    scores = match.find_elements(By.CLASS_NAME, "matches__teamscores-side")

                    home_team = teams[0].text.strip() if len(teams) > 0 else "Unknown"
                    away_team = teams[1].text.strip() if len(teams) > 1 else "Unknown"
                    home_score = scores[0].text.strip() if len(scores) > 0 else "N/A"
                    away_score = scores[1].text.strip() if len(scores) > 1 else "N/A"

                    # Append data
                    leagues.append(league_name)
                    dates.append(date)
                    home_teams.append(home_team)
                    away_teams.append(away_team)
                    home_scores.append(home_score)
                    away_scores.append(away_score)

                except Exception as e:
                    print(f"Error parsing match: {e}")
        except Exception as e:
            print(f"Error loading URL {url}: {e}")

    driver.quit()

    # Save results to CSV
    data = {
        "League": leagues,
        "Date": dates,
        "Home Team": home_teams,
        "Away Team": away_teams,
        "Home Score": home_scores,
        "Away Score": away_scores,
    }
    df = pd.DataFrame(data)
    output_file = f"{initial_year}_{end_year}_{league_name.replace(' ', '_')}.csv"
    df.to_csv(output_file, index=False)
    print(f"Data scraping complete. Results saved to {output_file}")

# Usage example
#scrape_league("../basic_codes/URLS/urls_LA_LIGA.txt", "La Liga", 2024, 2025)
