import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook
import openpyxl
# from openpyxl import Worksheet
from datetime import datetime
import mysql.connector
import os
import shutil
import sys
from selenium import webdriver
import urllib.request

##############################################################################
######################## Settings ############################################
##############################################################################

######################## Proxy ###############################################
# Adapt the Proxy to youre infrastructure
# If you make proxy = false proxyDict will be ignored
proxy = False
http_proxy  = "http://uzu047.buhler-ltd.com:3128"
https_proxy = "https://uzu047.buhler-ltd.com:3128"
proxyDict = { 
              "http"  : http_proxy, 
              "https" : https_proxy
            }

######################## Path ################################################
# Be carefull when changing the Path, it could destroy youre OS
path = "C:/Rebrickable_Pictures_temp"
# Creates the directory
os.mkdir(path)

######################## DB ##################################################
# Adapt the variables
mydb = mysql.connector.connect(
host="localhost",
user="BLJ4ever",
password="BLJ4ever",
database="asdf"
)
database="asdf"
mycursor = mydb.cursor()

##############################################################################
######################## Functions ###########################################
##############################################################################

class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.69 Safari/537.36"


# Gets the html from the site
def get_url(url):
    try: 
        if (proxy == True):
            response = requests.get(url, proxies=proxyDict) 
        else:
            response = requests.get(url) 
        content_type = response.headers['Content-Type'].lower()
        if (response.status_code == 200 and content_type is not None 
            and content_type.find('html') > -1): 
          return response.content 
    except Exception as e: 
        print ('error when accessing', url, '\n', e) 
    return None

# Select the elements needed and converts them into an array
def extract_data(response_content): 
    items = []
    raw_html = BeautifulSoup(response_content, 'html.parser') 
    for index, element in enumerate(raw_html.select('td')):
        items.append(element.text)
    return items
        
# Splits the array into a 2-dimentional array with an array for every dataset
def split_data(inputArray, length):
    chunkarr = [] 
    i = 0
    while i < len(inputArray):
        chunkarr.append(inputArray[i:i+length]); 
        i += length
    return chunkarr

# Add color code to array
def addColor_addImage(currentArray, response_content):
    rawData = BeautifulSoup(response_content, 'html.parser')
    i = 0
    items = []
    for index, element in enumerate(rawData.select('img')):
         element = str(element)
         element = element.replace('<img class="img-responsive" data-src="', '')
         element = element.replace('" height="85" src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7" width="85"/>', '')
         urllib._urlopener = AppURLopener()
         urllib._urlopener.retrieve(element,"C:/Rebrickable_Pictures_temp/" + str(index) + ".jpg")
         # urllib.request.urlretrieve(element, "C:/Rebrickable_Pictures_temp/" + str(index) + ".jpg")
         items.append(index)
    while i < len(currentArray):
        appendArray = currentArray[i]
        mycursor.execute("SELECT id FROM " + database + ".colors WHERE name LIKE '" + appendArray[2] + "'") 
        color = mycursor.fetchone()
        color = color[0]
        appendArray.append(color)
        appendArray.append(items[i])
        i += 1
    return currentArray
     
    
##############################################################################
######################### Input ##############################################
##############################################################################

print('Enter the ID')
urlInput = input()
if (urlInput.startswith("https://") == False):
    if (urlInput.startswith("MOC-") == False):
        urlInput = "https://rebrickable.com/inventory/" + str(urlInput) + "/parts/?format=table"
    else:
        print("Fehler, bitte geben sie die MOC-Nr. im Format MOC-<Nr.> an. Es ist auch mölgich den Link des HTML-Tabels anzugeben oder auch die Nummer des HTML-Tabel")

    
# url = "https://rebrickable.com/inventory/31956/parts/?format=table&&_=1600413356065"
url = urlInput


##############################################################################
######################### Get and process data ###############################
##############################################################################

# Gets the html from the site
rawData = get_url(url)
# Select the elements needed and converts them into an array
processedData = extract_data(rawData)
# Throws out \n\n in the table
processedData = list(filter(('\n\n').__ne__, processedData))
# Splits the array into a 2-dimentional array with an array for every dataset
processedData = split_data(processedData, 4)
# Add color code to array
processedData = addColor_addImage(processedData, rawData)

##############################################################################
######################## Exel Export #########################################
##############################################################################

# Create Sheet
workbook = Workbook()
worksheet = workbook.active

listAllParts = processedData

# Set headers
width = 7
worksheet['A1'] = "legoNum"
worksheet.column_dimensions['A'].width = width
worksheet['B1'] = "quantity"
worksheet.column_dimensions['B'].width = width
worksheet['C1'] = "color_name"
worksheet.column_dimensions['C'].width = width
worksheet['D1'] = "color_id"
worksheet.column_dimensions['D'].width = width
worksheet['E1'] = "description"
worksheet.column_dimensions['E'].width = width
worksheet['F1'] = "img"
height = 65
width = 13
worksheet.column_dimensions['F'].width = width


# Set data
i = 2
for row in listAllParts:
    #worksheet.row_dimensions[i].height = heightAndWidth
    worksheet.row_dimensions[i].height = height
    worksheet['A' + str(i)] = listAllParts[i-2][0]
    worksheet['B' + str(i)] = listAllParts[i-2][1]
    worksheet['C' + str(i)] = listAllParts[i-2][2]
    worksheet['D' + str(i)] = listAllParts[i-2][4]
    worksheet['E' + str(i)] = listAllParts[i-2][3]
    img = openpyxl.drawing.image.Image(str(path) + '/' + str(listAllParts[i-2][5]) + '.jpg')
    img.anchor = 'F' + str(i)
    worksheet.add_image(img)
    i += 1



# Used to make a different Name and save
now = datetime.now()
current_time = now.strftime("%d_%m_%Y_%H.%M.%S")
workbook.save("Export_" + current_time + ".xlsx")

# Remove the Directory that was created for the Pictures
# Caution, by changeing the path its possible to destroy youre os
shutil.rmtree(path)
