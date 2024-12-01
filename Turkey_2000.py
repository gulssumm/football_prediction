import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Initialize the Selenium WebDriver
driver = webdriver.Chrome()  # Ensure ChromeDriver is installed and in PATH

# Name of the CSV file to create
csv_file = "2000_3_home_teams.csv"

# Open the CSV file in write mode (this will create the file if it doesn't exist)
with open(csv_file, mode="w", newline="", encoding="utf-8-sig") as file:
    writer = csv.writer(file)
    writer.writerow(["League Name", "Date", "Home Team", "Home Score", "Away Score", "Away Team"])  # Updated header row

    # Loop through all weeks (1 to 34)
    for j in range(2, -1, -1):
        for i in range(1, 35):
            url = f'https://www.tff.org/Default.aspx?pageID=55{j}&hafta={i}#grp'
            driver.get(url)

            # Wait for the page to load
            time.sleep(5)

            try:
                # Find the league name
                league_element = driver.find_element(By.XPATH,"/html/body/form/div[4]/div/section[2]/article[2]/div[1]/b/i/a")
                league_name = league_element.text.strip()

                # Find all home team elements
                home_teams = driver.find_elements(By.XPATH, "//td[@class='haftaninMaclariEv']/a/span")
                home_team_names = [team.text.strip() for team in home_teams]

                # Find the date elements
                dates = driver.find_elements(By.XPATH, "//td[@class='haftaninMaclariTarih']")
                match_dates = [date.text.strip() for date in dates]  # List of match dates

                # Find the score elements
                scores = driver.find_elements(By.XPATH, "//td[@class='haftaninMaclariSkor']")
                score_results = [score.text.strip() for score in scores]  # List of scores

                # Find the away team elements
                away_teams = driver.find_elements(By.XPATH, "//td[@class='haftaninMaclariDeplasman']/a/span")
                away_team_names = [away_team.text.strip() for away_team in away_teams]  # List of away teams

                # Ensure each home team aligns with its respective date
                for home_team, match_date, score_1, away_team in zip(home_team_names, match_dates, score_results,
                                                                     away_team_names):
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
                print(f"Error on week {i}: {e}")

# Close the browser
driver.quit()

print(f"Data has been saved to {csv_file}")
