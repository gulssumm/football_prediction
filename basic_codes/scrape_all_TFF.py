from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

# Set up Selenium WebDriver
options = webdriver.ChromeOptions()
# options.add_argument("--headless")  # Uncomment to run in headless mode
driver = webdriver.Chrome(options=options)


def generate_urls(base_url, start_week, end_week):
    """Generate URLs for a range of weeks."""
    urls = []
    for i in range(start_week, end_week + 1):
        urls.append(base_url.replace("{i}", str(i)))
    return urls


def filter_urls_by_year(urls, initial_year, end_year):
    filtered_urls = []

    for url in urls:
        url = url.strip()  # Clean up the URL

        try:
            # Extract year range from URL and derive actual years (adjust this logic for your URL structure)
            year_part = url.split("?pageID=")[1].split("&")[0]
            year_range = int(year_part)

            # Example mapping logic: Adjust to match your specific format
            start_year = 1950 + (year_range - 500)
            end_year_actual = start_year + 1

            # Check if the year range falls within the desired range
            if initial_year <= start_year <= end_year or initial_year <= end_year_actual <= end_year:
                filtered_urls.append(url)
        except (IndexError, ValueError):
            print(f"Skipping URL with invalid format: {url}")

    print(f"Filtered URLs: {filtered_urls}")
    return filtered_urls


def scrape_TFF(base_url, league_name, initial_year, end_year, start_week, end_week):
    try:
        # Generate URLs dynamically
        urls = generate_urls(base_url, start_week, end_week)

        # Filter URLs based on the year range
        filtered_urls = filter_urls_by_year(urls, initial_year, end_year)

        all_matches = []

        # Loop through each filtered URL
        for url in filtered_urls:
            print(f"Processing URL: {url}")
            driver.get(url)  # Open the URL in the browser
            time.sleep(5)  # Wait for the page to load

            try:
                # Scrape the page
                league_element = driver.find_element(By.XPATH,
                                                     "/html/body/form/div[4]/div/section[2]/article[2]/div[1]/b/i/a")
                league_name = league_element.text.strip()

                home_teams = driver.find_elements(By.XPATH, "//td[@class='haftaninMaclariEv']/a/span")
                dates = driver.find_elements(By.XPATH, "//td[@class='haftaninMaclariTarih']")
                scores = driver.find_elements(By.XPATH, "//td[@class='haftaninMaclariSkor']")
                away_teams = driver.find_elements(By.XPATH, "//td[@class='haftaninMaclariDeplasman']/a/span")

                home_team_names = [team.text.strip() for team in home_teams]
                match_dates = [date.text.strip() for date in dates]
                score_results = [score.text.strip() for score in scores]
                away_team_names = [team.text.strip() for team in away_teams]

                # Collect match data
                for home_team, match_date, score, away_team in zip(home_team_names, match_dates, score_results,
                                                                   away_team_names):
                    try:
                        home_score, away_score = map(int, score.split('-'))
                        all_matches.append({
                            "League": league_name,
                            "Date": match_date,
                            "Home Team": home_team,
                            "Away Team": away_team,
                            "Home Score": home_score,
                            "Away Score": away_score,
                        })
                    except ValueError:
                        print(f"Skipping invalid score: {score}")

            except Exception as e:
                print(f"Error scraping data from {url}: {e}")

        # Save all matches to CSV
        df = pd.DataFrame(all_matches)
        output_file = f"{initial_year}_{end_year}_{league_name.replace(' ', '_')}.csv"
        df.to_csv(output_file, index=False)
        print(f"Data scraping complete. Results saved to {output_file}")

    except Exception as e:
        print(f"Error processing file {base_url}: {e}")


# Usage example
scrape_TFF(
    base_url="https://www.tff.org/Default.aspx?pageID=552&hafta={i}#grp",
    league_name="Trendyol Süper Lig",
    initial_year=2001,
    end_year=2002,
    start_week=1,
    end_week=34
)
