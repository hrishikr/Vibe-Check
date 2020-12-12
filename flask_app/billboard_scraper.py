# from urllib.request import urlopen
from bs4 import BeautifulSoup
# import pprint
import requests

url = 'https://www.officialcharts.com/charts/billboard-hot-100-chart/'
req = requests.get(url)
root = BeautifulSoup(req.content)
table = root.find("table",{"class":"chart-positions"})
data = table.findAll("div",{"class":"title"})
songs = []
for i in range(len(data)):
    songs.append((data[i].find("a").text))
artists = []
data2 = table.findAll("div",{"class":"artist"})
for i in range(len(data2)):
    artists.append((data2[i].find("a").text))
d = {"songs":songs, "artists":artists}
print(songs)
print("---------")
print(artists)



# def scrape_billboard_hot_100():
#     url = 'https://www.billboard.com/charts/hot-100'
#     req = requests.get(url)
#     soup = BeautifulSoup(req.content, "html.parser")
#     containers = soup.select('article[class*=chart]')
#     print(containers)

#     json = {
#         "position": [],
#         "song": [],
#         "artist": [],
#         "last_week": [],
#         "peak_position": [],
#         "weeks_on_chart": []
#     }

#     chart_pos = 1

#     # Loops through each container
#     for container in containers:

#         # Container storing the song name and artist name
#         song_container = container.find('div', {'class': 'chart-row__title'})

#         # Grabs the song name
#         song = song_container.h2.text
        
#         # Grabs the artist name
#         try:
#             artist = song_container.a.text.strip()
#         except AttributeError:
#             artist = song_container.span.text.strip()

#         # Grabs the song's position last week
#         last_week_container = container.find('div', {'class': 'chart-row__last-week'})
#         last_week = last_week_container.find('span', {'class': 'chart-row__value'}).text

#         # Grabs the song's peak position
#         peak_position_container = container.find('div', {'class': 'chart-row__top-spot'})
#         peak_position = peak_position_container.find('span', {'class': 'chart-row__value'}).text

#         # Grabs the song's duration in the hot 100 (in weeks)
#         weeks_on_chart_container = container.find('div', {'class': 'chart-row__weeks-on-chart'})
#         weeks_on_chart = weeks_on_chart_container.find('span', {'class': 'chart-row__value'}).text

#         json['position'].append(chart_pos)
#         json['song'].append(song)
#         json['artist'].append(artist)
#         json['last_week'].append(last_week)
#         json['peak_position'].append(peak_position)
#         json['weeks_on_chart'].append(weeks_on_chart)

#         chart_pos += 1
    
#     return json

# if __name__ == '__main__':
#     pp = pprint.PrettyPrinter(width=41, compact=True)
#     pp.pprint(scrape_billboard_hot_100())

