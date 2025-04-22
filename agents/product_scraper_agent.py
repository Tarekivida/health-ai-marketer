from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import json
import time
import random
# Developer: This module handles web scraping of product information using Selenium WebDriver.
# Note: This agent uses Selenium for scraping product details.
# Developer: fetch_product_details(url) takes a product URL and returns a dict with title, price, description, and reviews (or an error).
def fetch_product_details(url):
    """Scrapes product details from the given URL using Selenium."""
    print(f"🔍 Initializing WebDriver for {url}")
    options = Options()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-features=NetworkService")
    options.add_argument("--disable-features=VizDisplayCompositor")
    options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        print("✅ WebDriver initialized successfully.")
    except Exception as e:
        print(f"❌ Error initializing WebDriver: {e}")
        return {"error": "WebDriver initialization failed"}
    
    try:
        print(f"🔍 Fetching product page: {url}")
        driver.get(url)
        time.sleep(random.uniform(2, 5))  # Avoid bot detection
        print("✅ Page loaded, extracting product details...")
        
        # Extract product details
        try:
            print("🔍 Extracting title...")
            title = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "product-details__title"))
            ).text.strip()
            print(f"✅ Title extracted: {title}")
        except Exception:
            title = "Title not found"
            print("❌ Title extraction failed.")
        
        try:
            print("🔍 Extracting price...")
            price = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "price__sale"))
            ).text.strip()
            print(f"✅ Price extracted: {price}")
        except Exception:
            price = "Price not found"
            print("❌ Price extraction failed.")
        
        try:
            print("🔍 Extracting description...")
            description_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "product-details"))
            )
            description = "\n".join([p.text.strip() for p in description_element.find_elements(By.TAG_NAME, "p") if p.text.strip()])
            if not description:
                description = "Description not available"
            print(f"✅ Description extracted: {len(description)} characters.")
        except Exception:
            description = "Description not available"
            print("❌ Description extraction failed.")
        
        try:
            print("🔍 Extracting reviews...")
            reviews = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "product-details__reviews__stars__left--average"))
            ).text.strip()
            print(f"✅ Reviews extracted: {reviews}")
        except Exception:
            reviews = "Reviews not found"
            print("❌ Reviews extraction failed.")
        
        print(f"✅ Extraction complete: Title: {title}, Price: {price}, Description Length: {len(description)}, Reviews: {reviews}")
        return {
            "title": title,
            "price": price,
            "description": description,
            "reviews": reviews,
        }
    except Exception as e:
        print(f"❌ Error while scraping {url}: {e}")
        return {"error": str(e)}
    finally:
        driver.quit()