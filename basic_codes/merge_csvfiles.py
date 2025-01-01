import csv
import chardet

# List of CSV file names to merge
file_names = [
    '../ENGLAND/2000_24_EN_ChampionshipLeague.csv',
    '../ENGLAND/2000_24_EN_LeagueOne.csv',
    '../ENGLAND/2000_24_EN_PremierLeague.csv',
    '../FRANCE/2000_24_FR_Ligue1.csv',
    '../GERMAN/2000_24_GER_Bundesliga.csv',
    '../ITALY/2000_24_IT_serieA.csv',
    '../SPAIN/2000_24_SP_laliga.csv',
    '../TURKEY/2000_24_TR_birincilig.csv',
    '../TURKEY/2000_24_TR_superlig.csv'
]

# Output file name
output_file = 'merged_data.csv'

# Merge CSV files
with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
    writer = csv.writer(outfile)
    for filename in file_names:
        try:
            with open(filename, 'r', encoding='utf-8') as infile:  # Explicitly specify UTF-8 encoding
                reader = csv.reader(infile)
                for row in reader:
                    writer.writerow(row)
        except UnicodeDecodeError:
            print(f"Error decoding file: {filename}. Check the file encoding.")



"""file_name = '../ENGLAND/2000_24_EN_ChampionshipLeague.csv'
with open(file_name, 'utf-8') as f:
    raw_data = f.read()
    result = chardet.detect(raw_data)
    print(result['encoding'])"""
