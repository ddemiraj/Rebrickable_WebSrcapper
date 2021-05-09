from htmlFunctions import getLinkFromMoc, get_html, get_html_Login

def readIntInput(text):
    return int(readInput(text))

def readInput(text):
    print(text)
    read = input()
    print("\n")
    return read

def getRawHtml():
    WorksheetName = "MOC-XXXXXX"
    typeInput = readIntInput("MOC-Nr.\t1\nID of HTML-Table\t2\nPartlist HTML-Table\t3")
    urlInput = readInput("Type in the number or link")
    
    # MOC
    if (typeInput == 1):
        WorksheetName = "MOC-XXXXXX"
        WorksheetName = urlInput
        if (urlInput.startswith("MOC-") == False) and (urlInput.startswith("https:") == False):
            urlInput = "MOC-" + str(urlInput)
        else:
            MocPositionStart = urlInput.find("MOC-")
            MocPositionStop = MocPositionStart+9
            WorksheetName = urlInput[MocPositionStart:MocPositionStop]
            urlInput = getLinkFromMoc(urlInput)
        return [get_html(urlInput), WorksheetName]

    # MOC html table
    if (typeInput == 2):
        if (urlInput.startswith("https:") == False):
            urlInput = "https://rebrickable.com/inventory/" + str(urlInput) + "/parts/?format=table"
        return [get_html(urlInput), WorksheetName]
            
    # Part HTML table
    if (typeInput == 3):
        if (urlInput.startswith("https:") == False):
            urlInput = "https://rebrickable.com/users/Exonic/partlists/" + str(urlInput) + "/parts/?format=table"
        return [get_html_Login(urlInput), WorksheetName]
    
    print("Not a valid input type")