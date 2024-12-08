import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the page you want to scrape
url = 'https://www.skysports.com/la-liga-results/2000-01'

# Send a GET request to fetch the page content
response = requests.get(url)
response.raise_for_status()  # Check if the request was successful

# Parse the page content with BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Find the section containing the match results
# Based on the structure of the page, we need to locate the right div containing the matches
match_sections = soup.find_all('div', {'class': 'match-day'})

# Initialize empty lists to store the extracted data
dates = []
teams = []
scores = []

# Loop through each match section and extract details
for section in match_sections:
    # Find the date for the match day
    date = section.find('span', {'class': 'match-day__date'})
    if date:
        dates.append(date.get_text(strip=True))

    # Find the teams and scores for the matches in this section
    matches = section.find_all('div', {'class': 'match'})
    for match in matches:
        # Extract teams and score
        home_team = match.find('span', {'class': 'swap-text__target'}).get_text(strip=True)
        away_team = match.find('span', {'class': 'swap-text__target'}).get_text(strip=True)
        score = match.find('span', {'class': 'score'}).get_text(strip=True)

        # Append the data to the lists
        teams.append(f"{team1} vs {team2}")
        scores.append(score)


# Create a DataFrame to organize the data
data = {
    'Date': dates,
    'Teams': teams,
    'Score': scores
}
#df = pd.DataFrame(data)

# Print the results
#print(df)

# Optionally, save the data to a CSV file
#df.to_csv('la_liga_results.csv', index=False)
