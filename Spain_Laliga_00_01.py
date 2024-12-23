from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Set up Chrome WebDriver (ensure you have ChromeDriver installed)
chrome_options = Options()
#chrome_options.add_argument("--headless")  # Run in headless mode (no browser window)
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# Step 1: Set up the WebDriver
driver = webdriver.Chrome(options=chrome_options)
url = "https://www.transfermarkt.com/real-sociedad_racing-santander/index/spielbericht/1089930"
driver.get(url)

# Step 2: Define functions to extract data
def get_element_text(selector_type, value):
    try:
        if selector_type == "xpath":
            return driver.find_element(By.XPATH, value).text
        elif selector_type == "class":
            return driver.find_element(By.CLASS_NAME, value).text
    except:
        return None

# Step 3: Extract Data
# League name
league_name = get_element_text("xpath", "//span/a")

# Teams and score
home_team = get_element_text("xpath", "//div[@class='sb-team sb-heim']//a")
away_team = get_element_text("xpath", "//div[@class='sb-team sb-gast']//a")
score = get_element_text("xpath", "//div[@class='sb-endstand']")

# Match date
match_date = get_element_text("xpath", "//div[contains(@class, 'spielbericht')]//span[@class='sb-datum']")

# Extract players by position
def get_players_by_position(position_class):
    try:
        players = driver.find_elements(By.CLASS_NAME, position_class)
        return [player.text for player in players if player.text]
    except:
        return []

goalkeepers = get_players_by_position("aufstellung-keeper")
defenders = get_players_by_position("aufstellung-verteidiger")
midfielders = get_players_by_position("aufstellung-mittelfeld")
forwards = get_players_by_position("aufstellung-angriff")

# Manager
home_manager = get_element_text("xpath", "//div[contains(@class, 'trainer-name-heim')]//a")
away_manager = get_element_text("xpath", "//div[contains(@class, 'trainer-name-gast')]//a")

# Step 4: Print the data
print("League Name:", league_name)
print("Home Team:", home_team)
print("Away Team:", away_team)
print("Score:", score)
print("Match Date:", match_date)
print("Goalkeepers:", goalkeepers)
print("Defenders:", defenders)
print("Midfielders:", midfielders)
print("Forwards:", forwards)
print("Home Manager:", home_manager)
print("Away Manager:", away_manager)

# Step 5: Close the browser
driver.quit()
