from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Configure WebDriver
options = webdriver.ChromeOptions()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
driver = webdriver.Chrome(options=options)

try:
    # Open the webpage
    url = "https://www.transfermarkt.com/laliga/gesamtspielplan/wettbewerb/ES1/saison_id/2000"
    driver.get(url)

    # Wait for the page to load completely
    WebDriverWait(driver, 60).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )
    print("Page fully loaded!")

    # Debugging: Save a screenshot
    driver.save_screenshot("page_loaded.png")

    # Wait for the table to appear
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "//table[contains(@class, 'box')]"))
    )
    print("Table found!")

    # Debugging: Print the page source
    with open("page_source.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)

    # Extract table rows
    rows = driver.find_elements(By.XPATH, "//table[contains(@class, 'box')]//tr")
    print(f"Number of rows found: {len(rows)}")

except Exception as e:
    print(f"Error: {e}")

finally:
    driver.quit()
