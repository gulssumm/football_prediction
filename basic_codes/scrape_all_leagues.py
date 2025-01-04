from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

# Set up Selenium WebDriver
options = webdriver.ChromeOptions()
# options.add_argument("--headless")  # Run in headless mode (optional)
driver = webdriver.Chrome(options=options)

# Scrape function for any league
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

    # Loop through each URL and scrape the data
    for url in urls:
        url = url.strip()  # Remove any leading/trailing whitespace
        print(f"Processed URL: '{url}'")  # Debug print
        if not url:
            print("Skipping empty URL")
            continue
        if not url.startswith("http"):
            print(f"Skipping invalid URL: '{url}'")
            continue
        if not url:
            continue  # Skip empty lines

        # Open the URL
        driver.get(url)
        driver.implicitly_wait(5)  # Wait for the page to load

        # Extract league name (assume it's a global header)
        try:
            league_header = driver.find_element(By.CLASS_NAME, 'swap-text__target')
            league = league_header.text.strip()
        except:
            league = 'Unknown'

        # Get all sections containing headers and matches
        sections = driver.find_elements(By.XPATH, "//div[contains(@class, 'fixres__body')]/..")

        # Loop through each section
        for section in sections:
            date_headers = driver.find_elements(By.XPATH, "//h3[contains(@class, 'fixres__header1')]")
            for i, header in enumerate(date_headers):
                date = driver.execute_script("return arguments[0].textContent;", header).strip() or "Unknown"

                # Find all matches under this section
                match_elements = section.find_elements(By.CLASS_NAME, 'fixres__item')

                for match in match_elements:
                    # Extract teams
                    try:
                        team_elements = match.find_elements(By.CLASS_NAME, 'swap-text__target')
                        home_team = team_elements[0].text if len(team_elements) > 0 else 'Unknown'
                        away_team = team_elements[1].text if len(team_elements) > 1 else 'Unknown'
                    except:
                        home_team, away_team = 'Unknown', 'Unknown'

                    # Extract scores
                    try:
                        score_elements = match.find_elements(By.CLASS_NAME, 'score')
                        home_score = score_elements[0].text if len(score_elements) > 0 else '0'
                        away_score = score_elements[1].text if len(score_elements) > 1 else '0'
                    except:
                        home_score, away_score = '0', '0'

                    # Store the data
                    leagues.append(league_name)
                    dates.append(date)
                    home_teams.append(home_team)
                    away_teams.append(away_team)
                    home_scores.append(home_score)
                    away_scores.append(away_score)

    # Create a DataFrame and save the data as a CSV file
    df = pd.DataFrame({
        'League': leagues,
        'Date': dates,
        'Home_Team': home_teams,
        'Away_Team': away_teams,
        'Home_Score': home_scores,
        'Away_Score': away_scores
    })

    # Save the DataFrame to a CSV file
    csv_file = f"{initial_year}_{end_year}_{league_name.replace(' ', '_').lower()}.csv"
    df.to_csv(csv_file, index=False)
    print(f"Scraped data saved to {csv_file}")
