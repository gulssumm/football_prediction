from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

# Initialize WebDriver
driver = webdriver.Chrome()
url = "https://www.transfermarkt.com/laliga/gesamtspielplan/wettbewerb/ES1/saison_id/2000"
driver.get(url)

try:
    # Wait for the table to load
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//table[@class='large-12 columns']"))
    )
    print("Table found!")

    # Scroll to ensure full table loading
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)  # Allow time for additional rows to load

    # Find table rows
    rows = driver.find_elements(By.XPATH, "//table[@class='large-12 columns']//tr")
    print(f"Number of rows found: {len(rows)}")

    # Open CSV to save data
    csv_file = "laliga_2000_debug.csv"
    with open(csv_file, mode="w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Time", "Home Team", "Home Score", "Away Score", "Away Team"])

        for row in rows:
            try:
                # Extract data from columns
                match_date = row.find_element(By.XPATH, "./td[1]").text.strip()
                match_time = row.find_element(By.XPATH, "./td[2]").text.strip()
                home_team = row.find_element(By.XPATH, "./td[3]//a").text.strip()
                score = row.find_element(By.XPATH, "./td[4]").text.strip()
                away_team = row.find_element(By.XPATH, "./td[5]//a").text.strip()

                # Split scores
                home_score, away_score = score.split(":") if ":" in score else ("", "")

                # Write to CSV
                writer.writerow([match_date, match_time, home_team, home_score.strip(), away_score.strip(), away_team])
            except Exception as e:
                print(f"Error processing row: {e}")

except Exception as e:
    print(f"Error waiting for table rows: {e}")

# Close the browser
driver.quit()
