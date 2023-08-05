from . import settings
import sys
from datetime import datetime

def info(message:str):
    if(settings.aindapy_log_lvl >= 1):
        print("{} - {}".format(datetime.now(), message))

def warning(message:str):
    if(settings.aindapy_log_lvl >= 1):
        print("{} - WARNING: {}".format(datetime.now(), message))

def debug(message:str, extraData = None):
    if(settings.aindapy_log_lvl >= 2):
        print("{} - {}".format(datetime.now(), message))
    if(settings.aindapy_log_lvl >= 3 and extraData != None):
        print(extraData)
    
    
def error(message:str, extraData = None):
    if(settings.aindapy_log_lvl >= 2):
        print("{} - {}".format(datetime.now(), message))
    if(settings.aindapy_log_lvl >= 3 and extraData != None):
        print(extraData)
    exit()


# Log::emergency($message);
# Log::alert($message);
# Log::critical($message);
# Log::error($message);
# Log::warning($message);
# Log::notice($message);
# Log::info($message);
# Log::debug($message);