import openpyxl
from openpyxl import Workbook
from datetime import datetime
import json
import shutil
def excelExport(processedData, WorksheetName): 
    with open("config.json") as json_data_file:
        config = json.load(json_data_file)
    path = config["path"]

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
    workbook.save(config["outputLocation"] + WorksheetName + "_" + current_time + ".xlsx")
    shutil.rmtree(path)
    print("Workbook saved")