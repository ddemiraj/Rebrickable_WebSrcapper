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
import tkinter as tk

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
if os.path.isdir(path) == False:
    os.mkdir(path)

######################## DB ##################################################
# Adapt the variables
mydb = mysql.connector.connect(
host="localhost",
user="root",
password="",
database="webscrapper"
)
database="webscrapper"
mycursor = mydb.cursor(buffered=True)


##############################################################################
######################## Functions ###########################################
##############################################################################

class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.69 Safari/537.36"


# Gets the html from the site
def get_html(url):
    try: 
        if (proxy == True):
            response = requests.get(url, proxies=proxyDict) 
        else:
            response = requests.get(url)
        content_type = response.headers['Content-Type'].lower()
        if (response.status_code == 200 and content_type is not None and content_type.find('html') > -1): 
          return response.content 
    except Exception as e: 
        print ('error when accessing', url, '\n', e) 
    return None

def get_html_Login(url):
    username = "dämler"
    password = "BLJ4ever"
    driver = webdriver.Chrome("C:/chromedriver.exe")
    try: 
            username = "dämler"
            password = "Abc_1234"

            loginPage = "https://rebrickable.com/login/"
            driver = webdriver.Chrome("C:/chromedriver.exe")
            driver.get(loginPage)
            
            user = driver.find_element_by_name("username")
            user.send_keys(username)
            
            pas = driver.find_element_by_name("password")
            pas.send_keys(password)

            pas.submit()
            driver.get(url)
            html = driver.page_source
            print(html)
            driver.close()
            driver.quit()
    except Exception as e: 
        print ('error when accessing', url, '\n', e) 
        return None
    return html

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
    f = open("C:\Exports\debugOut.txt", "w")
    f.write(str(rawData))
    f.close()
    i = 0
    items = []
    for index, element in enumerate(rawData.select('img')):
         element = str(element)
         element = element.replace('<img class="img-responsive" data-src="', '')
         element = element.replace('<img class="img-responsive lazy-hidden" data-src="', '')
         element = element.replace('" height="85" src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7" width="85"/>', '')
         urllib._urlopener = AppURLopener()
         urllib._urlopener.retrieve(element,"C:/Rebrickable_Pictures_temp/" + str(index) + ".jpg")
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
     

def urlInput(urlInput):
    driver = webdriver.Chrome("C:/chromedriver.exe")
	# Input is the userinput, output is the URL of the HTML-table or an error
    if("https://" in urlInput or "http://" in urlInput):
        # Get URL from argument
        URL = urlInput
        inventoryPath = URL
    else:
        URL = str('https://rebrickable.com/mocs/'+urlInput)

    # Replace after tailing slash
    deleteParts = {'/#comments', '/#buy_parts', '/#bi', '/#photos', '/#parts', '#details'}
    for delete in deleteParts:
        URL = URL.replace(str(delete), '')
        
    if(URL[len(URL) - 1] != '/'):
        URL = URL + '/#parts'
            
    else:
        URL = URL + '#parts'
            
    # retry while error occured
    error = True  # only initial value
    attempt = 0
    while error and attempt < 3:
        try:
            print(URL)
            driver.get(URL)
            page = driver.page_source
            soup = BeautifulSoup(page, features="html.parser")
            results = soup.find(class_='btn-group js-export-parts-list')
           
            export_elements = results.find_all('li', class_='')
            # The Link with the HTML Grid table
            a = export_elements[4].find('a')
            inventoryPath = 'https://rebrickable.com' + a['href']
            error = False
            break
            
        except:
            error = True  # retry while loop
            attempt += 1
                
            print("Attempting Retry " + str(attempt))
            
        # close selenium session
        driver.close()
        driver.quit()
    return inventoryPath
    
##############################################################################
######################### Input ##############################################
##############################################################################

print("MOC-Nr.\t1\nID of HTML-Table\t2\nPartlist HTML-Table\t3\n")
typeInput = input()
print("Type in the number or link")
userInput = input()
# MOC


WorksheetName = "MOC-XXXXXX"
if (int(typeInput) == 1):
     WorksheetName = userInput
     if (userInput.startswith("MOC-") == False) and (userInput.startswith("https:") == False):
       userInput = "MOC-" + str(userInput)
     else:
         MocPositionStart = userInput.find("MOC-")
         MocPositionStop = MocPositionStart+9
         WorksheetName = userInput[MocPositionStart:MocPositionStop]
     userInput = urlInput(userInput)
# MOC html table
if (int(typeInput) == 2):
     if (userInput.startswith("https:") == False):
       userInput = "https://rebrickable.com/inventory/" + str(userInput) + "/parts/?format=table"
      
# Part HTML table
if (int(typeInput) == 3):
    if (userInput.startswith("https:") == False):
       userInput = "https://rebrickable.com/users/Exonic/partlists/" + str(userInput) + "/parts/?format=table"

url = userInput




##############################################################################
######################### Get and process data ###############################
##############################################################################

# Gets the html from the site
if(int(typeInput) == 3):
    rawData = get_html_Login(url)    
    print("get_html_Login")
else:
    rawData = get_html(url)
    print("get_html")

# Select the elements needed and converts them into an array
processedData = extract_data(rawData)
# Throws out \n\n in the table
processedData = list(filter(('\n\n').__ne__, processedData))
# Splits the array into a 2-dimentional array with an array for every dataset
processedData = split_data(processedData, 4)
# Add color code to array
print(processedData)
processedData = addColor_addImage(processedData, rawData)

##############################################################################
######################## Exel Export #########################################
##############################################################################

# Create Sheet
workbook = Workbook()
worksheet = workbook.active

listAllParts = processedData

# Set headers
# width = 7
height = 65
width = 13
worksheet['A1'] = "img"
worksheet.column_dimensions['A'].width = width
worksheet['B1'] = "legoNum"
worksheet.column_dimensions['B'].width = width
worksheet['C1'] = "quantity"
worksheet.column_dimensions['C'].width = width
worksheet['D1'] = "color_id"
worksheet.column_dimensions['D'].width = width
worksheet['E1'] = "color_name"
worksheet.column_dimensions['E'].width = width
worksheet['F1'] = "description"

worksheet.column_dimensions['F'].width = width


# Set data
i = 2
for row in listAllParts:
    #worksheet.row_dimensions[i].height = heightAndWidth
    worksheet.row_dimensions[i].height = height
    img = openpyxl.drawing.image.Image(str(path) + '/' + str(listAllParts[i-2][5]) + '.jpg')
    img.anchor = 'A' + str(i)
    worksheet['B' + str(i)] = listAllParts[i-2][0]
    worksheet['C' + str(i)] = listAllParts[i-2][1]
    worksheet['D' + str(i)] = listAllParts[i-2][4]
    worksheet['E' + str(i)] = listAllParts[i-2][2]
    worksheet['F' + str(i)] = listAllParts[i-2][3]
    
    worksheet.add_image(img)
    i += 1


# Used to make a different Name and save
now = datetime.now()
current_time = now.strftime("%d_%m_%Y_%H.%M")
workbook.save("C:/Exports/Export_" + WorksheetName + "_" + current_time + ".xlsx")
print("Workbook saved")
# Remove the Directory that was created for the Pictures
# Caution, by changeing the path its possible to destroy youre os
shutil.rmtree(path)
