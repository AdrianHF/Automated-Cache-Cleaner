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

        if ('Apps' and 'All') in texto: 
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

def homeMenuAppList(ocrTextSS, firstAppName):
    
    print('homeMenuAppList() is running')
    appList = []
    locationList = []
    
    i1= 0
    i=0
    initializeAppList = False
    rango = 0
    stop = len(ocrTextSS)
    print('i vale: ', i)
    print('Stop has been calculated as: ', stop)
    for element in ocrTextSS['text']: 
        
        print('i vale: ', i)
        print('stop vale: ', stop)

        firstWord = ocrTextSS.iloc[i,11]
        appName = []
        appName.append(firstWord)
        
        firstWordLocation = int(ocrTextSS.iloc[i,7])
        
        topValueToCompare = int(ocrTextSS.iloc[i+1,7])
        print('Esta shit vale: ',topValueToCompare)

        i1 = 1 

        
        wordFinished= False

        
        
        
        while wordFinished == False:
            nextWord = ocrTextSS.iloc[i+i1,11]
            print('Check this out')
            print('i vale: ', i)
            print('i1 vale: ', i1)
            if ((topValueToCompare <= (firstWordLocation+5)) and (topValueToCompare >= (firstWordLocation-5))):
                
                appName.append(nextWord)
                i1 = i1 + 1
                topValueToCompare = int(ocrTextSS.iloc[i+i1,7])

                print('i1 vale: ', i1)

            else:

                wordFinished = True
                if ' '.join(appName) == firstAppName:
                    initializeAppList = True

                if ( initializeAppList == True ) or ((rango + 90) <= firstWordLocation <= (rango + 110) ):
                    
                    appName = ' '.join(appName)
                    appList.append(appName)
                    
                    initializeAppList = False
                    rango = firstWordLocation
                    locationList.append(firstWordLocation)
      
        i = i+1
    

    appListDF = pd.DataFrame()        

    appListDF['Name'] = appList
    appListDF['Location'] = locationList



    return appListDF


# This function receives the name of an app to be cleaned, 
# it goes there and clicks the right buttons to get to the clean cache menu

def cacheCleaner(appToBeCleaned):

    print('cacheCleaner() is running')

    appNames = homeMenuAppList(ocrTextSS(),appToBeCleaned)

    print(appNames)
    print(type(appNames))

    print(appNames)
    i = 0
    for appName in appNames['Name']:
        print ('For cicle initiated')
        
    
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
            print ('Aqui si llego')
            if str(ssData.iloc[-1,11]) == 'cache' and str(ssData.iloc[-2,11]) == 'Clear':
                
                pyautogui.moveTo(950, 952)
                time.sleep(3)
                pyautogui.click()
                cleanedApps.append(appToBeCleaned)

print(type(cleanedApps))

cleanedApps = ['Amazon Shopping']

print(cleanedApps[-1])


ocrData = ocrTextSS()    
ocrData = ocrData.reset_index()


indexInRange = (ocrData['top'] >= 455) * ( ocrData['top']<=470)
indexInRange = indexInRange[indexInRange.iloc[:]]


print(ocrData['top'])



print(indexInRange.index)

for element in indexInRange.index:
    print(element)
    print(ocrData['text'].iloc[element])


'''
goHome()
appsToClean = homeMenuAppList(ocrTextSS(), 'Accessibility')

for appName in appsToClean['Name']:
    print('Cleaning: ', appName)
    cacheCleaner(appName)
    goHome()
'''