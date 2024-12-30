import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup
import csv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Function to clean team names
def clean_team_name(name):
    if name:
        return re.sub(r"\(\d+\.\)", "", name).strip()  # Remove ranking indicators like "(4.)"
    return None


# Function to clean the score
def clean_score(score):
    # Check if score is None or not a string, return as is if so
    if not score or not isinstance(score, str):
        return score

    # If the score looks like a timestamp (e.g., "1:00:00 AM"), convert it to "1:0"
    if re.match(r'^\d{1,2}:\d{2}:\d{2} [APM]{2}$', score):
        parts = score.split(":")
        return f"{parts[0]}:{parts[1]}"

    return score  # Return the score as is if no match

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
    # Find the container with the class `large-6 columns`
    matches_container = soup.find_all('div', class_='large-6 columns')

    # Iterate through each match container to extract data
    for container in matches_container:
        rows = container.find_all('tr', class_=lambda x: x != 'bg_blau_20')  # Exclude headers and separators
        for row in rows:
            # Extract data
            date = row.find('td', class_='hide-for-small')
            home_team = row.find('td', class_='text-right no-border-rechts hauptlink')
            away_team = row.find('td', class_='no-border-links hauptlink')
            score_element = row.find('td', class_='zentriert hauptlink')

            # Clean and extract data
            date = date.get_text(strip=True) if date else None
            home_team = clean_team_name(home_team.get_text(strip=True)) if home_team else None
            away_team = clean_team_name(away_team.get_text(strip=True)) if away_team else None
            score = score_element.get_text(strip=True) if score_element else None
            score = clean_score(score)
            #print(score)

            matches.append({
                "League Name": league_name,
                "Match Date": date,
                "Home Team": home_team,
                "Away Team": away_team,
                "Score": score
            })
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
