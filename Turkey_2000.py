from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Initialize the Selenium WebDriver
driver = webdriver.Chrome()  # Ensure ChromeDriver is installed and in PATH
url = 'https://www.tff.org/Default.aspx?pageID=552&hafta=1#grp'
driver.get(url)

# Wait for the page to load
time.sleep(5)

try:
    # Locate the element using the full XPath
    league_element = driver.find_element(By.XPATH, "/html/body/form/div[4]/div/section[2]/article[2]/div[1]/b/i/a")
    league_name = league_element.text.strip()
    print("League Name:", league_name)

    # Locate all home team names using a relative XPath
    home_teams = driver.find_elements(By.XPATH, "//td[@class='haftaninMaclariEv']/a/span")

    # Extract the text of each home team and store in a list
    home_team_names = [team.text.strip() for team in home_teams]

    # Print the list of home team names
    print("Home Team Names:")
    for name in home_team_names:
        print(name)

except Exception as e:
    print("Error:", e)

# Quit the driver
driver.quit()
