import csv

# List of CSV file names to merge
file_names = [
    '../ENGLAND/2000_24_EN_ChampionshipLeague.csv',
    '../ENGLAND/2000_24_EN_LeagueOne.csv',
    '../ENGLAND/2000_24_EN_PremierLeague.csv',
    '../FRANCE/2000_24_FR_Ligue1.csv',
    '../GERMAN/2000_24_GER_Bundesliga.csv',
    '../ITALY/2000_24_IT_serieA.csv',
    '../SPAIN/2000_24_SP_laliga.csv',
    '../TURKEY/2000_22_TR_birincilig.csv',
    '../TURKEY/2000_24_TR_superlig.csv'
]

# Output file name
output_file = 'merged_data.csv'

# Merge CSV files
with open(output_file, 'w', newline='', encoding='utf-8-sig') as outfile:
    writer = csv.writer(outfile)
    is_first_file = True  # Flag to check if it's the first file

    for filename in file_names:
        try:
            with open(filename, 'r', encoding='utf-8-sig') as infile:
                reader = csv.reader(infile)
                # Write header only for the first file
                if is_first_file:
                    writer.writerow(next(reader))  # Write the header row
                    is_first_file = False
                else:
                    next(reader)  # Skip the header row for subsequent files

                # Write the remaining rows
                for row in reader:
                    writer.writerow(row)
        except UnicodeDecodeError:
            print(f"Error decoding file: {filename}. Check the file encoding.")
