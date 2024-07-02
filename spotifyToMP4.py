from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
from youtubesearchpython import VideosSearch
from pytube import YouTube

options = Options()
options.binary_location = '/Users/vidhitamittal/Desktop/chromedriver'  # the path to your chromdriver

driver = webdriver.Chrome(options=options)

data = [[]]

playlist_url = 'https://open.spotify.com/playlist/2REmMMi9MAjY6UFuUK2B1I' # link of the spotify playlist from spotify web
driver.get(playlist_url)
time.sleep(10)

titles = driver.find_elements('xpath','//*[@id="main"]/div/div[2]/div[3]/div[1]/div[2]/div[2]/div[2]/main/div[1]/section/div[2]/div[3]/div[1]/div[2]/div[2]/div/div/div[2]/div/a/div')
artists = driver.find_elements('xpath','//*[@id="main"]/div/div[2]/div[3]/div[1]/div[2]/div[2]/div[2]/main/div[1]/section/div[2]/div[3]/div[1]/div[2]/div[2]/div/div/div[2]/div/span/div/a[1]')
    
category_data = []
for i in range(len(titles)):
    category_data.append([titles[i].text, artists[i].text])

data.extend(category_data)

driver.close()

df = pd.DataFrame(data, columns=['Song Title','Artist'])

for i in range(1,len(titles)+1):
    videosSearch = VideosSearch(f"{df['Song Title'][i]}+{df['Artist'][i]} official video", limit = 1)

    searchResult = videosSearch.result()
    link = searchResult['result'][0]['link']

    youtubeObject = YouTube(link)
    youtubeObject = youtubeObject.streams.get_highest_resolution()
    try:
        youtubeObject.download()
    except:
        print("An error has occurred")
    print(f"Download {i} is completed successfully")



