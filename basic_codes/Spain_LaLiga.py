import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

def filter_urls_by_year(urls, start_year, end_year):
    filtered_urls = []
    for url in urls:
        # Extract the second-to-last part of the URL and check if it's a valid year
        year_part = url.split('/')[-2]
        if year_part.isdigit():
            year = int(year_part)
            if start_year <= year <= end_year:
                filtered_urls.append(url)
    return filtered_urls


def scrape_laliga(start_year, end_year):
    # Set up Selenium WebDriver
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # Run in headless mode (optional)
    driver = webdriver.Chrome(options=options)

    # File containing all URLs (one per line)
    url_file = "../basic_codes/URLS/urls_SP_LaLiga.txt"

    # Initialize empty lists to store the extracted data
    leagues = []
    dates = []
    home_teams = []
    away_teams = []
    home_scores = []
    away_scores = []

    # Read URLs from the file
    with open(url_file, "r") as file:
        urls = file.readlines()

    # Filter the URLs based on the year range
    filtered_urls = filter_urls_by_year(urls, start_year, end_year)

    # Loop through each URL and scrape the data
    for url in filtered_urls:
        url = url.strip()  # Remove any leading/trailing whitespace
        if not url:
            continue  # Skip empty lines

        # Open the URL
        driver.get(url)
        driver.implicitly_wait(5)  # Wait for the page to load

        # Extract league name (assume it's a global header)
        try:
            league_header = driver.find_element(By.CLASS_NAME, 'swap-text__target')
            league = league_header.text.strip()
        except:
            league = 'Unknown'

        # Get all sections containing headers and matches
        sections = driver.find_elements(By.XPATH, "//div[contains(@class, 'fixres__body')]/..")

        # Loop through each section
        for section in sections:
            date_headers = driver.find_elements(By.XPATH, "//h3[contains(@class, 'fixres__header1')]")
            for i, header in enumerate(date_headers):
                date = driver.execute_script("return arguments[0].textContent;", header).strip() or "Unknown"

                # Find all matches under this section
                match_elements = section.find_elements(By.CLASS_NAME, 'fixres__item')

                for match in match_elements:
                    # Extract teams
                    try:
                        team_elements = match.find_elements(By.CLASS_NAME, 'swap-text__target')
                        home_team = team_elements[0].text if len(team_elements) > 0 else 'Unknown'
                        away_team = team_elements[1].text if len(team_elements) > 1 else 'Unknown'
                    except:
                        home_team, away_team = 'Unknown', 'Unknown'

                    # Extract scores
                    try:
                        score_elements = match.find_elements(By.CLASS_NAME, 'matches__teamscores-side')
                        home_score = score_elements[0].text if len(score_elements) > 0 else 'N/A'
                        away_score = score_elements[1].text if len(score_elements) > 1 else 'N/A'
                    except:
                        home_score, away_score = 'N/A', 'N/A'

                    # Append the data to the lists
                    leagues.append(league)
                    dates.append(date)
                    home_teams.append(home_team)
                    away_teams.append(away_team)
                    home_scores.append(home_score)
                    away_scores.append(away_score)

    # Close the driver after scraping
    driver.quit()

    # Create a DataFrame to organize the data
    data = {
        'League': leagues,
        'Date': dates,
        'Home Team': home_teams,
        'Away Team': away_teams,
        'Home Score': home_scores,
        'Away Score': away_scores
    }
    df = pd.DataFrame(data)

    # Save the results to a CSV file
    output_file = f"{start_year}_{end_year}_SP_laliga.csv"
    df.to_csv(output_file, index=False)

    print(f"Data scraping complete. Results saved to {output_file}")


if __name__ == "__main__":
    # Check if the script is called with command-line arguments
    if len(sys.argv) != 3:
        print("Usage: python Spain_LaLiga.py <start_year> <end_year>")
        sys.exit(1)

    # Parse the years from the command-line arguments
    start_year = int(sys.argv[1])
    end_year = int(sys.argv[2])

    # Call the function to scrape the data
    scrape_laliga(start_year, end_year)
    scrape_laliga(2024, 2025)