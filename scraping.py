from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import re


# FUNCTION TO GET POSTS DATA
def get_post_data(driver, post_url, max_retries):
    for attempt in range(max_retries):
        try:
            driver.get(post_url)
            wait = WebDriverWait(driver, 20)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'article')))

            post_soup = BeautifulSoup(driver.page_source, 'html.parser')
            caption_container = post_soup.find('div', {'class': '_a9zs'})

            if caption_container:
                h1_element = caption_container.find('h1')
                if h1_element:
                    caption_text = h1_element.get_text(strip=True, separator=' ')
                else:
                    caption_text = "Caption structure not recognized"
            else:
                caption_text = "No caption"

            hashtags = [tag.get_text() for tag in post_soup.find_all('a') if tag.get_text().startswith('#')]
            return {'caption': caption_text, 'hashtags': hashtags}

        except (TimeoutException, StaleElementReferenceException) as e:
            if attempt < max_retries - 1:
                print(f"Attempt {attempt + 1} failed. Retrying...")
                time.sleep(5)
            else:
                print(f"Error extracting caption after {max_retries} attempts: {e}")
                return {'caption': "Error extracting caption", 'hashtags': []}



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

    
# META DATA COLLECTION
    counts = re.findall(r'(\d[\d,.]*\s*[KM]?)\s*(Followers|Following|Posts)', description)

    follower_count = following_count = post_count = None

    for count, label in counts:
        if label == "Followers":
            follower_count = count
        elif label == "Following":
            following_count = count
        elif label == "Posts":
            post_count = count

    profile_info = description.split('-')[1].strip()

    print(f"Profile Info: {profile_info}")
    print(f"Followers: {follower_count}")
    print(f"Following: {following_count}")
    print(f"Posts: {post_count}")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    driver.quit()