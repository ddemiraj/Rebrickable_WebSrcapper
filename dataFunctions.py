from bs4 import BeautifulSoup
import urllib.request
import mysql.connector
import json
import os

def extract_data(response_content): 
    items = []
    raw_html = BeautifulSoup(response_content, 'html.parser') 
    for index, element in enumerate(raw_html.select('td')):
        items.append(element.text)
    items = list(filter(('\n\n').__ne__, items))
    return items

def split_data(inputArray, length):
    chunkarr = [] 
    i = 0
    while i < len(inputArray):
        chunkarr.append(inputArray[i:i+length]); 
        i += length
    return chunkarr

def addColor_addImage(currentArray, response_content):
    with open("config.json") as json_data_file:
        config = json.load(json_data_file)
    path = config["path"]
    

    if os.path.isdir(path) == False:
        os.mkdir(path)
    
    class AppURLopener(urllib.request.FancyURLopener):
        version = "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.69 Safari/537.36"
        with open("config.json") as json_data_file:
            config = json.load(json_data_file)
    mydb = mysql.connector.connect(
        host=config["mysql"]["host"],
        user=config["mysql"]["user"],
        password=config["mysql"]["passwd"],
        database=config["mysql"]["db"]
    )
    # database="webscrapper"
    mycursor = mydb.cursor(buffered=True)
    rawData = BeautifulSoup(response_content, 'html.parser')
    i = 0
    items = []
    for index, element in enumerate(rawData.select('img')):
         element = str(element)
         element = element.replace('<img class="img-responsive" data-src="', '')
         element = element.replace('<img class="img-responsive lazy-hidden" data-src="', '')
         element = element.replace('" height="85" src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7" width="85"/>', '')
         urllib._urlopener = AppURLopener()
         urllib._urlopener.retrieve(element, path + "/" + str(index) + ".jpg")
         items.append(index)
    while i < len(currentArray):
        appendArray = currentArray[i]
        mycursor.execute("SELECT id FROM " + mydb.database + ".colors WHERE name LIKE '" + appendArray[2] + "'") 
        color = mycursor.fetchone()
        color = color[0]
        appendArray.append(color)
        appendArray.append(items[i])
        i += 1
    return currentArray