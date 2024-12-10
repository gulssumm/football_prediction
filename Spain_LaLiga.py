from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd

# Set up Selenium WebDriver
#service = Service("path/to/chromedriver")  # Update this path to your ChromeDriver location
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode (optional)
driver = webdriver.Chrome(options=options)

# URL of the page you want to scrape
url = 'https://www.skysports.com/la-liga-results/2000-01'
driver.get(url)

# Let the page load completely
driver.implicitly_wait(5)  # Adjust the wait time if needed

# Parse the page content with BeautifulSoup
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Close the driver after page load
driver.quit()

# Find the container for all matches
matches = soup.find_all('div', {'class': 'fixres__item'})

# Initialize empty lists to store the extracted data
dates = []
home_teams = []
away_teams = []
home_scores = []
away_scores = []
scores = []

# Loop through each match section and extract details
for match in matches:
    # Extract the date (the date is in a separate header above the match section)
    date_header = match.find_previous('h3', {'class': 'fixres__header1'})
    date = date_header.get_text(strip=True) if date_header else 'Unknown'

    # Extract teams
    team_elements = match.find_all('span', {'class': 'swap-text__target'})
    if len(team_elements) == 2:
        home_team = team_elements[0].get_text(strip=True)
        away_team = team_elements[1].get_text(strip=True)
    else:
        home_team, away_team = 'Unknown', 'Unknown'

    # Extract score
    score_element = match.find('span', {'class': 'matches__item-col matches__status'})
    score = score_element.get_text(strip=True) if score_element else 'N/A'

    # Append the data to the lists
    dates.append(date)
    home_teams.append(home_team)
    away_teams.append(away_team)
    scores.append(score)
    #home_scores.append(home_score)
    #away_scores.append(away_score)

# Create a DataFrame to organize the data
data = {
    'Date': dates,
    'Home Team': home_team,
    'Away Team': away_team,
    'Score': score
}
df = pd.DataFrame(data)

# Print the results
print(df)

# Optionally, save the data to a CSV file
#df.to_csv('la_liga_results.csv', index=False)