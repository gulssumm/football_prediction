from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode (no GUI)

# Setup Selenium WebDriver
driver = webdriver.Chrome(options=chrome_options)

# URL of the webpage
url = "https://www.transfermarkt.com/real-sociedad_racing-santander/index/spielbericht/1089930"

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

# Find the first "Goalkeeper" entry
goalkeeper_elements = soup.find_all('td', string="Goalkeeper")

# Extract the name of the first goalkeeper
if goalkeeper_elements:
    first_goalkeeper = goalkeeper_elements[0].find_next('td').get_text(strip=True)
    second_goalkeeper = goalkeeper_elements[1].find_next('td').get_text(strip=True)
    print(f"First Goalkeeper: {first_goalkeeper}")
    print(f"Second Goalkeeper: {second_goalkeeper}")
else:
    print("Goalkeeper not found.")

# Find defenders
defender_elements = soup.find_all('td', string="Defenders")

# Extract names of defenders
if defender_elements:
    first_defender = defender_elements[0].find_next('td').get_text(strip=True)
    second_defender = defender_elements[1].find_next('td').get_text(strip=True)
    print(f"First Defender: {first_defender}")
    print(f"Second Defender: {second_defender}")
else:
    print("Defender not found.")

# Find midfielders (searching for rows containing 'Midfielder' in the team lineup section)
midfielder_elements = soup.find_all('td', string="Midfielders")

# Extract names of midfielders
if midfielder_elements:
    first_midfielder = midfielder_elements[0].find_next('td').get_text(strip=True)
    second_midfielder = midfielder_elements[1].find_next('td').get_text(strip=True)
    print(f"First Midfielder: {first_midfielder}")
    print(f"Second Midfielder: {second_midfielder}")
else:
    print("Midfielder not found.")

# Find midfielders (searching for rows containing 'Midfielder' in the team lineup section)
forward_elements = soup.find_all('td', string="Forwards")

# Extract names of midfielders
if midfielder_elements:
    first_forward = forward_elements[0].find_next('td').get_text(strip=True)
    second_forward = forward_elements[1].find_next('td').get_text(strip=True)
    print(f"First Midfielder: {first_forward}")
    print(f"Second Midfielder: {second_forward}")
else:
    print("Forward not found.")


# Find midfielders (searching for rows containing 'Midfielder' in the team lineup section)
manager_elements = soup.find_all('td', string="Manager")

# Extract names of midfielders
if manager_elements:
    first_forward = manager_elements[0].find_next('td').get_text(strip=True)
    second_forward = manager_elements[1].find_next('td').get_text(strip=True)
    print(f"First Manager: {first_forward}")
    print(f"Second Manager: {second_forward}")
else:
    print("Manager not found.")