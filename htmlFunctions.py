from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import json
def getLinkFromMoc(urlInput):
    with open("config.json") as json_data_file:
        config = json.load(json_data_file)
    driver = webdriver.Chrome(config["chromedriver"])
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

# Gets the html from the site
def get_html(url):
    with open("config.json") as json_data_file:
        config = json.load(json_data_file)
    proxy = config["proxy"]["setProxy"]
    http_proxy  = config["proxy"]["http_proxy"]
    https_proxy = config["proxy"]["https_proxy"]
    proxyDict = { 
              "http"  : http_proxy, 
              "https" : https_proxy
            }
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
    with open("config.json") as json_data_file:
        config = json.load(json_data_file)
    driver = webdriver.Chrome(config["chromedriver"])
    try: 
            loginPage = "https://rebrickable.com/login/"
            driver.get(loginPage)
            
            user = driver.find_element_by_name("username")
            user.send_keys(config["login"]["username"])
            
            pas = driver.find_element_by_name("password")
            pas.send_keys(config["login"]["pw"])
            print(config["login"]["username"])
            print(config["login"]["pw"])
            pas.submit()
            driver.get(url)
            html = driver.page_source
            driver.close()
            driver.quit()
    except Exception as e: 
        print ('error when accessing', url, '\n', e) 
        return None
    return html