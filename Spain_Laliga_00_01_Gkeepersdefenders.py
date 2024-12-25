from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup


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
    if len(match_date_) > 1:
        match_date = match_date_[1].get_text(strip=True)  # Get date in format (e.g. Sat, 9/9/00)
    else:
        match_date = "Date not found"


    # Extract Home and Away Teams
    home_team = soup.find('a', class_='sb-vereinslink').get_text(strip=True)
    away_team_ = soup.find('div', class_='sb-team sb-gast').find_all('a')
    if len(away_team_) > 1:
        away_team = away_team_[1].get_text(strip=True)
    else:
        away_team = "Away team not found"


    # Extract Referee
    referee_tag = soup.find('p', class_='sb-zusatzinfos').find('a', title=True)
    referee = referee_tag.get_text(strip=True) if referee_tag else "N/A"

    # Print the extracted information
    print(f"League Name: {league_name}")
    print(f"Match Date: {match_date}")
    print(f"Home Team: {home_team}")
    print(f"Away Team: {away_team}")
    print(f"Referee: {referee}")

    # Function to extract player roles
    def extract_players(role):
        elements = soup.find_all('td', string=role)
        players = []
        if elements:
            for elem in elements:
                player = elem.find_next('td').get_text(strip=True)
                players.append(player)
        else:
            print(f"{role} not found.")
        return players

    # Extract goalkeepers
    goalkeepers = extract_players("Goalkeeper")
    home_goalkeeper = goalkeepers[0]
    away_goalkeeper = goalkeepers[1]
    print("Goalkeepers:")
    print(f"Home Goalkeeper:{home_goalkeeper}")
    print(f"Away Goalkeeper:{away_goalkeeper}")

    # Extract defenders
    defenders = extract_players("Defenders")
    home_defender = defenders[0]
    away_defender = defenders[1]
    print("Defenders:")
    print(f"Home Defender:{home_defender}")
    print(f"Away Defender:{away_defender}")

    # Extract midfielders
    midfielders = extract_players("Midfielders")
    home_midfielder = midfielders[0]
    away_midfielder = midfielders[1]
    print("Midfielders:")
    print(f"Home Midfielder:{home_midfielder}")
    print(f"Away Midfielder:{away_midfielder}")

    # Extract forwards
    forwards = extract_players("Forwards")
    home_forward = forwards[0]
    away_forward = forwards[1]
    print("Forwards:")
    print(f"Home Forward:{home_forward}")
    print(f"Away Forward:{away_forward}")

    # Extract managers
    managers = extract_players("Manager")
    home_manager = managers[0]
    away_manager = managers[1]
    print("Managers:")
    print(f"Home Manager:{home_manager}")
    print(f"Away Manager:{away_manager}")

# URL of the webpage
url = "https://www.transfermarkt.com/real-sociedad_racing-santander/index/spielbericht/1089930"

# Call the function with the URL
extract_team_info(url)
