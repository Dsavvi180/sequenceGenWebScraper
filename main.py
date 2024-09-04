# When installing packages run pip install __package__ && pip freeze > requirements.txt
# Run this code in a personal virtual python environment
# use 'pip install -r requirements.txt' once in venv to download required dependencies
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
import logging
import sys

# Configure the logging settings
logging.basicConfig(level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Variables for memory tracking
memory_usage_data = []  # Store memory usage data
timestamps = []  # Store timestamps
sequenceNumber = []


### The below two functions track memory usage of the script and the latter plots a graph at the end of the script of memory usage against sequence count ###
def track_memory_usage(indexRec):
    """Track and record the memory usage."""
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    memory_usage = memory_info.rss / (1024 * 1024)  # Convert to MB
    print(f"\n\n*******   Current memory usage: {memory_usage}  ******* \n")
    memory_usage_data.append(memory_usage)
    # timestamps.append(time.time())
    sequenceNumber.append(indexRec)


def plot_memory_usage():
    """Plot the memory usage over time."""
    plt.figure(figsize=(10, 5))
    plt.plot(sequenceNumber, memory_usage_data,
             marker='o', linestyle='-', color='b')
    plt.title('Memory Usage by Sequence Count')
    plt.xlabel('Sequence Number')
    plt.ylabel('Memory Usage (MB)')
    plt.grid(True)
    plt.show()


### **** ENTER INPUT DATA CSV HERE: **** ###
### basic data cleaning of input CSV to pass sequences and preference data through to relevant functions: ###
inputPrimersCsv = '/Users/damensavvasavvi/Desktop/sequenceGenerationWebscraper/neb_lamp_preferencesInput.csv'
inputPrimersAndPreferences = pd.read_csv(inputPrimersCsv)[::-1]
inputPrimersAndPreferences.columns = inputPrimersAndPreferences.columns.str.strip()
sequencesList = inputPrimersAndPreferences['sequence to paste'].to_list()
parameterSet = inputPrimersAndPreferences["Parameter Set"].to_list()
fieldValueColumns = inputPrimersAndPreferences.columns[2:].to_list()
fieldValues = inputPrimersAndPreferences[fieldValueColumns]
primerOutputJsonArray = []

### Process for initialising WebDriver and navigating to the URL, implements a maximum retry limit of 3 incase errors upon starting the driver occur ###
### Sets Chrome instance window to the following coordinates on your screen X:900, Y:1000 ###


def startUpDriver(retries=0):
    maxRetries = 3
    try:
        print("Starting WebDriver...")
        options = webdriver.ChromeOptions()
        # Sets directory downloads are saved to
        prefs = {
            "download.default_directory": "/Users/damensavvasavvi/Desktop/sequenceGenerationWebscraper/primerResults"}
        options.add_experimental_option("prefs", prefs)
        # options.add_argument("--headless")
        options.add_argument(
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")
        # script default = 30000, implicit default = 0: implicit wait sets wait period to wait for each element if not found yet
        options.timeouts = {'script': 10000, 'implicit': 5000}
        driver = webdriver.Chrome(options=options)
        window_width = 800
        window_height = 1000
        driver.set_window_size(window_width, window_height)
        driver.set_window_position(900, 1000)
        driver.set_script_timeout(45)
        driver.get("https://lamp.neb.com/#!/")
        handleCookies(driver)
    except Exception as e:
        logging.exception(f"Error starting up WebDriver {e}")
        driver.quit()
        if retries <= maxRetries:
            driver = startUpDriver(retries+1)
            print('Trying again')
        else:
            logging.exception(
                f"FATAL: cannot initialise WebDriver at all, ending script. \n {e}")
            sys.exit(1)
        raise
    finally:
        return driver

### Passes required variable to the processSequence() function, returns False upon any errors within processSequence or itself, and True upon successful execution of processSequence(), which indicated by the name, ###
### is responsible for processing an indvidual sequence through the online tool ###


def navigateWebsite(driver, indexRec, sequence):
    try:
        time.sleep(2)
        print(f"\nStarting generation for sequence {indexRec}\n")
        index = sequencesList.index(sequence)
        formattedSequence = f">Sequence_{indexRec}\n{sequencesList[indexRec]}"
        processSequence(
            driver, formattedSequence, parameterSet[index], fieldValues.iloc[index])
        return True
    except Exception:
        logging.exception(f"""Exception occurred in navigating website, on sequence {
                          indexRec}, restarting driver...""")
        return False

### This function pulls together the above functions to configure correct execution of the entire webscraping process, and implements logic for what sequence the helper methods execute in, handles errors ###
### thrown by the helper methods and implements error handling techniques to overcome the errors, in order to successfully iterate through all sequences in the data set without manual intervention###


def main(indexRec=0):
    driver = startUpDriver()

    try:
        isSuccessful = True
        while indexRec < len(sequencesList):
            sequence = sequencesList[indexRec]

            if (indexRec != 0 and indexRec % 20 == 0) or not isSuccessful:
                driver.quit()
                print(
                    "Exception occurred or sequence is a multiple of 20, quitting driver...")
                driver = startUpDriver()
            isSuccessful = navigateWebsite(driver, indexRec, sequence)
            indexRec += 1
            track_memory_usage(indexRec)
    except Exception as e:
        driver.quit()
        print("Exception occurred, restarting rerunning main function...")
        main(indexRec)
        logging.exception(f"Error while running main(): {e}")
        raise

    finally:
        if driver:
            driver.quit()
        plot_memory_usage()
        print("Script complete. Check output.log for details.")


if __name__ == "__main__":
    original_std_out, original_std_err = sys.stdout, sys.stderr
    ### Redirect standard output to log_file, creates file if it doesn't exist: use for advanced pattern matching/regex analysis of processing sequences on large data sets ###
    with open("output.log", "w") as log_file:
        sys.stdout = log_file
        sys.stderr = log_file
        main()
    sys.stdout, sys.stderr = original_std_out, original_std_err
