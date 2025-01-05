# Define the base URL and years
base_url = "https://www.skysports.com/la-liga-results/"
start_year = 2000
end_year = 2024

# Open the text file in write mode
with open("urls_SP_LaLiga.txt", "w") as file:
    # Generate URLs for each year and write to the file
    for year in range(start_year, end_year + 1):
        season = f"{year}-{str(year + 1)[-2:]}"  # Format the season, e.g., "2000-01"
        url = base_url + season
        file.write(url + "\n")  # Write each URL on a new line

print("URLs have been written to urls_SP_LaLiga.txt")
