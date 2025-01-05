import time
import uuid
from datetime import datetime

from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config import (COLLECTION_NAME, DB_NAME, MONGODB_URI, TWITTER_EMAIL,
                    TWITTER_PASSWORD, TWITTER_URL, TWITTER_USERNAME)


class TwitterTrendsScraper:
    def __init__(self):
        self.twitter_url = TWITTER_URL
        self.twitter_email = TWITTER_EMAIL
        self.twitter_username = TWITTER_USERNAME
        self.twitter_password = TWITTER_PASSWORD
        
    def get_proxy(self):
        with open('proxies/valid_proxy_list.txt', 'r') as f:
            proxy_list = f.read().split('\n')
            print('Loaded proxy list', len(proxy_list))
        return proxy_list

    def setup_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--disable-notifications')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36")
        return webdriver.Chrome(options=options)

    def scrape(self):
        proxy_list = self.get_proxy()
        
        # Try proxies until one works
        for proxy in proxy_list:
            try:
                ip_address = proxy.split(":")[0]
                print(f"Using proxy: {proxy} with IP: {ip_address}")
                
                driver = self.setup_driver()
                
                try:
                    # Perform scraping
                    self.login_to_twitter(driver)
                    print("Scraping trends...")
                    trends = self.get_trending_topics(driver)
                    print('Trends:', trends)
                    
                    # Store and return results
                    return self.store_trends(trends, ip_address)
                    
                finally:
                    driver.quit()
                    
            except Exception as e:
                print(f"Error with proxy {proxy} : {e}")
                continue
                
        raise Exception("All proxies failed. Unable to scrape trends.")
    def login_to_twitter(self, driver):
        driver.get(TWITTER_URL)
        print(TWITTER_URL)

        wait = WebDriverWait(driver, 20)

        time.sleep(5)

        print("Finding email field...")
        try:
            email_input = wait.until(EC.element_to_be_clickable((
                By.CSS_SELECTOR, 'input[name="text"][autocomplete="username"]'
            )))
            print('Email input field found', email_input)
        except Exception as e:
            print('Email input field not found', e)
            raise Exception(f"Email input field not found: {e}")

        email_input.clear()
        email_input.send_keys(TWITTER_EMAIL)
        print("Email entered", TWITTER_EMAIL, self.twitter_username)
        email_input.send_keys(Keys.RETURN)

        time.sleep(5)

        print("Username entered and submitted")
        print("Finding password field...")
        try:
            password_input = wait.until(EC.element_to_be_clickable((
                By.CSS_SELECTOR, 'input[type="password"][autocomplete="current-password"]'
            )))
        except Exception as e:
            raise Exception(f"Password input field not found: {e}")

        password_input.clear()
        password_input.send_keys(TWITTER_PASSWORD)
        password_input.send_keys(Keys.RETURN)
        time.sleep(5)
        print("Password entered and submitted")
        wait.until(lambda d: "x.com/home" in d.current_url or "twitter.com/home" in d.current_url)
        print("Successfully logged in")

    def get_trending_topics(self, driver):
        wait = WebDriverWait(driver, 20)

        trends_section = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "a[href='/explore/tabs/for-you'][role='link']")))
        print("Found trends section", trends_section)
        
        trends_section.click()
        time.sleep(5)

        trends = wait.until(EC.presence_of_all_elements_located(
            (By.XPATH, '//div[@aria-label="Timeline: Explore"]/div/div[position() >= 1 and position() <= 6]')))
        print("Found trends", trends)
        
        return [trend.text.split('\n')[0] for trend in trends]


    def store_trends(self, trends, proxy_ip):
        try:
            client = MongoClient(MONGODB_URI)
            db = client[DB_NAME]
            collection = db[COLLECTION_NAME]
            
            record = {
                "_id": str(uuid.uuid4()),
                "timestamp": datetime.now(),
                "ip_address": proxy_ip,
                "nameoftrend1": trends[0],
                "nameoftrend2": trends[1],
                "nameoftrend3": trends[2],
                "nameoftrend4": trends[3],
                "nameoftrend5": trends[4]
            }
            
            collection.insert_one(record)
            return record
    
        except Exception as e:
            print(f"Error storing trends: {e}")
            return None