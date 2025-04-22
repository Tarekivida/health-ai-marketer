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

def scrape_product_page(url):
    """Scrapes product details from the given URL using Selenium."""
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
    except Exception as e:
        print(f"❌ Error initializing WebDriver: {e}")
        return {"error": "WebDriver initialization failed"}
    
    try:
        driver.get(url)
        time.sleep(random.uniform(2, 5))  # Avoid bot detection
        
        # Extract product details
        try:
            title = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "product-details__title"))
            ).text.strip()
        except Exception:
            title = "Title not found"
        
        try:
            price = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "price__sale"))
            ).text.strip()
        except Exception:
            price = "Price not found"
        
        try:
            description_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "product-details"))
            )
            description = "\n".join([p.text.strip() for p in description_element.find_elements(By.TAG_NAME, "p") if p.text.strip()])
            if not description:
                description = "Description not available"
        except Exception:
            description = "Description not available"
        
        try:
            reviews = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "product-details__reviews__stars__left--average"))
            ).text.strip()
        except Exception:
            reviews = "Reviews not found"
        
        return {
            "title": title,
            "price": price,
            "description": description,
            "reviews": reviews,
        }
    except Exception as e:
        return {"error": str(e)}
    finally:
        driver.quit()

def test_scraper():
    """Tests the scraper with dummy product URLs."""

    # Dummy data simulating product research agent output
    dummy_data = {
        "Suppléments en vitamine C, E et B": [
            {
                "name": "ixX Pharma B-ixX Complexe De Vitamines B 90 Comprimés",
                "url": "https://www.newpharma.be/pharmacie/ixx-pharma/839845/ixx-pharma-b-ixx-complexe-de-vitamines-b-90-comprimes.html"
            },
            {
                "name": "Physalis Multivit A-Z 12 Vitamines Et 9 Minéraux 45 Comprimés",
                "url": "https://www.newpharma.be/pharmacie/physalis/661445/physalis-multivit-a-z-12-vitamines-et-9-mineraux-45-comprimes.html"
            }
        ]
    }

    print("🔍 Running Scraper Test...")
    scraped_results = {}

    for category, products in dummy_data.items():
        scraped_results[category] = []
        for product in products:
            print(f"🔍 Scraping product: {product['name']} ({product['url']})")
            scraped_data = scrape_product_page(product["url"])
            scraped_results[category].append(scraped_data)

    print("\n✅ Scraper Test Completed! Results:")
    print(json.dumps(scraped_results, indent=4, ensure_ascii=False))

if __name__ == "__main__":
    test_scraper()
