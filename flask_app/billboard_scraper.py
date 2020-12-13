from bs4 import BeautifulSoup
import pprint
import requests

def scrape_billboard_hot_20():
    url = 'https://www.officialcharts.com/charts/billboard-hot-100-chart/'
    req = requests.get(url)
    root = BeautifulSoup(req.content, features="html.parser")

    table = root.find("table", {"class":"chart-positions"})
    data = {}

    for i in range(20):
        data[i+1] = []

    song_table = table.findAll("div", {"class":"title"})
    for i in range(len(song_table)):
        data[i+1].append(song_table[i].find("a").text)


    artist_table = table.findAll("div", {"class":"artist"})
    for i in range(len(artist_table)):
        data[i+1].append(artist_table[i].find("a").text)

    image_table = table.findAll("div", {"class": "cover"})
    for i in range(len(image_table)):
        data[i+1].append(image_table[i].find("img")['src'])
    
    return data
