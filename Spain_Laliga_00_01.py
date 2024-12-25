from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
def get_element_text(selector_type, value, attribute=None):
    try:
        if selector_type == "xpath":
            element = driver.find_element(By.XPATH, value)
            # Eğer attribute verilmişse, attribute değerini al
            if attribute:
                return element.get_attribute(attribute)
            # Eğer attribute verilmemişse, text değerini al
            else:
                return element.text
        elif selector_type == "class":
            element = driver.find_element(By.CLASS_NAME, value)
            # Eğer attribute verilmişse, attribute değerini al
            if attribute:
                return element.get_attribute(attribute)
            # Eğer attribute verilmemişse, text değerini al
            else:
                return element.text
    except Exception as e:
        print(f"Error: {e}")
        return None
# Step 3: Wait for elements to be loaded (use explicit waits)
wait = WebDriverWait(driver, 10)  # Wait for a maximum of 10 seconds

# Wait for the teams and score to load
wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='sb-team sb-heim']//a[2]")))

# League name
league_name = get_element_text("xpath", "//span/a")

# Teams and score
home_team = get_element_text("xpath", "//div[@class='sb-team sb-heim']//a[2]")
away_team = get_element_text("xpath", "//div[@class='sb-team sb-gast']//a[2]")
score = get_element_text("xpath", "//div[@class='sb-endstand']")
referee = get_element_text("xpath", "//p[@class='sb-zusatzinfos']//a[1]","title")

# Match date
match_date = get_element_text("xpath", "//div[contains(@class, 'sb-spieldaten')]//a[2]")

# Extract players by position
def get_players_by_position(position_xpath):
    try:
        players = driver.find_elements(By.XPATH, position_xpath)
        return [player.text for player in players if player.text]
    except Exception as e:
        print(f"Error: {e}")
        return []

# Home Goalkeeper
home_goalkeeper = get_players_by_position("//div[@class='large-12 columns']//table//tbody//tr//td[2]//a")
home_defender = get_players_by_position("//div[@class='large-12 columns']//table//tbody//tr[2]//td[2]//a")
home_midfielder = get_players_by_position("//div[@class='large-12 columns']//table//tbody//tr[3]//td[2]//a")
home_forward = get_players_by_position("//div[@class='large-12 columns']//table//tbody//tr[4]//td[2]//a")

# Ensure elements are loaded
home_manager = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.XPATH, "//div[@class='large-12 columns']//table//tbody//tr[5]//td[2]//a"))
).text

away_manager = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.XPATH, "//div[@class='large-6 columns']//table//tbody//tr[5]//td[2]//a"))
).text

# Step 4: Print the data
print("League Name:", league_name)
print("Home Team:", home_team)
print("Away Team:", away_team)
print("Score:", score)
print("Referee:", referee)
print("Match Date:", match_date)
print("Home Goalkeeper:", home_goalkeeper)
print("Defenders:", home_defender)
print("Midfielders:", home_midfielder)
print("Forwards:", home_forward)
print("Home Manager:", home_manager)
print("Away Manager:", away_manager)

# Step 5: Close the browser
driver.quit()
