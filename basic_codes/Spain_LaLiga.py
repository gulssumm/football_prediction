from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd


def filter_urls_by_year(urls, start_year, end_year):
    filtered_urls = []
    for url in urls:
        # Extract the "YYYY-YY" part from the URL (the second-to-last part of the URL)
        year_part = url.split("/")[-1]  # Assuming the "YYYY-YY" part is the second-to-last element in the URL

        if year_part:  # Check if the year part is non-empty
            print(f"Processing URL: {url}")  # Debug output to track the URL being processed

            try:
                # Extract the first and second year from the "YYYY-YY" part
                first_year = int(year_part.split("-")[0])  # Get the first year (YYYY)
                second_year = int(year_part.split("-")[1])  # Get the second year (YY)
                full_second_year = 2000 + second_year  # Convert YY to full year (20YY)

                # Check if the years are within the specified range
                if start_year <= first_year <= end_year or start_year <= full_second_year <= end_year:
                    filtered_urls.append(url)  # Add the URL to the list if it's within the range
            except ValueError:
                print(f"Skipping invalid URL: {url}")  # Debug invalid URLs
                continue  # Skip URLs with invalid format

    print(f"Filtered URLs: {filtered_urls}")
    return filtered_urls


def scrape_laliga(start_year, end_year):
    # Set up Selenium WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode
    driver = webdriver.Chrome(options=options)

    # File containing all URLs (one per line)
    url_file = "../basic_codes/URLS/urls_SP_LaLiga.txt"

    # Initialize empty lists to store the extracted data
    leagues, dates, home_teams, away_teams, home_scores, away_scores = [], [], [], [], [], []

    # Read URLs from the file
    with open(url_file, "r") as file:
        urls = file.readlines()

    # Filter the URLs based on the year range
    filtered_urls = filter_urls_by_year(urls, start_year, end_year)

    for url in filtered_urls:
        url = url.strip()
        print(f"Scraping URL: {url}")

        try:
            driver.get(url)
            driver.implicitly_wait(5)

            # Extract matches
            matches = driver.find_elements(By.CLASS_NAME, "fixres__item")
            for match in matches:
                try:
                    league = "La Liga"
                    date = driver.find_element(By.CLASS_NAME, "fixres__header1").text.strip()
                    teams = match.find_elements(By.CLASS_NAME, "swap-text__target")
                    scores = match.find_elements(By.CLASS_NAME, "matches__teamscores-side")

                    home_team = teams[0].text.strip() if len(teams) > 0 else "Unknown"
                    away_team = teams[1].text.strip() if len(teams) > 1 else "Unknown"
                    home_score = scores[0].text.strip() if len(scores) > 0 else "N/A"
                    away_score = scores[1].text.strip() if len(scores) > 1 else "N/A"

                    # Append data
                    leagues.append(league)
                    dates.append(date)
                    home_teams.append(home_team)
                    away_teams.append(away_team)
                    home_scores.append(home_score)
                    away_scores.append(away_score)
                except Exception as e:
                    print(f"Error parsing match: {e}")
        except Exception as e:
            print(f"Error loading URL {url}: {e}")

    driver.quit()

    # Save results to CSV
    data = {
        "League": leagues,
        "Date": dates,
        "Home Team": home_teams,
        "Away Team": away_teams,
        "Home Score": home_scores,
        "Away Score": away_scores,
    }
    df = pd.DataFrame(data)
    output_file = f"{start_year}_{end_year}_SP_laliga.csv"
    df.to_csv(output_file, index=False)
    print(f"Data scraping complete. Results saved to {output_file}")

# Run the function
scrape_laliga(2024, 2025)