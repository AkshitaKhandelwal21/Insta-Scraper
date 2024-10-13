from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from bs4 import BeautifulSoup
import time
import re


#MAIN

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
username = 'geeks_for_geeks'
url = f"https://www.instagram.com/{username}"


try:
    driver.get(url)
    time.sleep(5)

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    wait = WebDriverWait(driver, 10)

    description = soup.find('meta', attrs={'name': 'description'})['content']
    # print(description)

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    driver.quit()