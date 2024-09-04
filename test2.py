####### IGNORE #######


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from preferences import preferences as handlePreferences
from handleCookies import handleCookies
from selenium.webdriver.support.wait import WebDriverWait
import time
import pandas as pd
from processSequence import processSequence as processSequence
import json
import psutil
import os
import matplotlib.pyplot as plt
import pyautogui

options = webdriver.ChromeOptions()
prefs = { "download.default_directory": "/Users/damensavvasavvi/Desktop/sequenceGenerationWebscraper/primerResults"} #Sets directory downloads are saved to
options.add_experimental_option("prefs",prefs)
# options.add_argument("--headless")
options.add_argument("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")
options.timeouts = { 'script': 10000 ,'implicit': 5000 } #script default = 30000, implicit default = 0: implicit wait sets wait period to wait for each element if not found yet
driver = webdriver.Chrome(options=options)
# Get screen size of the MacBook Air
screen_width, screen_height = pyautogui.size()

# Example screen resolution for MacBook Air could be 1440x900
# Set the window size to something smaller than the screen resolution
window_width = 800
window_height = 1000
driver.set_window_size(window_width, window_height)

# Set the window position to the bottom-right corner of the MacBook Air screen
driver.set_window_position(900, 1000)  
driver.set_script_timeout(45) 
driver.get("https://lamp.neb.com/#!/")
time.sleep(20000)


