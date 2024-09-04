#### IGNORE ####

import pandas as pd
from main import inputPrimersCsv

inputPrimersCsv = '/Users/damensavvasavvi/Desktop/sequenceGenerationWebscraper/neb_lamp_preferencesInput.csv'
inputPrimersAndPreferences = pd.read_csv(inputPrimersCsv)
inputPrimersAndPreferences.columns = inputPrimersAndPreferences.columns.str.strip()
sequencesList = inputPrimersAndPreferences['sequence to paste'].to_list()
parameterSet = inputPrimersAndPreferences["Parameter Set"].to_list()
fieldValueColumns = inputPrimersAndPreferences.columns[2:].to_list()
fieldValues = inputPrimersAndPreferences[fieldValueColumns]

print(fieldValueColumns)
print(fieldValues)

## When installing packages run pip install __package__ && pip freeze > requirements.txt
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

inputPrimersCsv = '/Users/damensavvasavvi/Desktop/sequenceGenerationWebscraper/neb_lamp_preferencesInput.csv'
inputPrimersAndPreferences = pd.read_csv(inputPrimersCsv)[::-1]
inputPrimersAndPreferences.columns = inputPrimersAndPreferences.columns.str.strip()
sequencesList = inputPrimersAndPreferences['sequence to paste'].to_list()
parameterSet = inputPrimersAndPreferences["Parameter Set"].to_list()
fieldValueColumns = inputPrimersAndPreferences.columns[2:].to_list()
fieldValues = inputPrimersAndPreferences[fieldValueColumns]

def startUpDriver():
    options = webdriver.ChromeOptions()
    prefs = { "download.default_directory": "/Users/damensavvasavvi/Desktop/sequenceGenerationWebscraper/primerResults"} #Sets directory downloads are saved to
    options.add_experimental_option("prefs",prefs)
    # options.add_argument("--headless")
    options.add_argument("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")
    options.timeouts = { 'script': 10000 ,'implicit': 5000 } #script default = 30000, implicit default = 0: implicit wait sets wait period to wait for each element if not found yet
    driver = webdriver.Chrome(options=options)
    driver.set_script_timeout(45) 
    driver.get("https://lamp.neb.com/#!/")
    handleCookies(driver)
    return driver

def main(indexRec=0):
    primerOutputJsonArray = []
    try:
        driver = startUpDriver()
        while indexRec < len(sequencesList): 
            sequence = sequencesList[indexRec]
            indexRec+=1
            if indexRec%20==0:
                driver.quit()
                startUpDriver()
            try:
                time.sleep(5)
                print(f"\n\n\nStarting generation for sequence {indexRec}\n\n\n")
                index = sequencesList.index(sequence)
                primerOutput = processSequence(driver,sequence,parameterSet[index],fieldValues.iloc[index])
                if primerOutput is not None:
                    primerOutputJsonArray.append(json.loads(primerOutput.to_json(orient='records')))
                else:
                    print(f"Warning: processSequence returned None for sequence {indexRec}")
            except Exception as e:
                print(f"Error while iteratively processing sequences: {e}\n Restarting loop with next sequence.")
                driver.quit()
                main(indexRec)
                print(primerOutputJsonArray)

                continue
    except Exception as e:
        driver.quit()
        main(indexRec)
        print(f"Error while running main(): {e}")
    finally:
        try:
            with open('primerOutput.json','r') as file:
                existing_data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
               existing_data = []
        combined_data = existing_data + primerOutputJsonArray
        try:
            with open('primerOutput.json', 'w') as file:
                json.dump(combined_data, file, indent=4)
        except Exception as e:
            print(f"Error writing primer output json to output file: {e}")
        finally:
            print("final json array: ")
            print(combined_data)
        
        driver.quit()

    

if __name__ == "__main__":
    main()

