from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup
import csv


def extract_team_info(url):
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode (no GUI)

    # Setup Selenium WebDriver
    driver = webdriver.Chrome(options=chrome_options)

    # Fetch the webpage
    driver.get(url)

    # Wait for the page to fully load (adjust time if necessary)
    time.sleep(5)

    # Get the page source after it has loaded
    html_content = driver.page_source

    # Close the browser
    driver.quit()

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract League Name
    league_name = soup.find('a', class_='direct-headline__link').get_text(strip=True)

    # Extract Match Date
    match_date_ = soup.find('p', class_='sb-datum hide-for-small').find_all('a')
    match_date = match_date_[1].get_text(strip=True) if len(match_date_) > 1 else "Date not found"

    # Extract Home and Away Teams
    home_team = soup.find('a', class_='sb-vereinslink').get_text(strip=True)
    away_team_ = soup.find('div', class_='sb-team sb-gast').find_all('a')
    away_team = away_team_[1].get_text(strip=True) if len(away_team_) > 1 else "Away team not found"

    # Extract Referee
    referee_tag = soup.find('p', class_='sb-zusatzinfos').find('a', title=True)
    referee = referee_tag.get_text(strip=True) if referee_tag else "N/A"

    # Extract player roles function
    def extract_players(role):
        elements = soup.find_all('td', string=role)
        players = []
        for elem in elements:
            player = elem.find_next('td').get_text(strip=True)
            players.append(player)
        return players if players else ["Not found", "Not found"]

    # Extract players for each role
    goalkeepers = extract_players("Goalkeeper")
    defenders = extract_players("Defenders")
    midfielders = extract_players("Midfielders")
    forwards = extract_players("Forwards")
    managers = extract_players("Manager")

    # Return extracted data as a dictionary
    return {
        "URL": url,
        "League Name": league_name,
        "Match Date": match_date,
        "Home Team": home_team,
        "Away Team": away_team,
        "Referee": referee,
        "Home Goalkeeper": goalkeepers[0],
        "Away Goalkeeper": goalkeepers[1],
        "Home Defender": defenders[0],
        "Away Defender": defenders[1],
        "Home Midfielder": midfielders[0],
        "Away Midfielder": midfielders[1],
        "Home Forward": forwards[0],
        "Away Forward": forwards[1],
        "Home Manager": managers[0],
        "Away Manager": managers[1],
    }


# Generate URLs dynamically
start_url = "https://www.transfermarkt.com/real-sociedad_racing-santander/index/spielbericht/1089930"
end_url = "https://www.transfermarkt.com/real-sociedad_racing-santander/index/spielbericht/1089939"
start_id = int(start_url.split('/')[-1])
end_id = int(end_url.split('/')[-1])

# List of URLs
urls = [f"https://www.transfermarkt.com/real-sociedad_racing-santander/index/spielbericht/{id_}" for id_ in range(start_id, end_id + 1)]

# CSV file to save the data
output_file = "match_data.csv"

# Write data to CSV
with open(output_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=[
        "URL", "League Name", "Match Date", "Home Team", "Away Team", "Referee",
        "Home Goalkeeper", "Away Goalkeeper", "Home Defender", "Away Defender",
        "Home Midfielder", "Away Midfielder", "Home Forward", "Away Forward",
        "Home Manager", "Away Manager"
    ])
    writer.writeheader()  # Write header row
    for url in urls:
        try:
            data = extract_team_info(url)
            writer.writerow(data)
            print(f"Data for {url} saved successfully.")
        except Exception as e:
            print(f"Error processing {url}: {e}")
