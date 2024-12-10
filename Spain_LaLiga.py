from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

# Set up Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode (optional)
driver = webdriver.Chrome(options=options)

# URL of the page you want to scrape
url = 'https://www.skysports.com/la-liga-results/2000-01'
driver.get(url)

# Let the page load completely
driver.implicitly_wait(5)

# Initialize empty lists to store the extracted data
dates = []
home_teams = []
away_teams = []
home_scores = []
away_scores = []

# Get all headers and their following matches
sections = driver.find_elements(By.XPATH, "//div[contains(@class, 'fixres__body')]/..")

# Loop through each section
for section in sections:
    # Find all matches under this section
    match_elements = section.find_elements(By.CLASS_NAME, 'fixres__item')

    for match in match_elements:
        # Extract the date from the header
        date_header = section.find_element(By.CLASS_NAME, 'fixres__header1')
        date = date_header.text.strip()

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
        dates.append(date)
        home_teams.append(home_team)
        away_teams.append(away_team)
        home_scores.append(home_score)
        away_scores.append(away_score)

# Close the driver after scraping
driver.quit()

# Create a DataFrame to organize the data
data = {
    'Date': dates,
    'Home Team': home_teams,
    'Away Team': away_teams,
    'Home Score': home_scores,
    'Away Score': away_scores
}
df = pd.DataFrame(data)

# Print the results
print(df)

# Optionally, save the data to a CSV file
#df.to_csv('la_liga_results.csv', index=False)
