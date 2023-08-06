import numpy as np
import urllib.request as req
from datetime import datetime, timedelta
from browse_file import *

def connect():
    try:
        with  req.urlopen('http://just-the-time.appspot.com/') as response:
            data = response.read()
        return data
    except:
        return False



def license(key):
    CONST = 2 * 3.1416 * 1000
    data = connect()


    temp = str(data)
    year = temp[2:6]
    month = temp[7:9]
    date = temp[10:12]

    now = datetime.now()
    dt_string = now.strftime("%d%m%y")
    dat = now.strftime("%d")
    mon = now.strftime("%m")
    yr = now.strftime("%Y")

   
    encryption_online = int((int(month) * 31*CONST) * (int(year) * 100*CONST))
    encryption_online =str(encryption_online)
    
  

    if encryption_online==str(key):
        val_pass =True
        return val_pass
    else:
        val_pass = False
        return val_pass
    
    ## Testing Block
    # print("the data from the link",temp)
    # print(month)
    # print(year)
    # print(key)
    # print(encryption_online)
   
def checking2(key):
    CONST = 2 * 3.1416 * 1000
    data = connect()


    temp = str(data)
    year = temp[2:6]
    month = temp[7:9]
    date = temp[10:12]

    now = datetime.now()
    dt_string = now.strftime("%d%m%y")
    dat = now.strftime("%d")
    mon = now.strftime("%m")
    yr = now.strftime("%Y")

   
    encryption_online = int((int(month) * 31*CONST) * (int(year) * 100*CONST))
    encryption_online =str(encryption_online)
  

    if encryption_online==str(key):
        val_pass =True
        return val_pass
    else:
        val_pass = False
        return val_pass

def checking3(key):
    CONST = 2 * 3.1416 * 1000
    data = connect()


    temp = str(data)
    year = temp[2:6]
    month = temp[7:9]
    date = temp[10:12]

    now = datetime.now()
    dt_string = now.strftime("%d%m%y")
    dat = now.strftime("%d")
    mon = now.strftime("%m")
    yr = now.strftime("%Y")

   
    encryption_online = int((int(date)*24)*(int(month) * 31*CONST) * (int(year) * 100*CONST))
    encryption_online =str(encryption_online)
    
  ##Testing:
    #print(encryption_online)

    if encryption_online==str(key):
        val_pass =True
        return val_pass
    else:
        val_pass = False
        return val_pass
  

## TESTING
ouput =checking3(1233)
print("the license ouput:", ouput)