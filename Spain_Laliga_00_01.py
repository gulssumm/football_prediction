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
home_team = get_element_text("xpath", "//div[@class='sb-team sb-heim']//a[2]")
away_team = get_element_text("xpath", "//div[@class='sb-team sb-gast']//a[2]")
score = get_element_text("xpath", "//div[@class='sb-endstand']")

# Match date
match_date = get_element_text("xpath", "//div[contains(@class, 'sb-spieldaten')]//a[2]")

# Extract players by position
def get_players_by_position(position_class):
    try:
        players = driver.find_elements(By.XPATH, position_class)
        return [player.text for player in players if player.text]
    except:
        return []

home_goalkeeper= get_players_by_position("//div[@class='large-12 columns']//table//tbody//tr//td[2]//a")
defenders = get_players_by_position("aufstellung-verteidiger")
midfielders = get_players_by_position("aufstellung-mittelfeld")
forwards = get_players_by_position("aufstellung-angriff")

# Manager
home_manager = get_element_text("xpath", "/html/body/div[1]/main/div[5]/div/div/div[1]/div[2]/table/tbody/tr[5]/td[2]/a")
away_manager = get_element_text("xpath", "/html/body/div[1]/main/div[5]/div/div/div[2]/div[2]/table/tbody/tr[5]/td[2]/a")

# Step 4: Print the data
print("League Name:", league_name)
print("Home Team:", home_team)
print("Away Team:", away_team)
print("Score:", score)
print("Match Date:", match_date)
print("Home Goalkeeper:", home_goalkeeper)
print("Defenders:", defenders)
print("Midfielders:", midfielders)
print("Forwards:", forwards)
print("Home Manager:", home_manager)
print("Away Manager:", away_manager)

# Step 5: Close the browser
driver.quit()
