
#### IGNORE: NOT IMPLEMENTED ####

from selenium.webdriver.common.by import By
import pandas as pd
from io import StringIO 
### This function retrieves the inner html of the results table and converts it to a pandas dataframe.
### It then converts the dataframe to a json object and writes it to the location specified by json_location
json_location = '/Users/damensavvasavvi/Desktop/sequenceGenerationWebscraper/primerOutput.json'
def resultsTable(driver):
    try:
        results = driver.find_element(By.XPATH,'//*[@id="content-view"]/div[1]/div[1]/div/div/div/div/div[6]/ng-include/div[4]/div/div/div[2]/div/table')
        resultsHtml = results.get_attribute('innerHTML')
        htmlIO = StringIO("<table>"+resultsHtml+"</table>")
        resultsDataFrame = pd.read_html(htmlIO)[0]
        resultsDataFrame = resultsDataFrame.astype(str)
        resultsDataFrame = resultsDataFrame.fillna('', inplace=True)
        # print(resultsDataFrame)
        # resultsDataFrame.to_json(json_location, orient='records')
        return resultsDataFrame
    except Exception as e:
        print(f"Exception raised while trying to convert results table from html to dataframe: {e}")