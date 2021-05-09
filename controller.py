# Own Files
from dataFunctions import extract_data, split_data, addColor_addImage
from excelExport import excelExport
from inputFunctions import getRawHtml

returnObject = getRawHtml()
rawData = returnObject[0]
WorksheetName = returnObject[1]

processedData = extract_data(rawData)
processedData = split_data(processedData, 4)
processedData = addColor_addImage(processedData, rawData)

excelExport(processedData, WorksheetName)
