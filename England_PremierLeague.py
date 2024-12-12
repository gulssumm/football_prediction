from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import os

file_path = 'c:\\Users\\Lenovo\\Desktop\\FutboolMatch\\urls.txt'
if os.path.exists(file_path):
    with open(file_path, 'r') as file:
        urls = [line.strip() for line in file.readlines()]
else:
    print(f"File not found: {file_path}")


# Set up Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode (optional)
driver = webdriver.Chrome(options=options)


# Initialize empty lists to store the extracted data
all_leagues = []
all_dates = []
all_home_teams = []
all_away_teams = []
all_home_scores = []
all_away_scores = []

# Loop through each URL
for url in urls:
    print(f"Scraping data from: {url}")
    driver.get(url)
    driver.implicitly_wait(5)

    # Extract league name (assume it's a global header)
    try:
        league_header = driver.find_element(By.CLASS_NAME, 'swap-text__target')
        league = league_header.text.strip()
    except:
        league = 'Unknown'

    # Get all sections containing headers and matches
    sections = driver.find_elements(By.XPATH, "//div[contains(@class, 'fixres__body')]/..")

    for section in sections:
        date_headers = driver.find_elements(By.XPATH, "//h3[contains(@class, 'fixres__header1')]")
        for header in date_headers:
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
                    score_elements = match.find_elements(By.CLASS_NAME, 'matches__teamscores-side')
                    home_score = score_elements[0].text if len(score_elements) > 0 else 'N/A'
                    away_score = score_elements[1].text if len(score_elements) > 1 else 'N/A'
                except:
                    home_score, away_score = 'N/A', 'N/A'

                # Append the data to the lists
                all_leagues.append(league)
                all_dates.append(date)
                all_home_teams.append(home_team)
                all_away_teams.append(away_team)
                all_home_scores.append(home_score)
                all_away_scores.append(away_score)

# Close the driver after scraping
driver.quit()

# Create a DataFrame to organize the data
data = {
    'League': all_leagues,
    'Date': all_dates,
    'Home Team': all_home_teams,
    'Away Team': all_away_teams,
    'Home Score': all_home_scores,
    'Away Score': all_away_scores
}
df = pd.DataFrame(data)

# Save the data to a CSV file
df.to_csv('premier_league_results_all_seasons.csv', index=False)

print("Data scraping completed successfully!")
