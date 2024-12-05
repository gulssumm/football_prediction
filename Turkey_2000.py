import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# File containing URLs with placeholders for ID and {i}
input_file = "urls1.txt"
# Output CSV file
csv_file = "output_data2.csv"

# Initialize the Selenium WebDriver
driver = webdriver.Chrome()  # Ensure ChromeDriver is installed and in PATH

# Open the CSV file in write mode
with open(csv_file, mode="w", newline="", encoding="utf-8-sig") as file:
    writer = csv.writer(file)
    # Write the header row
    writer.writerow(["League Name", "Date", "Home Team", "Home Score", "Away Score", "Away Team"])

    # Read the URL templates from the text file
    with open(input_file, mode="r", encoding="utf-8") as url_file:
        urls = [line.strip() for line in url_file.readlines()]  # Read and strip lines

    # Loop through each URL template
    for url_template in urls:
        for i in range(1, 36):  # Replace {i} with values from 1 to 35
            url = url_template.replace("{i}", str(i))  # Replace {i} with the current value
            print(f"Processing URL: {url}")
            driver.get(url)  # Open the URL in the browser

            # Wait for the page to load
            time.sleep(5)

            try:
                # Find the league name
                league_element = driver.find_element(By.XPATH, "/html/body/form/div[4]/div/section[2]/article[2]/div[1]/b/i/a")
                league_name = league_element.text.strip()

                # Find all home team elements
                home_teams = driver.find_elements(By.XPATH, "//td[@class='haftaninMaclariEv']/a/span")
                home_team_names = [team.text.strip() for team in home_teams]

                # Find the date elements
                dates = driver.find_elements(By.XPATH, "//td[@class='haftaninMaclariTarih']")
                match_dates = [date.text.strip() for date in dates]

                # Find the score elements
                scores = driver.find_elements(By.XPATH, "//td[@class='haftaninMaclariSkor']")
                score_results = [score.text.strip() for score in scores]

                # Find the away team elements
                away_teams = driver.find_elements(By.XPATH, "//td[@class='haftaninMaclariDeplasman']/a/span")
                away_team_names = [away_team.text.strip() for away_team in away_teams]

                # Ensure each home team aligns with its respective date
                for home_team, match_date, score_1, away_team in zip(home_team_names, match_dates, score_results, away_team_names):
                    # Split score into home_score and away_score
                    try:
                        home_score, away_score = map(int, score_1.split('-'))  # Convert both parts to integers
                    except ValueError:
                        # If score is not in "x-y" format, skip this entry
                        print(f"Skipping invalid score: {score_1}")
                        continue

                    # Write data to the CSV
                    writer.writerow([league_name, match_date, home_team, home_score, away_score, away_team])

            except Exception as e:
                print(f"Error processing URL {url}: {e}")

# Close the browser
driver.quit()

print(f"Data has been saved to {csv_file}")
