# TTY system information grabber, written in Python
# Built to run on Unix-like systems, but may function on other systems
# Written and tested by Logan Allen, 2023
# PLEASE REPORT ANY ISSUES TO THE GITHUB REPOSITORY!!! www.github.com/TeaPixl
from platform import machine, system, processor, release
from datetime import datetime
import socket
import psutil
import logging
import sys
import time
import getpass
import shutil
import random
import os

cupImage= """                                                                                       
                                      ██    ██    ██                                    
                                    ██      ██  ██                                      
                                    ██    ██    ██                                      
                                      ██  ██      ██                                    
                                      ██    ██    ██                                    
                                                                                        
                                  ████████████████████                                  
                                  ██   ██████████   ██████                              
                                  ██                ██  ██                              
                                  ██                ██  ██                              
                                  ██                ██████                              
                                    ██            ██                                    
                                ████████████████████████                                
                                ██                    ██                                
                                  ████████████████████"""

# quote
def quoteGen():
    try:
         path = os.path.dirname(__file__)
         realPath = "quotes/quotes.txt"
         location = os.path.join(path, realPath)
         with open(location, 'r') as f:
             quotes = [] # all quotes in list, randomly pick 1 out of 20
             text = f.readlines()
             quotes.append(text)
             chosen = random.choice(text)
             print("\n                             " + chosen)
    except Exception as e:
        logging.exception(e)
        print("\nQuoteGen failed... Proceeding.")
        pass

# loading cursor
def spinningCursor():
    try:
        while True:
            for cursor in "|/-\\":
                yield cursor
    except Exception as e:
        logging.exception(e)
        print("spinningCursor failed... Proceeding.")

# welcoming prompt
def currentUser(): # current user
    user = getpass.getuser()
    print("Hello, " + user)
    
def getTime():
    try:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("It is: "+ current_time)
    except Exception as e:
        logging.exception(e)
        print("\nSomething's wrong, Unable to display the current time.")
        exit()

# sys. uptime
def bootTime():
    return time.time() - psutil.boot_time()

boot = bootTime()/60
approxBoot = round(boot, 1)

# get disk usage
try:
    info = []
    d = shutil.disk_usage("/") # tuple (total, used, free) *data in bytes
    info = list(d)
    info.pop(2)
    total = int(info[0]) / (1024 * 1024 * 1024)
    totalDisk = round(total, 1)
    used = int(info[1]) / (1024 * 1024 * 1024)
    usedDisk = round(used, 1)
    fraction = (usedDisk / totalDisk) *100
    newFraction = str(round(fraction, 1))
except Exception as e:
    logging.exception(e)
    print("\nSomething went wrong while trying to access your disk.")
    exit()

# get cpu freq.
try:
    data = []
    cpuData = psutil.cpu_freq() # tuple (current, min, max)
    data = list(cpuData)
    floatFreq = int(data[0])/1000 #convert MHz to GHz
    freq = str(round(floatFreq, 2))
except Exception as e:
    logging.exception(e)
    print("\nSomething went wrong while trying to access your CPU info.")
    exit()

# get ip addr.
try:
    request = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    request.connect(("8.8.8.8", 80)) # connect to an addr. that is likely to be up
    addr = request.getsockname()
    ip = list(addr)
    ip.pop(1)
    realAddress = str(ip)[2:-2]
except Exception as e:
    logging.exception(e)
    print("Failed to fetch socket name... Proceeding")
    pass

"""MAIN PROGRAM"""
def main():
    try:
        data = [] # data fills list from 0-6
        data.append(str(system()))
        data.append(str(release()))
        data.append(str(machine()))
        data.append(str(socket.gethostname()))
        data.append(realAddress)
        data.append(str(processor()))
        data.append(str(round(psutil.virtual_memory().total / (1024.0 **3)))+" GB") # total RAM
        usage = (psutil.virtual_memory()[2]) # RAM usage
        newUsage = str(round(usage))
        spinner = spinningCursor()
        for _ in range(7):
            sys.stdout.write(next(spinner))
            sys.stdout.flush()
            time.sleep(0.1)
            sys.stdout.write('\b')
        print(cupImage)
        quoteGen()
        currentUser()
        getTime()
        print("*------------------------------*") # display
        print("OS: "+ data[0])
        print("VERSION: "+ data[1])
        print("CPU: "+ data[5] + " ("+ freq + " GHz)")
        print("ARCHITECTURE: "+ data[2])
        print("HOST: "+ data[3])
        print("UPTIME:", approxBoot, "minutes")
        print("IP: "+ data[4])
        print("RAM: "+ newUsage + "% used / " + data[6] + " total")
        print("DISK:", newFraction + "% used / "+ str(totalDisk) +" GB total")
        print("*------------------------------*")
    except Exception as e:
        logging.exception(e)
        print("\nSomething has failed, please check for any issues!!!")
        exit()


if __name__ == "__main__":
    main()
