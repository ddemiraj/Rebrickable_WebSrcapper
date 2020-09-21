import sys
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

# Check if the parameter was given
# 0 - Scriptname
# 1 - Parameter
if(len(sys.argv) == 2):

    # check for chrome driver and selenium
    try:
        # BUHLER specific
        chrome_options = webdriver.ChromeOptions()
        PROXY = 'http://uzu047.buhler-ltd.com:3128'  # IP:PORT or HOST:PORT
        chrome_options.add_argument('--proxy-server=%s' % PROXY)
        driver = webdriver.Chrome(options=chrome_options)
        # BUHLER specific

        # driver = webdriver.Chrome()
    except:
        print("Chrome Driver not found!")
        exit()

    if("https://" in str(sys.argv[1]) or "http://" in str(sys.argv[1])):
        # Get URL from argument
        URL = str(sys.argv[1])
    else:
        URL = str('https://rebrickable.com/mocs/'+sys.argv[1])

    # Replace after tailing slash
    deleteParts = {'/#comments', '/#buy_parts', '/#bi', '/#photos', '/#parts'}
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
            driver.get(URL)
            page = driver.page_source

            soup = BeautifulSoup(page, features="html.parser")
            results = soup.find(class_='btn-group js-export-parts-list')

            export_elements = results.find_all('li', class_='')

            # The Link with the HTML Grid table
            a = export_elements[4].find('a')
            inventoryPath = 'https://rebrickable.com' + a['href']
            print(inventoryPath)

            error = False

            break

        except:
            error = True  # retry while loop
            attempt += attempt

            print("Attempting Retry " + str(attempt))

    # close selenium session
    driver.close()
    driver.quit()

else:
    print("Only 1 Argument needed - URL of MOC without tailing slash OR MOC num")
