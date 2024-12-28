from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import os

# File path for URLs
file_path = '../basic_codes/URLS/urls_EN_PremierLeague.txt'

# Check if the file exists
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
        # Extract the main date (e.g., May 2001)
        date_headers = section.find_elements(By.XPATH, ".//h3[contains(@class, 'fixres__header1')]")
        detailed_date_headers = section.find_elements(By.XPATH, ".//h4[contains(@class, 'fixres__header2')]")
        
        for header, detailed_header in zip(date_headers, detailed_date_headers):
            main_date = driver.execute_script("return arguments[0].textContent;", header).strip() or "Unknown"
            detailed_date = driver.execute_script("return arguments[0].textContent;", detailed_header).strip() or "Unknown"
            
            # Combine main date and detailed date
            combined_date = f"{main_date}, {detailed_date}"

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
                all_dates.append(combined_date)
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

# Print the results to the terminal for testing
print(df)

# Optionally, save the data to a CSV file
df.to_csv('2000_24_EN_Premierleague.csv', index=False)

print("Data scraping completed successfully!")
