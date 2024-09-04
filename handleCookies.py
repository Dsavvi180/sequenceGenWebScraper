from selenium.webdriver.common.by import By
def handleCookies(driver):
    # Handle the cookie pop-up if necessary
    try:
        accept_cookies_button = driver.find_element(By.XPATH, '//button[contains(text(), "Accept")]')
        accept_cookies_button.click()
    except Exception:
        print("No cookies pop-up found or unable to click the 'Accept' button.")
        raise