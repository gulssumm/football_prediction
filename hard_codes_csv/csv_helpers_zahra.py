from bs4 import BeautifulSoup
import requests
import re
import datetime
from datetime import datetime
import openmeteo_requests
import requests_cache
import pandas as pd
import math
from retry_requests import retry

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

def get_match_data(url):
    if '.com.tr' in url:
        url = url.replace('.com.tr', '.com')
    if 'transfermarkt.com' not in url:
        return {
            "home_link": "NA",
            "away_link": "NA",
            "home_player_links": "NA",
            "away_player_links": "NA",
            "statistics": "NA",
            "time": "NA"
        }

    html_content = requests.get(url, headers=headers).text
    # driver.get(url)
    # driver.implicitly_wait(1)
    # html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')

    href_values = [a['href'] for a in soup.select('.sb-zusatzinfos a')]
    stadium_link = 'https://www.transfermarkt.com' + href_values[0]
    
    team_elements = soup.select('.sb-vereinslink')
    team_links = [link.get('href') for link in team_elements]
    
    player_links = soup.select('.aufstellung-rueckennummer-name a')
    first_11_links = []
    second_11_links = []
    for index, player_link in enumerate(player_links):
        href = player_link.get('href')
        the_link = 'https://www.transfermarkt.com' + href
        if index < 11:
            first_11_links.append(the_link)
        else:
            second_11_links.append(the_link)

    converted_url = url.replace("/index/spielbericht/", "/statistik/spielbericht/")
    statistics = get_statistics(converted_url)

    time = get_time(converted_url)

    match_data_dictionary = {
        "home_link": 'https://www.transfermarkt.com' + team_links[0],
        "away_link": 'https://www.transfermarkt.com' + team_links[1],
        "home_player_links": first_11_links,
        "away_player_links": second_11_links,
        "statistics": statistics,
        "time": time,
        "stadium_link": stadium_link
    }
    
    # driver.quit()
    return match_data_dictionary

def get_time(url):
    response = requests.get(url, headers = headers)
    page = response.text
    soup = BeautifulSoup(page, 'html.parser')

    date_elements = soup.select('.sb-datum.hide-for-small')
    date_values = [element.get_text(strip=True) for element in date_elements]
    date_array = date_values[0].split(' ')[2].split('|')[0].split('.')[0].split('/')
    time_array = date_values[0].split('|')[2].strip().split(' ')
    time_array_hour = int(time_array[0].split(':')[0])
    time_array_minute = int(time_array[0].split(':')[1])
    if(time_array[1] == 'PM' and time_array_hour != 12):
        time_array_hour += 12
    return {
        'month:': int(date_array[0]),
        'day:': int(date_array[1]),
        'year:': int(date_array[2]) + 2000,
        'hour:': time_array_hour + 2,
        'minute:': time_array_minute,
    }

def get_player_data(url):
    if '.com.tr' in url:
        url = url.replace('.com.tr', '.com')
    if 'transfermarkt.com' not in url:
        return {
            "home_link": "NA",
            "away_link": "NA",
            "home_player_links": "NA",
            "away_player_links": "NA",
            "statistics": "NA",
            "time": "NA"
        }
    
    trophies_url = url.replace("/profil/", "/erfolge/")
    stats_url = url.replace('/profil/', '/leistungsdaten/').replace('/spieler/', '/spieler/') + '/plus/0?saison=ges'
    player_id = url.split("/")[-1]
    
    response = requests.get(url, headers = headers)
    page = response.text
    soup = BeautifulSoup(page, 'html.parser')

    player_position_elements = soup.select('.data-header__content')
    player_position_values= [element.get_text(strip=True) for element in player_position_elements]
    
    if player_position_values[6][-1] != 'm':
        if(player_position_values[6] == 'Goalkeeper'):
            player_stats_array = get_goalkeeper_stats(stats_url)
    
        else:
            player_stats_array = get_player_stats(stats_url)            
    else:
        if(player_position_values[7] == 'Goalkeeper'):
            player_stats_array = get_goalkeeper_stats(stats_url) 
        else:
            player_stats_array = get_player_stats(stats_url)            
    
    player_value_elements = soup.select('.data-header__market-value-wrapper')
    if player_value_elements:
        player_value_values= [element.get_text(strip=True) for element in player_value_elements]
        player_value_temp = player_value_values[0][:12]
        index_of_L = player_value_temp.find('L')
        player_value_temp = player_value_temp[:index_of_L]
        player_value_temp = player_value_temp[1:]
        if 'm' in player_value_temp:
            value = float(player_value_temp.replace('m', '')) * 1e6
            player_value = int(value)
        else:
            value = float(player_value_temp.replace('k', '')) * 1e3
            player_value = int(value)
    else:
        player_value = 0

    player_age_elements = soup.select('.data-header__content')
    player_age_values= [element.get_text(strip=True) for element in player_age_elements]
    player_age_date = player_age_values[3]
    player_age_string = player_age_date[-3] + player_age_date[-2]
    try:
        player_age = int(player_age_string)
    except ValueError:
        player_age = "NA"
    
    player_trophies = get_player_trophies(trophies_url)
    player_seasonal_stats = get_player_seasonal(player_id)

    if(player_stats_array[0] == '-'):
        player_appearances = 0
    else:
        player_appearances = int(player_stats_array[0])

    if(player_stats_array[1] == '-'):
        player_goals = 0
    else:
        player_goals = int(player_stats_array[1])

    if(player_stats_array[2] == '-'):
        player_assists = 0
    else:
        player_assists = int(player_stats_array[2])

    if(player_stats_array[3] == '-'):
        player_yellow_cards = 0
    else:
        player_yellow_cards = int(player_stats_array[3])
    
    if(player_stats_array[4] == '-'):
        player_red_cards = 0
    else:
        player_red_cards = int(player_stats_array[4])

    temp_array = [player_appearances, player_goals, player_assists, player_yellow_cards, player_red_cards]
    updated_player_stats_array = [0 if data == "-" else data for data in temp_array]

    player_data_dictionary = {
    "value": player_value,
    "age": player_age,
    "total_trophies": player_trophies,
    "total_appearances": updated_player_stats_array[0],
    "total_goals": updated_player_stats_array[1],
    "total_assists": updated_player_stats_array[2],
    "total_yellow_cards": updated_player_stats_array[3],
    "total_red_cards": updated_player_stats_array[4],
    "season_appearances": player_seasonal_stats["season_appearances"],
    "season_goals": player_seasonal_stats["season_goals"],
    "season_assists": player_seasonal_stats["season_assists"],
    "season_yellow_cards": player_seasonal_stats["season_yellow_cards"],
    "season_red_cards": player_seasonal_stats["season_red_cards"]
    }

    return player_data_dictionary

def get_player_seasonal(player_id = 342229, year = 2023):
    url = f"https://transfermarkt-api.vercel.app/players/{player_id}/stats"
    year_str = str(year)
    response = requests.get(url)

    if(len(year_str) == 4):    
        year_str = year_str[-2:] + '/' + str(int(year_str[-2:]) + 1)
    else:
        season_appearances, season_goals, season_assists, season_yellow_cards, season_red_cards = 0, 0, 0, 0, 0

        get_player_seasonal_dictionary = {
        "season_appearances": season_appearances,
        "season_goals": season_goals,
        "season_assists": season_assists,
        "season_yellow_cards": season_yellow_cards,
        "season_red_cards": season_red_cards
        } 

        return get_player_seasonal_dictionary
        
    if response.status_code == 200:
        all_data = response.json()
        all_stats = all_data.get("stats", [])
        tr1_stats = [season for season in all_stats if season.get("competitionID") == "TR1"]
        season_appearances, season_goals, season_assists, season_yellow_cards, season_red_cards = 0, 0, 0, 0, 0

        for season in tr1_stats:
            if season.get("seasonID") == year_str:
                season_appearances = season.get("appearances", 0)
                season_goals = season.get("goals", 0)
                season_assists = season.get("assists", 0)
                season_yellow_cards = season.get("yellowCards", 0)
                season_red_cards = season.get("redCards", 0)
                break
        
        get_player_seasonal_dictionary = {
            "season_appearances": season_appearances,
            "season_goals": season_goals,
            "season_assists": season_assists,
            "season_yellow_cards": season_yellow_cards,
            "season_red_cards": season_red_cards
        } 
        
        return get_player_seasonal_dictionary
    else:
        season_appearances, season_goals, season_assists, season_yellow_cards, season_red_cards = 'NA', 'NA', 'NA', 'NA', 'NA'

        get_player_seasonal_dictionary = {
            "season_appearances": season_appearances,
            "season_goals": season_goals,
            "season_assists": season_assists,
            "season_yellow_cards": season_yellow_cards,
            "season_red_cards": season_red_cards
        }

        return get_player_seasonal_dictionary

def get_player_trophies(trophies_url):
    response = requests.get(trophies_url, headers = headers)
    page = response.text
    soup = BeautifulSoup(page, 'html.parser')

    trophy_elements = soup.select('.content-box-headline')
    trophy_values = [element.get_text(strip=True) for element in trophy_elements]
    trophies = sum(int(re.search(r'\d+', item).group()) for item in trophy_values if re.search(r'\d+', item))

    return trophies

def get_player_stats(stats_link):
    response = requests.get(stats_link, headers = headers)
    page = response.text
    soup = BeautifulSoup(page, 'html.parser')
    
    stats_elements = soup.select('.zentriert')
    stats_values = [element.get_text(strip=True) for element in stats_elements]
    stats_array = [stats_values[6], stats_values[7], stats_values[8], stats_values[9], stats_values[11]]

    return stats_array

def get_goalkeeper_stats(stats_link):
    response = requests.get(stats_link, headers=headers)
    page = response.text
    soup = BeautifulSoup(page, 'html.parser')
    
    stats_elements = soup.select('.zentriert')
    stats_values = [element.get_text(strip=True) for element in stats_elements]
    stats_array = [stats_values[7], stats_values[8], 0, stats_values[9], stats_values[11]]

    return stats_array

def get_match_links(yil):
    
    current_year = datetime.now().year
    target_year = current_year - yil
    
    # Hedef yıla göre URL oluşturma
    initial_url = f'https://www.transfermarkt.com/super-lig/gesamtspielplan/wettbewerb/TR1?saison_id={target_year}'

    # driver.get(initial_url)
    # wait = WebDriverWait(driver, 7)
    # wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'large-12')))

    data = requests.get(initial_url, headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')
    match_links = []
    base_url = 'https://www.transfermarkt.com'
    link_final = []

    for link in soup.find_all('a', class_='ergebnis-link'):
        match_links.append(base_url + link.get('href'))
    for match_link in match_links:
        zamb = match_link.split('/')
        zamb[3] = "spielbericht"
        link__finall = '/'.join(zamb)
        link_final.append(link__finall)

    link_final.reverse()  # Listeyi ters çevir
    son_mac = link_final[0] if link_final else None  # listenin son elemanı, eğer liste doluysa

    match_dictionary = {
        'link_array': link_final,
        'last_match': son_mac if son_mac else "son mac yok :)"
    }
    # print('initial url bu ' +initial_url)
    return match_dictionary

def cont(linik, sayi):
    i = 1
    found = False
    while not found:
        link_array = get_match_links(i)['link_array']
        if linik in link_array:
            found = True
            konum = link_array.index(linik)
            if konum >= sayi:
                return link_array[konum - sayi : konum]
            else:
                return link_array[:konum]
        i += 1
    return []

def get_statistics(converted_url):
    # TODO statistic sayfasi olmayan maclara gelince patliyor
    page = requests.get(converted_url, headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')

    score_elements = soup.select('.sb-endstand')
    score_values = [element.get_text(strip=True) for element in score_elements]
    score_values_split = [score_values[0][:1], score_values[0][2], score_values[0][2:]]

    statistics_elements = soup.select('.sb-statistik-zahl')
    statistics_values = [element.get_text(strip=True) for element in statistics_elements]

    position_elements1 = soup.select('.sb-team.sb-heim')
    position_elements2 = soup.select('.sb-team.sb-gast')
    position_value1 = [element.get_text(strip=True) for element in position_elements1]
    position_value2 = [element.get_text(strip=True) for element in position_elements2]
    homeposition1 = position_value1[0][-2:]
    homeposition2 = position_value2[0][-2:]
    if homeposition1[0] == ' ':
        homeposition1 = homeposition1[1:]
    if homeposition2[0] == ' ':
        homeposition2 = homeposition2[1:]

    score1 = int(score_values_split[0])
    score2 = int(score_values_split[1])
    statistics1 = int(statistics_values[0])
    statistics2 = int(statistics_values[1])
    statistics3 = int(statistics_values[2])
    statistics4 = int(statistics_values[3])
    statistics5 = int(statistics_values[4])
    statistics6 = int(statistics_values[5])
    statistics7 = int(statistics_values[6])
    statistics8 = int(statistics_values[7])
    statistics9 = int(statistics_values[8])
    statistics10 = int(statistics_values[9])
    statistics11 = int(statistics_values[10])
    statistics12 = int(statistics_values[11])
    statistics13 = int(statistics_values[12])
    statistics14 = int(statistics_values[13])
    homeposition11 = int(homeposition1)
    homeposition22 = int(homeposition2)

    statistic_dictionary = {
        "home_score": score1,
        "away_score": score2,
        "home_total_shots": statistics1,
        "away_total_shots": statistics2,
        "home_shots_off_target": statistics3,
        "away_shots_off_target": statistics4,
        "home_shots_saved": statistics5,
        "away_shots_saved": statistics6,
        "home_corners": statistics7,
        "away_corners": statistics8,
        "home_free_kicks": statistics9,
        "away_free_kicks": statistics10,
        "home_fouls": statistics11,
        "away_fouls": statistics12,
        "home_offsides": statistics13,
        "away_offsides": statistics14,
        "home_position": homeposition11,
        "away_position": homeposition22,           
    }

    return statistic_dictionary

def get_team_data(team_url):
    if '.com.tr' in team_url:
        team_url = team_url.replace('.com.tr', '.com')

    if 'transfermarkt.com' not in team_url:
        return {
            'team_value': "NA",
            'avarage_age': "NA",
            'national_players': "NA",
            'stadium_seat': "NA",
            'squad_size': "NA",
            'team_trophies' : "NA"
        }
    
    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    # }

    team_page = requests.get(team_url, headers=headers)

    team_soup = BeautifulSoup(team_page.content, 'html.parser')

    try:
        team_value = team_soup.find("div", class_="data-header__box--small").text.strip()
        # Son "m" harfine sahip olan kısmı bulmak için regular expression kullanıyoruz
        #print(team_value)
        son_kismi = team_value.split(' ')[0][-1:]
        nnteamvalue = team_value.split(' ')[0][1:-1]
        final_team_value = float(nnteamvalue)
        if son_kismi == "m":
            final_team_value = final_team_value * 1000000
        if son_kismi == "k":
            final_team_value = final_team_value * 1000
    except AttributeError:
        final_team_value = "NA"
        team_value = "NA"
    # Yaş ortalaması, milli takımdaki oyuncu sayısı, stadyum ve kadro boyutu
    labels = team_soup.find_all(class_="data-header__label")
    for label in labels:
        label_name = label.text.strip()
        if label_name.startswith("Average age"):
            average_aged = label.find_next(class_="data-header__content").text.strip()
            average_age = float(average_aged)
        elif label_name.startswith("National team players"):
            national_playersd = label.find_next(class_="data-header__content").text.strip().split()[0]
            national_players = int(national_playersd)
        elif label_name.startswith("Stadium"):
            stadium_info = label.find_next(class_="data-header__content").text.strip()
            stadium_seat = ''
            if 'seat' in stadium_info.lower():
                seat_index = stadium_info.lower().find('seat')
                stadium_seatd = stadium_info[:seat_index].strip().split()[-1]
                stadium_seat =float(stadium_seatd)*1000

        elif label_name.startswith("Squad size"):
            squad_sized = label.find_next(class_="data-header__content").text.strip()
            squad_size = int(squad_sized)
    
    def get_team_trophies():

        success_numbers = team_soup.find_all("span", class_="data-header__success-number")

        # Span elementlerinin text içeriğini alarak bir liste oluştur
        numbers_list = [int(success_number.get_text().strip()) for success_number in success_numbers]

        # Sayıları topla
        total = sum(numbers_list)

        return total
            
    trophies = get_team_trophies()

    return {
        'team_value': final_team_value,
        'average_age': average_age,
        'national_players': national_players,
        'stadium_seat': stadium_seat,
        'squad_size': squad_size,
        'team_trophies' : trophies}

def stadium_link(url):
    response = requests.get(url, headers=headers)
    html_content = response.text
    soup = BeautifulSoup(html_content, "html.parser")
    eksik_stadium_link = soup.find("a", href=lambda href: href and "/stadion/" in href)
    # Sonucu yazdır
    if eksik_stadium_link:
        stadium_link = "https://www.transfermarkt.com" + eksik_stadium_link["href"]
        return stadium_link
    else:
        stadium_link = "NA"
        return "NA"
def find_adress(url):
    if(url == "NA"):
        return "NA"
    response = requests.get(url, headers=headers)
    html_content = response.text
    soup = BeautifulSoup(html_content, "html.parser")
    address_elements = soup.select('.profilheader')
    address_values = [element.get_text(strip=True) for element in address_elements]
    metin = address_values[1]
    turkiye_il_listesi = ["Adana", "Adıyaman", "Afyonkarahisar", "Ağrı", "Amasya", "Ankara", "Antalya", "Artvin", "Aydın", "Balıkesir", "Bilecik", "Bingöl", "Bitlis", "Bolu", "Burdur", "Bursa", "Çanakkale", "Çankırı", "Çorum", "Denizli", "Diyarbakır", "Edirne", "Elazığ", "Erzincan","Istanbul", "Erzurum", "Eskişehir", "Gaziantep", "Giresun", "Gümüşhane", "Hakkari", "Hatay", "Isparta", "Mersin", "İstanbul", "İzmir", "Kars", "Kastamonu", "Kayseri", "Kırklareli", "Kırşehir", "Kocaeli", "Konya", "Kütahya", "Malatya", "Manisa", "Kahramanmaraş", "Mardin", "Muğla", "Muş", "Nevşehir", "Niğde", "Ordu", "Rize", "Sakarya", "Samsun", "Siirt", "Sinop", "Sivas", "Tekirdağ", "Tokat", "Trabzon", "Tunceli", "Şanlıurfa", "Uşak", "Van", "Yozgat", "Zonguldak", "Aksaray", "Bayburt", "Karaman", "Kırıkkale", "Batman", "Şırnak", "Bartın", "Ardahan", "Iğdır", "Yalova", "Karabük", "Kilis", "Osmaniye", "Düzce"]
    metin = metin  # Metni küçük harfe çevir
    words = metin.split()
    last_city = "NA"
    
    for word in reversed(words):  # Kelimeleri ters sıradan kontrol et
        for city in turkiye_il_listesi:
            if city in word:
                last_city = city  # Eğer şehir metinde varsa, son şehri güncelle
                break  # İç içe döngüden çık
        if last_city:
            break  # İç içe döngüden çık
    if(last_city =="Istanbul"):
        return "İstanbul"
    return last_city


def flatten_dict(dictionary, parent_key='', sep='_'):
    items = []
    for k, v in dictionary.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

################## TEST ###################

def get_player_data_old(url):
    if '.com.tr' in url:
        url = url.replace('.com.tr', '.com')
    if 'transfermarkt.com' not in url:
        return {
            "home_link": "NA",
            "away_link": "NA",
            "home_player_links": "NA",
            "away_player_links": "NA",
            "statistics": "NA",
            "time": "NA"
        }
    trophies_url = url.replace("/profil/", "/erfolge/")
    stats_url = url.replace('/profil/', '/leistungsdaten/').replace('/spieler/', '/spieler/') + '/plus/0?saison=ges'

    response = requests.get(url, headers = headers)
    page = response.text
    soup = BeautifulSoup(page, 'html.parser')

    player_position_elements = soup.select('.data-header__content')
    player_position_values= [element.get_text(strip=True) for element in player_position_elements]
    
    if player_position_values[6][-1] != 'm':
        if(player_position_values[6] == 'Goalkeeper'):
            player_stats_array = get_goalkeeper_stats(stats_url)
    
        else:
            player_stats_array = get_player_stats(stats_url)            
    else:
        if(player_position_values[7] == 'Goalkeeper'):
            player_stats_array = get_goalkeeper_stats(stats_url) 
        else:
            player_stats_array = get_player_stats(stats_url)            
    
    player_value_elements = soup.select('.data-header__market-value-wrapper')
    if player_value_elements:
        player_value_values= [element.get_text(strip=True) for element in player_value_elements]
        player_value_temp = player_value_values[0][:12]
        index_of_L = player_value_temp.find('L')
        player_value_temp = player_value_temp[:index_of_L]
        player_value_temp = player_value_temp[1:]
        if 'm' in player_value_temp:
            value = float(player_value_temp.replace('m', '')) * 1e6
            player_value = int(value)
        else:
            value = float(player_value_temp.replace('k', '')) * 1e3
            player_value = int(value)
    else:
        player_value = 0

    player_age_elements = soup.select('.data-header__content')
    player_age_values= [element.get_text(strip=True) for element in player_age_elements]
    player_age_date = player_age_values[3]
    player_age_string = player_age_date[-3] + player_age_date[-2]
    try:
        player_age = int(player_age_string)
    except ValueError:
        player_age = "NA"
    
    player_trophies = get_player_trophies(trophies_url)
    
    if(player_stats_array[0] == '-'):
        player_appearances = 0
    else:
        player_appearances = int(player_stats_array[0])

    if(player_stats_array[1] == '-'):
        player_goals = 0
    else:
        player_goals = int(player_stats_array[1])

    if(player_stats_array[2] == '-'):
        player_assists = 0
    else:
        player_assists = int(player_stats_array[2])

    if(player_stats_array[3] == '-'):
        player_yellow_cards = 0
    else:
        player_yellow_cards = int(player_stats_array[3])
    
    if(player_stats_array[4] == '-'):
        player_red_cards = 0
    else:
        player_red_cards = int(player_stats_array[4])

    temp_array = [player_appearances, player_goals, player_assists, player_yellow_cards, player_red_cards]
    updated_player_stats_array = [0 if data == "-" else data for data in temp_array]

    player_data_dictionary = {
        "value": player_value,
        "age": player_age,
        "total_trophies": player_trophies,
        "total_appearances": updated_player_stats_array[0],
        "total_goals": updated_player_stats_array[1],
        "total_assists": updated_player_stats_array[2],
        "total_yellow_cards": updated_player_stats_array[3],
        "total_red_cards": updated_player_stats_array[4],
    }

    return player_data_dictionary

def get_weather_data(date, location):
    if location =="NA":
        return {
        "degree": "NA",
        "wspeed": "NA",
        "condition": "NA"
        }
    year = date['year:']
    day = date['day:']
    month = date['month:']
    hour = date['hour:']
    match_date = f"{year:04d}-{month:02d}-{day:02d}"
    cache_session = requests_cache.CachedSession('.cache', expire_after = -1)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)
    location = location.replace('İ', 'I').replace('ı', 'i').replace('ğ', 'g').replace('Ğ', 'G').replace('ü', 'u').replace('Ü', 'U').replace('ş', 's').replace('Ş', 'S').replace('ö', 'o').replace('Ö', 'O').replace('ç', 'c').replace('Ç', 'C')

    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below

    cities = {'Adana': {'geocode': ('37.0000', '35.3213')}, 'Adiyaman': {'geocode': ('37.7648', '38.2786')}, 'Afyonkarahisar': {'geocode': ('38.7500', '30.5567')}, 'Agri': {'geocode': ('39.7217', '43.0567')}, 'Amasya': {'geocode': ('40.6500', '35.8333')}, 'Ankara': {'geocode': ('39.9199', '32.8543')}, 'Antalya': {'geocode': ('36.8969', '30.7133')}, 'Artvin': {'geocode': ('41.1833', '41.8183')}, 'Aydin': {'geocode': ('37.8444', '27.8458')}, 'Balikesir': {'geocode': ('39.6484', '27.8826')}, 'Bilecik': {'geocode': ('40.1500', '29.9833')}, 'Bingol': {'geocode': ('38.8847', '40.4989')}, 'Bitlis': {'geocode': ('38.3936', '42.1231')}, 'Bolu': {'geocode': ('40.6667', '31.3000')}, 'Burdur': {'geocode': ('37.7203', '30.2906')}, 'Bursa': {'geocode': ('40.1824', '29.0671')}, 'Canakkale': {'geocode': ('40.1553', '26.4142')}, 'Cankiri': {'geocode': ('40.6667', '33.3333')}, 'Corum': {'geocode': ('40.5469', '34.9511')}, 'Denizli': {'geocode': ('37.7760', '29.0864')}, 'Diyarbakir': {'geocode': ('37.9144', '40.2306')}, 'Edirne': {'geocode': ('41.6667', '26.5667')}, 'Elazig': {'geocode': ('38.6750', '39.2200')}, 'Erzincan': {'geocode': ('39.7500', '39.5000')}, 'Erzurum': {'geocode': ('39.9334', '41.2692')}, 'Eskisehir': {'geocode': ('39.7767', '30.5206')}, 'Gaziantep': {'geocode': ('37.0662', '37.3833')}, 'Giresun': {'geocode': ('40.9128', '38.3895')}, 'Gumushane': {'geocode': ('40.4386', '39.5086')}, 'Hakkari': {'geocode': ('37.5744', '43.7408')}, 'Hatay': {'geocode': ('36.3628', '36.2586')}, 'Isparta': {'geocode': ('37.7648', '30.5567')}, 'Mersin': {'geocode': ('36.8000', '34.6333')}, 'Istanbul': {'geocode': ('41.0082', '28.9784')}, 'Izmir': {'geocode': ('38.4192', '27.1287')}, 'Kahramanmaras': {'geocode': ('37.5744', '36.9372')}, 'Karabuk': {'geocode': ('41.0833', '32.6333')}, 'Karaman': {'geocode': ('37.1759', '33.2287')}, 'Kars': {'geocode': ('40.6000', '43.0986')}, 'Kastamonu': {'geocode': ('41.3887', '33.7827')}, 'Kayseri': {'geocode': ('38.7345', '35.4676')}, 'Kirikkale': {'geocode': ('39.8468', '33.5152')}, 'Kirklareli': {'geocode': ('41.7333', '27.2167')}, 'Kirsehir': {'geocode': ('39.1500', '34.1667')}, 'Kocaeli': {'geocode': ('40.7669', '29.9169')}, 'Konya': {'geocode': ('37.8714', '32.4860')}, 'Kutahya': {'geocode': ('39.4167', '29.9833')}, 'Malatya': {'geocode': ('38.3552', '38.3095')}, 'Manisa': {'geocode': ('38.6191', '27.4289')}, 'Kahramanmaras': {'geocode': ('37.5744', '36.9372')}, 'Mardin': {'geocode': ('37.3217', '40.7247')}, 'Mugla': {'geocode': ('37.2153', '28.3636')}, 'Mus': {'geocode': ('38.9462', '41.7539')}, 'Nevsehir': {'geocode': ('38.6936', '34.6851')}, 'Nigde': {'geocode': ('37.9667', '34.6833')}, 'Ordu': {'geocode': ('40.9839', '37.8769')}, 'Rize': {'geocode': ('41.0201', '40.5234')}, 'Sakarya': {'geocode': ('40.7669', '30.4016')}, 'Samsun': {'geocode': ('41.2867', '36.3300')}, 'Siirt': {'geocode': ('37.9278', '41.9450')}, 'Sinop': {'geocode': ('41.7711', '34.8736')}, 'Sivas': {'geocode': ('39.7477', '37.0179')}, 'Tekirdag': {'geocode': ('40.9833', '27.5167')}, 'Tokat': {'geocode': ('40.3167', '36.5500')}, 'Trabzon': {'geocode': ('41.0053', '39.7316')}, 'Tunceli': {'geocode': ('39.1086', '39.5479')}, 'Sanliurfa': {'geocode': ('37.1671', '38.7939')}, 'Usak': {'geocode': ('38.6823', '29.4082')}, 'Van': {'geocode': ('38.4942', '43.3800')}, 'Yozgat': {'geocode': ('39.8200', '34.8147')}, 'Zonguldak': {'geocode': ('41.4564', '31.7987')}, 'Aksaray': {'geocode': ('38.3687', '34.0370')}, 'Bayburt': {'geocode': ('40.2552', '40.2249')}, 'Karaman': {'geocode': ('37.1811', '32.4797')}, 'Kirikkale': {'geocode': ('39.8563', '33.5067')}, 'Batman': {'geocode': ('37.8812', '41.1351')}, 'Sirnak': {'geocode': ('37.5164', '42.4613')}, 'Bartin': {'geocode': ('41.5811', '32.4614')}, 'Ardahan': {'geocode': ('41.1102', '42.7022')}, 'Igdir': {'geocode': ('39.9208', '44.0450')}, 'Yalova': {'geocode': ('40.6500', '29.2500')}, 'Karabuk': {'geocode': ('41.1970', '32.6190')}, 'Kilis': {'geocode': ('36.7161', '37.1164')}, 'Osmaniye': {'geocode': ('37.2130', '36.1767')}, 'Duzce': {'geocode': ('40.8500', '31.1667')}}
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
    	"latitude": float(cities[location]['geocode'][0]),
    	"longitude": float(cities[location]['geocode'][1]),
    	"start_date": match_date,
    	"end_date": match_date,
    	"hourly": ["temperature_2m", "weather_code", "wind_speed_10m"]
    }
    responses = openmeteo.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]

    # Process hourly data. The order of variables needs to be the same as requested.
    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
    hourly_weather_code = hourly.Variables(1).ValuesAsNumpy()
    hourly_wind_speed_10m = hourly.Variables(2).ValuesAsNumpy()

    hourly_data = {"date": pd.date_range(
    	start = pd.to_datetime(hourly.Time(), unit = "s"),
    	end = pd.to_datetime(hourly.TimeEnd(), unit = "s"),
    	freq = pd.Timedelta(seconds = hourly.Interval()),
    	inclusive = "left"
    )}
    hourly_data["temperature_2m"] = hourly_temperature_2m
    hourly_data["weather_code"] = hourly_weather_code
    hourly_data["wind_speed_10m"] = hourly_wind_speed_10m

    hourly_dataframe = pd.DataFrame(data=hourly_data)
    target_hour = hour

    # Saate göre filtreleme
    target_hour_data = hourly_dataframe[hourly_dataframe['date'].dt.hour == target_hour]

    def get_weather_description(weather_code):
        if math.isnan(weather_code):
            return "NA"

        weather_code = int(weather_code)

        weather_dict = {
            (0, 1): "Clear sky",
            (2, 3): "Mainly clear partly cloudy and overcast",
            (45, 48): "Fog and depositing rime fog",
            (51, 53, 55): "Drizzle: Light moderate and dense intensity",
            (56, 57): "Freezing Drizzle: Light and dense intensity",
            (61, 63, 65): "Rain: Slight moderate and heavy intensity",
            (66, 67): "Freezing Rain: Light and heavy intensity",
            (71, 73, 75): "Snow fall: Slight moderate and heavy intensity",
            77: "Snow grains",
            (80, 81, 82): "Rain showers: Slight moderate and violent",
            (85, 86): "Snow showers slight and heavy",
            (95,): "Thunderstorm: Slight or moderate",
            (96, 99): "Thunderstorm with slight and heavy hail"
        }

        for key, description in weather_dict.items():
            if weather_code in key or (isinstance(weather_code, int) and weather_code == key):
                return description

        return "Unknown"

    # Kullanım örneği 
    weather_code = target_hour_data["weather_code"].values[0]  # Float olarak gelen değeri integer'a çeviriyoruz
    condition = get_weather_description(weather_code)

    condition = get_weather_description(target_hour_data["weather_code"].values[0])

    # Sütun isimleri üzerinden veriye erişim
    weather_dictionary = {
        "degree": float(target_hour_data["temperature_2m"].values[0]),
        "wspeed": float(target_hour_data["wind_speed_10m"].values[0]),
        "condition": condition
    }
    return weather_dictionary

# print(get_weather_data({'year:': 2020, 'month:': 5, 'day:': 5, 'hour:': 14} , "Istanbul"))