import csv

# List of CSV file names to merge
file_names = ['2000_24_EN_ChampionshipLeague.csv',
              '2000_24_EN_LeagueOne.csv', '2000_24_EN_PremierLeague.csv',
              '2000_24_FR_Ligue1.csv', '2000_24_GER_Bundesliga.csv',
              '2000_24_IT_serieA.csv', '2000_24_SP_laliga.csv',
              '2000_24_TR_birincilig.csv', '2000_24_TR_superlig.csv']

# Output file name
output_file = 'merged_data.csv'

# Merge CSV files
with open(output_file, 'w', newline='') as outfile:
    writer = csv.writer(outfile)
    for filename in file_names:
        with open(filename, 'r') as infile:
            reader = csv.reader(infile)
            for row in reader:
                writer.writerow(row)