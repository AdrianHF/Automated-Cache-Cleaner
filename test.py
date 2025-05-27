import pandas as pd
import pyautogui
import time
import numpy as np
data = {

    'Name': ['Name1','Name2','Name3','Name4'],
    'Location': [1,2,3,4]
}

df = pd.DataFrame(data)

print(df['Name'] == 'Name1')
print(type(np.where(df['Name'] == 'Name1')))
print(( np.where(df['Name'] == 'Name1') ))