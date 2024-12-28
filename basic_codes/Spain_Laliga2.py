from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup
import csv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Function to extract match information
def extract_matches(url):
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode (no GUI)

    # Setup Selenium WebDriver
    driver = webdriver.Chrome(options=chrome_options)

    # Fetch the webpage
    driver.get(url)

    # Wait for the page to fully load (adjust time if necessary)
    time.sleep(5)

    try:
        # Wait for the main table or any specific element to load (adjust the element as needed)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'tr')))
    except Exception as e:
        print(f"Error waiting for page load: {e}")
        driver.quit()
        return []

    # Get the page source after it has loaded
    html_content = driver.page_source

    # Close the browser
    driver.quit()

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract League Name
    league_name_div = soup.find('div', class_='data-header__headline-wrapper data-header__headline-wrapper--oswald')
    league_name = league_name_div.get_text(strip=True) if league_name_div else "League name not found"

    # Extract match data
    matches = []
    classes = soup.find('div','large-6 columns')
    rows = classes.find_all('tr')
    for row in rows:
        try:
            # Extract date
            date_td = row.find('td', class_='hide-for-small')
            date = date_td.find('a').get_text(strip=True) if date_td and date_td.find('a') else "Date not found"

            # Extract home team
            home_team_td = row.find('td', class_='text-right no-border-rechts hauptlink')
            home_team = home_team_td.find('a').get_text(strip=True) if home_team_td and home_team_td.find('a') else "Home team not found"

            # Extract away team
            away_team_td = row.find('td', class_='no-border-links hauptlink')
            away_team = away_team_td.find('a').get_text(strip=True) if away_team_td and away_team_td.find('a') else "Away team not found"

            # Extract score
            score_td = row.find('td', class_='zentriert hauptlink')
            score = score_td.find('a', class_='ergebnis-link').get_text(strip=True) if score_td and score_td.find('a',class_='ergebnis-link') else "Score not found"

            matches.append({
                "League Name": league_name,
                "Match Date": date,
                "Home Team": home_team,
                "Away Team": away_team,
                "Score": score
            })
        except AttributeError:
            # Skip rows with incomplete data
            continue
    return matches

# Generate URLs dynamically
base_url = "https://www.transfermarkt.com/laliga2/gesamtspielplan/wettbewerb/ES2?saison_id={year}"
urls = [base_url.format(year=year) for year in range(2000, 2002)]  # From 2000 to 2024

# File to save the combined data
output_file = "2000_24_SP_laliga2.csv"

# Write data to a CSV
with open(output_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=["League Name", "Match Date", "Home Team", "Away Team", "Score"])
    writer.writeheader()  # Write header row

    # Loop through each URL
    for url in urls:
        try:
            print(f"Processing {url}...")
            match_data = extract_matches(url)  # Call the extraction function
            writer.writerows(match_data)  # Save the data to the CSV file
            print(f"Data for {url} saved successfully.")
        except Exception as e:
            print(f"Error processing {url}: {e}")
