# This script requires 'selenium' and 'webdriver-manager'.
# You can install them using pip:
# pip install selenium webdriver-manager

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def scrape_with_scrolling(url):
    """
    Scrapes data from a URL by scrolling down to load more content.

    Args:
        url (str): The URL to scrape.
    """
    # Set up Selenium WebDriver
    # This will automatically download the correct driver for your Chrome version
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    print("Setting up WebDriver...")
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    except Exception as e:
        print(f"Error setting up WebDriver: {e}")
        print("Please ensure you have Google Chrome installed.")
        return []

    print(f"Navigating to {url}...")
    driver.get(url)

    # Give the page time to load initially
    time.sleep(3)

    # Scroll down to the bottom of the page to load all content
    last_height = driver.execute_script("return document.body.scrollHeight")
    print("Scrolling down to load content...")
    scroll_attempts = 0
    while scroll_attempts < 5: # Add a limit to prevent infinite loops on static pages
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(2)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            scroll_attempts += 1
        else:
            scroll_attempts = 0 # Reset if new content is loaded
        last_height = new_height

    print("Finished scrolling.")

    # --- Placeholder for data extraction ---
    # Replace this with your specific data extraction logic.
    # For example, finding all elements with a certain class name.
    print("Extracting data...")
    data = []
    
    # Add a small delay to ensure title is loaded
    time.sleep(2)
    page_title = driver.title
    data.append(f"Page title: {page_title}")

    # This is an example of how you might extract text from elements.
    # You should inspect the target website to find the correct selectors.
    # For reddit, post titles can be found with a specific selector.
    print("Extracting post titles...")
    elements = driver.find_elements(By.CSS_SELECTOR, "[data-testid='post-title']")
    post_count = 0
    for element in elements:
        if element.text: # Ensure we don't add empty strings
            data.append(element.text)
            post_count += 1
    
    print(f"Found {post_count} post titles.")
    print("Data extracted.")
    # --- End of placeholder ---


    # Clean up
    driver.quit()

    return data

if __name__ == "__main__":
    # Replace with the URL you want to scrape
    # Using a reddit page as an example for infinite scrolling
    target_url = "https://www.reddit.com/r/malaysia/"
    scraped_data = scrape_with_scrolling(target_url)
    
    if scraped_data:
        print("\n--- Scraped Data ---")
        for item in scraped_data:
            print(item)
        print("--------------------")
    else:
        print("No data was scraped.")