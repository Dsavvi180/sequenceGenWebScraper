# When installing packages run pip install __package__ && pip freeze > requirements.txt
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from preferences import preferences as handlePreferences
from handleCookies import handleCookies
from selenium.webdriver.support.wait import WebDriverWait
import time
from resultsTable import resultsTable as result
from preferences import sequencePreferences
import logging
import traceback
import sys
# Configure the logging settings
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


# sequence=f">sequence 1\nTGACAAAATTAGCAGTTGTAGGTGCAACAGGATTAGTTGGAACAAAAATATTAGAAACAATTGAACGTAAAGAAATCCCTTTTGATGAATTGATTTTATTTTCTTCAAAACGTTCAGCAGGTCAACAAGTGTCTTTTAAAGGTAAAACCTACACTGTTCAAGAATTGACAGAAGAAGCGACTGACGGCGAATTTGATTACGTGTTAATGAGCGCTGGTGGTGGTACAAGTGAAAAATTCGCCCCTCTTTTTGAAAAACATGGTGCGCTTGTGATTGATAACTCAAGTCAATGGCGAATGACTAAAGATATTGACCTCATTGTTCCTGAAGTCAATGAGCCGACGTTTAAACGTGGTATCATAGCCAAACCCTAATTGTTCAACAATACAATCAGTCGTGCCATTAAAACCCCTTCAAGATACATTCGGTTTAAAACGGGTCGCTTATACAACGTATCAAGCGGTATCAGGTTCAGGAATGCAAGGAAAGAAAGATTTAGAAGATGGCGCACATGGCGCTGAACCTAAAGCATACCCACATCCAATTTATAATAATGTGTTACCACATATAGATAGTTTTCTTGAAGATGGCTATACAAAAGAAGAACAAAAAATGATTGATG"

def formatException(e):
    tb = traceback.extract_tb(sys.exc_info()[2])[0]
    # Extract file name, line number, and function name
    filename, line_number, function_name, text = tb
    logging.error(f"""Error: {type(e).__name__} occurred in {filename} at line {
                  line_number} in function {function_name}""")


def processSequence(driver, sequence, parameterSet, preferenceValues):
    # Handle "No primer sets available alert" or "All results will be cleared alert":
    def alert(xpath):
        try:
            time.sleep(1)
            driver.find_element(By.XPATH, xpath)
            return True
        except Exception as e:
            # print(f"Alert element not found, with exception: {e.__str__}")
            # print("Proceeding")

            return False
    # print(f"\n\nSEQUENCE: {sequence}\n\n")
    try:
        pasteSequence = driver.find_element(
            By.XPATH, '//*[@id="inputSeqEntryType"]/div/label[1]')
        pasteSequence.click()

        pasteBox = driver.find_element(By.XPATH, '//*[@id="target"]')
        pasteBox.clear()
        pasteBox.click()
        pasteBox.send_keys(sequence)

        processText = driver.find_element(By.XPATH, '//*[@id="parseseq"]')
        processText.click()

        preferences = driver.find_element(
            By.XPATH, '//*[@id="content-view"]/div[1]/div[1]/div/div/div/ul/li[2]')
        preferences.click()
        handlePreferences(driver, parameterSet, preferenceValues)

        specifyParameterSelection = driver.find_element(
            By.XPATH, '//*[@id="content-view"]/div[1]/div[1]/div/div/div/div/div[1]/ng-include/div/div/div[9]/div/div/div/div/p[2]/input')
        specifyParameterSelection.click()

        # Navigates to Set_Fixed page
        continueButton = driver.find_element(
            By.XPATH, '//*[@id="content-view"]/div[1]/div[1]/div/div/div/div/div[1]/ng-include/div/div/div[11]')
        continueButton.click()

        if alert('/html/body/div[1]/div/div/div[2]/div/p'):
            driver.find_element(
                By.XPATH, '/html/body/div[1]/div/div/div[3]/button[1]').click()

        generatePrimers = driver.find_element(
            By.XPATH, '//*[@id="content-view"]/div[1]/div[1]/div/div/div/div/div[3]/ng-include/div/div/div[4]/div[1]/button/span')
        generatePrimers.click()

        try:
            if alert('/html/body/div[1]/div/div/div[2]/div/p'):
                confirm = driver.find_element(
                    By.XPATH, '/html/body/div[1]/div/div/div[3]/button')
                confirm.click()
                print("No primers generated, start next sequence.")
                # Navigate back to first page
                # sequencePage = driver.find_element(By.XPATH,'//*[@id="content-view"]/div[1]/div[1]/div/div/div/ul/li[1]/a')
                # sequencePage.click()
                #### No further execution, skip to next sequence ###
            else:
                try:
                    selectPrimer = driver.find_element(
                        By.XPATH, '//*[@id="primerViewTable"]/table/tbody/tr[6]/td[1]/input[1]')
                    selectPrimer.click()
                    # generateLoopPrimers = driver.find_element(By.XPATH,'//*[@id="content-view"]/div[1]/div[1]/div/div/div/div/div[4]/ng-include/form/div[2]')
                    # generateLoopPrimers.click()
                    # noLoopPrimersAvailable = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[2]/div/p')
                    # if noLoopPrimersAvailable:
                    #     confirmAlert = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[3]/button')
                    #     confirmAlert.click()
                    #     getSelectedPrimers = driver.find_element(By.XPATH,'//*[@id="content-view"]/div[1]/div[1]/div/div/div/div/div[4]/ng-include/form/div[3]')
                    #     getSelectedPrimers.click()
                    #     downloadPrimerSet = driver.find_element(By.XPATH,'//*[@id="content-view"]/div[1]/div[1]/div/div/div/div/div[6]/ng-include/div[4]/div/div[1]/div[3]/div/div[1]')
                    #     downloadPrimerSet.click()
                    #     #Navigate back to Sequence/first page
                    #     sequencePage = driver.find_element(By.XPATH,'//*[@id="content-view"]/div[1]/div[1]/div/div/div/ul/li[1]/a')
                    #     sequencePage.click()
                    # else:
                    #     ### Handle Loop Primers Page --- unfinished --- ###
                    #     pass
                    getSelectedPrimers = driver.find_element(
                        By.XPATH, '//*[@id="content-view"]/div[1]/div[1]/div/div/div/div/div[4]/ng-include/form/div[3]')
                    getSelectedPrimers.click()
                    # time.sleep(10)

                    downloadPrimerSet = driver.find_element(
                        By.XPATH, '//*[@id="content-view"]/div[1]/div[1]/div/div/div/div/div[6]/ng-include/div[4]/div/div[1]/div[3]/div/div[1]')
                    downloadPrimerSet.click()
                    # sequenceResults = result(driver)
                    print("Succesfully downloaded primers.")
                    # if sequenceResults == None:
                    #     print(f"\nresultsTable not returning data.\n")
                    # Navigate back to Sequence/first page
                    # sequencePage = driver.find_element(By.XPATH,'//*[@id="content-view"]/div[1]/div[1]/div/div/div/ul/li[1]/a')
                    # sequencePage.click()
                    # time.sleep(10)
                    # return sequenceResults
                except Exception as e:
                    logging.exception("Error trying to download primers file.")
                    raise

        except Exception as e:
            logging.exception(f"Error while selecting primers: {e}")
            raise
        finally:
            # Navigate back to first page
            try:
                sequencePage = driver.find_element(
                    By.XPATH, '//*[@id="content-view"]/div[1]/div[1]/div/div/div/ul/li[1]/a')
                sequencePage.click()
            except Exception:
                raise
    except Exception as e:
        # logging.exception(f"Error in processSequence() function: {e}")
        formatException(e)
        raise
