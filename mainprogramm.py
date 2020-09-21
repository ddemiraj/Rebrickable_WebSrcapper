import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook
# from openpyxl import Worksheet
from datetime import datetime
# import mysql.connector



##############################################################################
######################## Settings ############################################
##############################################################################

######################## Proxy ###############################################
# Adapt the Proxy to youre infrastructure
# If you make proxy = false proxyDict will be ignored
proxy = True
http_proxy  = "http://uzu047.buhler-ltd.com:3128"
https_proxy = "https://uzu047.buhler-ltd.com:3128"
proxyDict = { 
              "http"  : http_proxy, 
              "https" : https_proxy
            }

######################## DB ##################################################
# mydb = mysql.connector.connect(
#   host="localhost",
#   user="yourusername",
#   password="yourpassword",
#   database="mydatabase"
# )
# mycursor = mydb.cursor()

##############################################################################
######################## Functions ###########################################
##############################################################################

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
def addColor_addImage(currentArray):
    i = 0
    while i < len(currentArray):
        appendArray = currentArray[i]
        # color =  mycursor.execute("SELECT color_id FROM " + database + ".color WHERE color_name LIKE" + appendArray[3])  
        color = 654654
        appendArray.append(color)
        # img =  mycursor.execute("SELECT color_id FROM " + database + ".color WHERE color_name LIKE" + appendArray[3])  
        img = "img"
        appendArray.append(img)
        i += 1
    return currentArray
     
    
##############################################################################
######################### Input ##############################################
##############################################################################
#     return array
# print('Enter the ID')
# urlInput = input()
# if (urlInput.startswith("https://") == False):
#   urlInput = "https://rebrickable.com/inventory/" + str(urlInput) + "/parts/?format=table"
    
    
url = "https://rebrickable.com/inventory/31956/parts/?format=table&&_=1600413356065"
# url = urlInput

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
processedData = addColor_addImage(processedData)
print(processedData)


##############################################################################
######################## Exel Export #########################################
##############################################################################

# Create Sheet
workbook = Workbook()
worksheet = workbook.active



#▼ listAllParts = [{"legoNum": "4555pr0066", "quantity": 1, "color_id": 0, "color_name": "Black", "description": "Duplo Figure, Early, with Light Gray Legs, Black Top with 3 Buttons and Badge, White Racing Helmet", "img": "https://cdn.rebrickable.com/media/parts/photos/118/PART-5821-118-ec023a5a-eea9-4e42-b9f3-a77cdbf29ee4.jpg"}, {"legoNum": "74201c01", "quantity": 1, "color_id": 2, "color_name": "Green", "description": "Duplo Motorcycle", "img": "https://cdn.rebrickable.com/media/parts/elements/4174122.jpg"}, {"legoNum": "4375", "quantity": 1, "color_id": 4, "color_name": "Red", "description": "Duplo Sign Post Short", "img": "https://cdn.rebrickable.com/media/parts/photos/4/4375-4-35bbbd3d-8f97-41f9-8fc3-94826a6067a5.jpg"}, {"legoNum": "31021p01", "quantity": 1, "color_id": 15, "color_name": "White", "description": "Duplo Fence 1 x 6 x 2 with Red Stripes Print", "img": "https://cdn.rebrickable.com/media/parts/elements/4583393.jpg"}, {"legoNum": "2318c01", "quantity": 1, "color_id": 15, "color_name": "White", "description": "Duplo Flashing Light - Trans-Dark Blue", "img": "https://cdn.rebrickable.com/media/parts/elements/231830.jpg"}, {"legoNum": "4066pb009", "quantity": 1, "color_id": 14, "color_name": "Yellow", "description": "Duplo Brick 1 x 2 x 2 with Road Sign Stop Print", "img": "https://cdn.rebrickable.com/media/parts/photos/14/4066pb009-14-ea401991-5b05-480d-b2a2-b896ece46e98.jpg"}]
listAllParts = processedData

# Set headers
heightAndWidth = 0
worksheet['A1'] = "legoNum"
worksheet.column_dimensions['A'].width = heightAndWidth
worksheet['B1'] = "quantity"
worksheet.column_dimensions['B'].width = heightAndWidth
worksheet['C1'] = "color_id"
worksheet.column_dimensions['C'].width = heightAndWidth
worksheet['D1'] = "color_name"
worksheet.column_dimensions['D'].width = heightAndWidth
worksheet['E1'] = "description"
worksheet.column_dimensions['E'].width = heightAndWidth
worksheet['F1'] = "img"
worksheet.column_dimensions['F'].width = heightAndWidth
worksheet.row_dimensions[1].height = heightAndWidth

# Set data
i = 2
for row in listAllParts:
    #worksheet.row_dimensions[i].height = heightAndWidth
    worksheet.row_dimensions[i].height = heightAndWidth
    worksheet['A' + str(i)] = listAllParts[i-2][0]
    worksheet['B' + str(i)] = listAllParts[i-2][1]
    worksheet['C' + str(i)] = listAllParts[i-2][2]
    worksheet['D' + str(i)] = listAllParts[i-2][4]
    worksheet['E' + str(i)] = listAllParts[i-2][3]
    worksheet['F' + str(i)] = listAllParts[i-2][5]
    i += 1




# Used to make a different Name and save
now = datetime.now()
current_time = now.strftime("%d_%m_%Y_%H.%M.%S")
workbook.save("Export_" + current_time + ".xlsx")
