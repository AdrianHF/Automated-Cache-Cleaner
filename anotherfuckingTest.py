import pandas as pd
import pyautogui as auto
import time
data = pd.read_csv('datos.csv')


data = data.iloc[:,1:]

print(data)

appList = []
appName = []
locationList = []

for element in data['top']:

    locationValue = element


    minValue = locationValue - 5
    maxValue = locationValue + 5

    locationRange = [minValue, maxValue]

    getIndex = (data['top'] >= locationRange[0]) * (data['top'] <= locationRange[1])


    getIndex = getIndex[getIndex]    

    getIndex = pd.Series(
        data = getIndex.index
    )
    appName = []
    tempLocationList = []
    for row in getIndex:
        appName.append(data['text'].iloc[row])
        tempLocationList.append(data['top'].iloc[row])
    appList.append(' '.join(appName))
    locationList.append(tempLocationList)

    print('hola')
    print(getIndex)
    

appList = list(dict.fromkeys(appList))


i = 0
while i < len(locationList):
    locationList[i] = locationList[i][0]
    i = i+1

locationList = list(dict.fromkeys(locationList))

output = pd.DataFrame()

output['Name'] = appList
output['Location'] = locationList
output['Keep'] = False

appToStartList = 'Accessibility'
targetLocation = 0
for element in output.index:
    if output['Name'].iloc[element] == appToStartList:
        output.loc[element,'Keep'] = True
        targetLocation = output['Location'].iloc[element]
    if (output['Location'].iloc[element] <= targetLocation + 110) * (output['Location'].iloc[element] >= targetLocation + 90 ):
        output.loc[element,'Keep'] = True
    
        targetLocation = output['Location'].iloc[element]


output = output[output['Keep']]

output = output.reset_index(drop=True)
output.drop('Keep',axis=1, inplace=True)
print(output)