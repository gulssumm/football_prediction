from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import csv
import time

# Function to scrape data using Selenium and BeautifulSoup
def scrape_matches(url):
    # Configure Selenium
    options = Options()
    options.add_argument("--headless")  # Run in headless mode (optional)
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=options)

    # Open the URL
    driver.get(url)
    time.sleep(5)  # Wait for the page to fully load (adjust as needed)

    # Get page source and parse with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    # Parse the data
    match_data = []
    weeks = soup.find_all('td', class_='belirginYazi')  # Find the week sections
    for week in weeks:
        matches_table = week.find_next('table')  # Get the matches table for the week
        rows = matches_table.find_all('tr')

        for row in rows:
            cells = row.find_all('td', class_='altCizgi')  # Find the relevant table cells
            if len(cells) == 3:  # Ensure it's a valid match row
                # Extract data from the <a> tags within <td>
                home_team = cells[0].find('a').text.strip() if cells[0].find('a') else None
                score = cells[1].text.strip() if cells[1].find('a') else None
                print(score)
                away_team = cells[2].find('a').text.strip() if cells[2].find('a') else None

                # Validate data and append only valid rows
                if home_team and away_team and score:
                    match_data.append({
                        'Home Team': home_team,
                        'Score': score,
                        'Away Team': away_team,
                    })

    return match_data

# Function to save data to CSV
def save_to_csv(data, filename):
    if not data:
        print("No data to save.")
        return
    keys = data[0].keys()  # Get the headers from the first dictionary
    with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=keys)
        writer.writeheader()  # Write headers
        writer.writerows(data)  # Write data rows
    print(f"Data successfully saved to {filename}")

# URL of the website to scrape
url = 'https://www.tff.org/Default.aspx?pageID=1650&hafta=1#macctl00_MPane_m_1650_12858_ctnr_m_1650_12858'

# Scrape the matches and save to CSV
try:
    matches = scrape_matches(url)
    if matches:
        save_to_csv(matches, '2000_24_TR_nesine2lig.csv')  # Save the data to matches.csv
    else:
        print("No match data found.")
except Exception as e:
    print(f"An error occurred: {e}")
