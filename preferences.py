from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import time
import pandas as pd
from typing import Dict, Tuple
sequencePreferences = Dict[str, Tuple[str, int]]
import logging

# Configure the logging settings
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

fields:sequencePreferences = {
    "Na+ concentration": ('//*[@id="condition_sodium"]',"170"),
    "Mg++ concentration":('//*[@id="condition_magnesium"]',"8"),
    "F1c/B1c Length Min": ("//*[@id='content-view']/div[1]/div[1]/div/div/div/div/div[2]/ng-include/form/div[1]/div[1]/div[7]/div[3]/input[1]", "20"),
    "F1c/B1c Length Max": ("//*[@id='content-view']/div[1]/div[1]/div/div/div/div/div[2]/ng-include/form/div[1]/div[1]/div[7]/div[3]/input[2]", "22"),
    "F2/B2 Length Min": ("//*[@id='content-view']/div[1]/div[1]/div/div/div/div/div[2]/ng-include/form/div[1]/div[1]/div[8]/div[3]/input[1]", "18"),
    "F2/B2 Length Max": ("//*[@id='content-view']/div[1]/div[1]/div/div/div/div/div[2]/ng-include/form/div[1]/div[1]/div[8]/div[3]/input[2]", "20"),
    "F3/B3 Length Min": ("//*[@id='content-view']/div[1]/div[1]/div/div/div/div/div[2]/ng-include/form/div[1]/div[1]/div[9]/div[3]/input[1]", "18"),
    "F3/B3 Length Max": ("//*[@id='content-view']/div[1]/div[1]/div/div/div/div/div[2]/ng-include/form/div[1]/div[1]/div[9]/div[3]/input[2]", "20"),
    "LF/LB Length Min": ("//*[@id='content-view']/div[1]/div[1]/div/div/div/div/div[2]/ng-include/form/div[1]/div[1]/div[10]/div[3]/input[1]", "15"),
    "LF/LB Length Max": ("//*[@id='content-view']/div[1]/div[1]/div/div/div/div/div[2]/ng-include/form/div[1]/div[1]/div[10]/div[3]/input[2]", "25"),
    "F1c/B1c Tm Min": ("//*[@id='content-view']/div[1]/div[1]/div/div/div/div/div[2]/ng-include/form/div[1]/div[1]/div[11]/div[3]/input[1]", "64"),
    "F1c/B1c Tm Max": ("//*[@id='content-view']/div[1]/div[1]/div/div/div/div/div[2]/ng-include/form/div[1]/div[1]/div[11]/div[3]/input[2]", "66"),
    "F2/B2 Tm Min": ("//*[@id='content-view']/div[1]/div[1]/div/div/div/div/div[2]/ng-include/form/div[1]/div[1]/div[12]/div[3]/input[1]", "59"),
    "F2/B2 Tm Max": ("//*[@id='content-view']/div[1]/div[1]/div/div/div/div/div[2]/ng-include/form/div[1]/div[1]/div[12]/div[3]/input[2]", "61"),
    "F3/B3 Tm Min": ("//*[@id='content-view']/div[1]/div[1]/div/div/div/div/div[2]/ng-include/form/div[1]/div[1]/div[13]/div[3]/input[1]", "59"),
    "F3/B3 Tm Max": ("//*[@id='content-view']/div[1]/div[1]/div/div/div/div/div[2]/ng-include/form/div[1]/div[1]/div[13]/div[3]/input[2]", "61"),
    "LF/LB Tm Min": ("//*[@id='content-view']/div[1]/div[1]/div/div/div/div/div[2]/ng-include/form/div[1]/div[1]/div[14]/div[3]/input[1]", "64"),
    "LF/LB Tm Max": ("//*[@id='content-view']/div[1]/div[1]/div/div/div/div/div[2]/ng-include/form/div[1]/div[1]/div[14]/div[3]/input[2]", "66"),
    "GC Min": ("//*[@id='content-view']/div[1]/div[1]/div/div/div/div/div[2]/ng-include/form/div[1]/div[1]/div[15]/div[3]/input[1]", "40"),
    "GC Max": ("//*[@id='content-view']/div[1]/div[1]/div/div/div/div/div[2]/ng-include/form/div[1]/div[1]/div[15]/div[3]/input[2]", "65"),
    "GC Min (Loop)": ("//*[@id='content-view']/div[1]/div[1]/div/div/div/div/div[2]/ng-include/form/div[1]/div[1]/div[16]/div[3]/input[1]", "40"),
    "GC Max (Loop)": ("//*[@id='content-view']/div[1]/div[1]/div/div/div/div/div[2]/ng-include/form/div[1]/div[1]/div[16]/div[3]/input[2]", "65"),
    "ΔG threshold 5′ Stability": ("//*[@id='content-view']/div[1]/div[1]/div/div/div/div/div[2]/ng-include/form/div[1]/div[1]/div[17]/div[3]/input", "-4"),
    "ΔG threshold 3′ Stability": ("//*[@id='content-view']/div[1]/div[1]/div/div/div/div/div[2]/ng-include/form/div[1]/div[1]/div[18]/div[3]/input", "-4"),
    "ΔG threshold 3′ Stability (Loop)": ("//*[@id='content-view']/div[1]/div[1]/div/div/div/div/div[2]/ng-include/form/div[1]/div[1]/div[19]/div[3]/input", "-2.0"),
    "Dimer check": ("//*[@id='content-view']/div[1]/div[1]/div/div/div/div/div[2]/ng-include/form/div[1]/div[1]/div[20]/div[3]/input", "-2.5"),
    "Dimer check (Loop)": ("//*[@id='content-view']/div[1]/div[1]/div/div/div/div/div[2]/ng-include/form/div[1]/div[1]/div[21]/div[3]/input", "-3.5"),
    "Distances F2-B2 Min": ("//*[@id='content-view']/div[1]/div[1]/div/div/div/div/div[2]/ng-include/form/div[1]/div[1]/div[22]/div[3]/input[1]", "120"),
    "Distances F2-B2 Max": ("//*[@id='content-view']/div[1]/div[1]/div/div/div/div/div[2]/ng-include/form/div[1]/div[1]/div[22]/div[3]/input[2]", "160"),
    "Distances Loop F1c-F2 Min": ("//*[@id='content-view']/div[1]/div[1]/div/div/div/div/div[2]/ng-include/form/div[1]/div[1]/div[23]/div[3]/input[1]", "40"),
    "Distances Loop F1c-F2 Max": ("//*[@id='content-view']/div[1]/div[1]/div/div/div/div/div[2]/ng-include/form/div[1]/div[1]/div[23]/div[3]/input[2]", "60"),
    "Distances F2-F3 Min": ("//*[@id='content-view']/div[1]/div[1]/div/div/div/div/div[2]/ng-include/form/div[1]/div[1]/div[24]/div[3]/input[1]", "0"),
    "Distances F2-F3 Max": ("//*[@id='content-view']/div[1]/div[1]/div/div/div/div/div[2]/ng-include/form/div[1]/div[1]/div[24]/div[3]/input[2]", "60"),
    "Distances F1c-B1c Min": ("//*[@id='content-view']/div[1]/div[1]/div/div/div/div/div[2]/ng-include/form/div[1]/div[1]/div[25]/div[3]/input[1]", "0"),
    "Distances F1c-B1c Max": ("//*[@id='content-view']/div[1]/div[1]/div/div/div/div/div[2]/ng-include/form/div[1]/div[1]/div[25]/div[3]/input[2]", "100"),
    "Limits F1c/B1c": ("//*[@id='content-view']/div[1]/div[1]/div/div/div/div/div[2]/ng-include/form/div[1]/div[1]/div[26]/div[3]/input", "3"),
    "Limits F2/B2": ("//*[@id='content-view']/div[1]/div[1]/div/div/div/div/div[2]/ng-include/form/div[1]/div[1]/div[27]/div[3]/input", "10"),
    "Limits F3/B3": ("//*[@id='content-view']/div[1]/div[1]/div/div/div/div/div[2]/ng-include/form/div[1]/div[1]/div[28]/div[3]/input", "3"),
    "Limits LF/LB": ("//*[@id='content-view']/div[1]/div[1]/div/div/div/div/div[2]/ng-include/form/div[1]/div[1]/div[29]/div[3]/input", "10"),
    "Sets": ("//*[@id='content-view']/div[1]/div[1]/div/div/div/div/div[2]/ng-include/form/div[1]/div[1]/div[30]/div[3]/input", "1000")
}

### This function is responsible for inputting the preference parameters that are passed through to it as an argument when invoked. The "fields" dictionary stores the xpaths of the preferences table ###
def preferences(driver,parameterSet:str,preferenceValues:pd.DataFrame):
    try:
        
        for key,(xpath,value) in fields.items():
            # print(preferenceValues[key])
            value = str(preferenceValues[key]) ##should be a one row dataframe
        # print(fields)

        ### Sorting rule remains unchanged: default - easy
        ### TODO: edit preferences dictionary and update the code to select the relevent sortingRule and resetParameters from the dropdown
        sortingRule = driver.find_element(By.XPATH, '//*[@id="content-view"]/div[1]/div[1]/div/div/div/div/div[2]/ng-include/form/div[1]/div[1]/div[2]/div[2]/select')
        sortingRuleOptions = [option.text for option in Select(sortingRule).options]

        resetParameters = driver.find_element(By.XPATH, '//*[@id="content-view"]/div[1]/div[1]/div/div/div/div/div[2]/ng-include/form/div[1]/div[1]/div[4]/div[2]/select')
        resetParametersOptions = [option.text for option in Select(resetParameters).options]
        Select(resetParameters).select_by_visible_text(parameterSet)

        fieldKeys = list(fields.keys())
        for key, (xpath,value) in fields.items():
            try:
                parameter = driver.find_element(By.XPATH, xpath)
                parameter.clear()
                parameter.click()
                # print(str(int(preferenceValues[key])))
                parameter.send_keys(str(int(preferenceValues[key])))
                if fieldKeys.index(key) == len(fieldKeys)-1:
                    driver.execute_script("arguments[0].blur();", parameter)
            except Exception as e:
                logging.exception(f"Could not input parameter values for {key} due to exception: {e}")
                raise

        saveChanges = driver.find_element(By.XPATH,'//*[@id="content-view"]/div[1]/div[1]/div/div/div/div/div[2]/ng-include/form/div[4]/div/button')
        saveChanges.click()

    except Exception as e:
        logging.exception(f"Exception thrown in Preferences function: {e}")
        raise
