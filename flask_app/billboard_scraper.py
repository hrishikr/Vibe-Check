# from urllib.request import urlopen
from bs4 import BeautifulSoup
import pprint
import requests

def scrape_billboard_hot_20():
    url = 'https://www.officialcharts.com/charts/billboard-hot-100-chart/'
    req = requests.get(url)
    root = BeautifulSoup(req.content)

    json = {
        "position": [],
        "song": [],
        "artist": [],
        "image_url": []
    }

    table = root.find("table",{"class":"chart-positions"})
    print(table)
    songs = []
    artists = []
    images = []

    song_table = table.findAll("div",{"class":"title"})
    for i in range(len(song_table)):
        songs.append(song_table[i].find("a").text)

    artist_table = table.findAll("div",{"class":"artist"})
    for i in range(len(artist_table)):
        artists.append(artist_table[i].find("a").text)

    image_table = table.findAll("div", {"class": "cover"})
    for i in range(len(image_table)):
        images.append(image_table[i].find("img")['src'])
    
    return songs, artists, images

if __name__ == '__main__':
    # pp = pprint.PrettyPrinter(width=41, compact=True)
    # pp.pprint(scrape_billboard_hot_100())
    scrape_billboard_hot_20()

