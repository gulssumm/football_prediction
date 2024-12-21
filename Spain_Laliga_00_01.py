from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Set up Chrome WebDriver (ensure you have ChromeDriver installed)
chrome_options = Options()
#chrome_options.add_argument("--headless")  # Run in headless mode (no browser window)
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# Update the path to your ChromeDriver
driver = webdriver.Chrome(options=chrome_options)

try:
    # URL of the match page
    url = "https://www.transfermarkt.com/real-sociedad_racing-santander/index/spielbericht/1089930"
    driver.get(url)

    # Extract league name
    league_name = driver.find_element(By.CLASS_NAME, "direct-headline__link").text.strip()

    # Extract teams and score
    teams = driver.find_elements(By.CLASS_NAME, "vereinprofil_tooltip")
    home_team = teams[0].text.strip()
    away_team = teams[1].text.strip()
    score = driver.find_element(By.CLASS_NAME, "sb-endstand").text.strip()

    # Extract match date
    date_element = driver.find_element(By.CLASS_NAME, "sb-datum").text.strip()

    # Extract lineups (players and manager)
    lineups = driver.find_elements(By.CLASS_NAME, "aufstellung-spieler-container")
    home_lineup = lineups[0]
    away_lineup = lineups[1]

    def extract_players(lineup):
        # Group players by positions
        positions = ["goalkeeper", "defense", "midfield", "attack"]
        players = {position: [] for position in positions}

        for position in positions:
            try:
                position_section = lineup.find_element(By.CLASS_NAME, f"sb-formation-{position}")
                player_elements = position_section.find_elements(By.CLASS_NAME, "spielprofil_tooltip")
                players[position] = [player.text.strip() for player in player_elements]
            except Exception:
                players[position] = []

        # Extract manager
        try:
            manager_section = lineup.find_element(By.CLASS_NAME, "sb-formation-trainer")
            manager = manager_section.find_element(By.CLASS_NAME, "spielprofil_tooltip").text.strip()
        except Exception:
            manager = None

        return players, manager

    home_players, home_manager = extract_players(home_lineup)
    away_players, away_manager = extract_players(away_lineup)

    # Print the results
    print("League Name:", league_name)
    print("Match Date:", date_element)
    print("Home Team:", home_team)
    print("Away Team:", away_team)
    print("Score:", score)
    print("\nHome Team Lineup:")
    print("Goalkeeper:", home_players["goalkeeper"])
    print("Defenders:", home_players["defense"])
    print("Midfielders:", home_players["midfield"])
    print("Forwards:", home_players["attack"])
    print("Manager:", home_manager)
    print("\nAway Team Lineup:")
    print("Goalkeeper:", away_players["goalkeeper"])
    print("Defenders:", away_players["defense"])
    print("Midfielders:", away_players["midfield"])
    print("Forwards:", away_players["attack"])
    print("Manager:", away_manager)

finally:
    # Close the driver
    driver.quit()
