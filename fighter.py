from bs4 import BeautifulSoup
import requests
import json


url = 'https://www.fightmatrix.com/fighter-profile/Ciryl+Gane/193933/'

fighter_html = requests.get(url).text
soup = BeautifulSoup(fighter_html, 'lxml')

content = soup.find('div', id="content")

fighter_name = content.find('div', class_ = 'posttitle').text

info_table = content.find('table', class_="tblRank")

info_chart = info_table.find_all('div')

rank_list = []

bio_list = [] #empty list to store all info as single array, to be converted to JSON

fighter_bio_dict = {'name' : fighter_name, 'url' : url}

current_ranking = content.find('td', class_ = "tdRank").text
ranking_array = current_ranking.split(':')

for rank_data in ranking_array: #This organises rankings into usable JSON format
    rank_string = rank_data.replace('\n', '') 
    rank_list.append(rank_string)

for info in info_chart:
    
    info_str = info.text.replace('\t', '')
    string_array = info_str.split(': ') #splits string into key:value array
    if len(string_array) == 2:
        key_value_pair = {string_array[0] : string_array[1]}
        bio_list.append(key_value_pair)
          
bio_list.pop(0) #removes unnecessary header information
if len(bio_list) > 13:
    bio_list.pop(13) #removes Highest quarterly rank

rank_key_value_pair = {rank_list[0] : rank_list[1]}
bio_list.append(rank_key_value_pair)

for bio in bio_list: #Turns the list of objects into one object for JSON conversion
    fighter_bio_dict.update(bio)

fighter_bio_json = json.dumps(fighter_bio_dict)

url_splitter = url.split("https://www.fightmatrix.com/fighter-profile/")
json_filename = url_splitter[1].replace('/', '').replace('+','_') + '.json'
with open(json_filename, "w") as outfile:
        outfile.write(fighter_bio_json)
        
print(json_filename)
