import pyautogui
import pytesseract
from PIL import Image
import time
import pandas as pd



xStart = 600
yStart = 0
xEnd = 1077
yEnd = 1000

height = yEnd - yStart 
width = xEnd - xStart

screenshotRegion = (xStart, yStart, width, height)

# Home is the apps menu, this function just reads the words 
# on screen and tries to go back to the menu where 'Apps' and 'All' appear

cleanedApps = []


def goHome():

    print('goHome() is running')
    areWeHome = False
    i=0
    while areWeHome == False:

        screenshot = pyautogui.screenshot(region=screenshotRegion)
        screenshot.save('screenshot.png')
        img = Image.open('screenshot.png')
        texto = pytesseract.image_to_string(img, lang='eng')
        i=i+1
        print('Screenshots Taken so far: ', i) 

        if '< Apps Q' in texto: 
            areWeHome = True
            if areWeHome == True:
                print('We are home!')
        else:   
            print('We are not home :c')
            pyautogui.rightClick()
            time.sleep(3)

#This function returns the OCR text found in a screenshot. Only the words above 90% confidence and in a dataframe

def ocrTextSS():

    print('ocrTextSS() is running')
    screenshot = pyautogui.screenshot(region=screenshotRegion)
    screenshot.save('screenshot.png')
    img = Image.open('screenshot.png')
    ssData = pytesseract.image_to_data(img, lang='eng',output_type=pytesseract.Output.DATAFRAME)

    #Removing text detected by the OCR with less than 90% confidence
    keepData = ssData['conf'] >= 90
    ssData = ssData[keepData]

    #Removing empty text detected by OCR
    keepData = ssData['text'] != " "
    ssData = ssData[keepData]

    return ssData


# This function cleans the data frame and returns a dataframe of the apps found with its location, 
# you need to provide the ocrTextSS dataframe and then the first app you want to register on the list

def homeMenuAppList(ocrTextSS, appToStartList):
    ocrTextSS.reset_index(inplace = True)

    appList = []
    appName = []
    locationList = []

    for element in ocrTextSS['top']:

        locationValue = element


        minValue = locationValue - 5
        maxValue = locationValue + 5

        locationRange = [minValue, maxValue]

        getIndex = (ocrTextSS['top'] >= locationRange[0]) * (ocrTextSS['top'] <= locationRange[1])


        getIndex = getIndex[getIndex]    

        getIndex = pd.Series(
            data = getIndex.index
        )
        appName = []
        tempLocationList = []
        for row in getIndex:
      
            appName.append(ocrTextSS['text'].iloc[row])
            tempLocationList.append(ocrTextSS['top'].iloc[row])
        appList.append(' '.join(appName))
        locationList.append(tempLocationList)

        
        

    appList = list(dict.fromkeys(appList))


    i = 0
    while i < len(locationList):
        locationList[i] = locationList[i][0]
        i = i+1

    locationList = list(dict.fromkeys(locationList))

    output = pd.DataFrame()
    
    print('Esta es la appList: ', appList)
    print('len: ',len(appList))
    print('Esta es la locationList: ',locationList)
    print('len: ',len(locationList))


    while len(appList) != len(locationList):
        if len(appList) > len(locationList):
            del appList[-1]
        else:
            del locationList[-1]

    output['Name'] = appList
    output['Location'] = locationList
    output['Keep'] = False

    appToStartList = 'Accessibility'
    targetLocation = 0
    for element in output.index:
        if output['Name'].iloc[element] == appToStartList:
            output.loc[element,'Keep'] = True
            targetLocation = output['Location'].iloc[element]
        if (output['Location'].iloc[element] <= targetLocation + 105) * (output['Location'].iloc[element] >= targetLocation + 95 ):
            output.loc[element,'Keep'] = True
        
            targetLocation = output['Location'].iloc[element]


    output = output[output['Keep']]

    output = output.reset_index(drop=True)
    output.drop('Keep',axis=1, inplace=True)
    return output
        


# This function receives the name of an app to be cleaned, 
# it goes there and clicks the right buttons to get to the clean cache menu

def cacheCleaner(appToBeCleaned):

    print('cacheCleaner() is running')

    appNames = homeMenuAppList(ocrTextSS(),appToBeCleaned)

   
    i = 0
    for appName in appNames['Name']:
        
        
    
        if appToBeCleaned == appName:
            pyautogui.moveTo(808, appNames.iloc[i,1])
            i = i+1
            time.sleep(3)
            pyautogui.click()
            time.sleep(3)
            ssData = ocrTextSS()
            storageLocation = ssData['text'] == 'Storage'
            storageLocation = ssData[storageLocation]
            storageLocation = storageLocation['top']
           
            storageLocation = int(storageLocation.iloc[0])
          
            pyautogui.moveTo(808, storageLocation)
            time.sleep(3)
            pyautogui.click()
            time.sleep(3)
            ssData = ocrTextSS()
           
            if str(ssData.iloc[-1,11]) == 'cache' and str(ssData.iloc[-2,11]) == 'Clear':
                
                pyautogui.moveTo(950, 952)
                time.sleep(3)
                pyautogui.click()
                cleanedApps.append(appToBeCleaned)

    return cleanedApps


pyautogui.moveTo(900,300)

goHome()
appsList = homeMenuAppList(ocrTextSS(),'Accessibility')

print('Esta es el appList: ',appsList)

cleanedApps = cacheCleaner('Accessibility')

print(cleanedApps)
