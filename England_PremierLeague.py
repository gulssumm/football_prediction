from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

# Set up Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode (optional)
driver = webdriver.Chrome(options=options)

# URL of the page you want to scrape
url = 'https://www.skysports.com/premier-league-results/2000-01'
driver.get(url)

# Let the page load completely
driver.implicitly_wait(5)

# Initialize empty lists to store the extracted data
leagues = []
dates = []
home_teams = []
away_teams = []
home_scores = []
away_scores = []


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
    #print(f"Date {i+1}: {date}")



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
        leagues.append(league)
        dates.append(date)
        home_teams.append(home_team)
        away_teams.append(away_team)
        home_scores.append(home_score)
        away_scores.append(away_score)

# Close the driver after scraping
driver.quit()

# Create a DataFrame to organize the data
data = {
    'League': leagues,
    'Date': dates,
    'Home Team': home_teams,
    'Away Team': away_teams,
    'Home Score': home_scores,
    'Away Score': away_scores
}
df = pd.DataFrame(data)

# Print the results
#print(df)

# Optionally, save the data to a CSV file
df.to_csv('premier_league_results.csv', index=False)
