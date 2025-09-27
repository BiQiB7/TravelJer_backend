import requests
import json
from selenium_scraper import scrape_with_scrolling

def test_scrape_api():
    """
    Tests the /scrape endpoint of the scraping service.
    """
    url = "http://localhost:5001/scrape"
    payload = {
        "url": "https://www.reddit.com/r/malaysia/comments/1lpriig/why_is_malaysian_food_so_good_and_filling_and.json",
        "depth": 1,
        # "max_num":1
    }
    headers = {
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # Raise an exception for bad status codes

        print("Status Code:", response.status_code)
        print("Response JSON:", response.json())

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

def test_selenium_scraper():
    """
    Tests the selenium scraper directly.
    """
    # Using a reddit page as an example for infinite scrolling
    target_url = "https://www.reddit.com/r/malaysia/comments/1npvgay/someone_i_knew_who_is_a_religious_and_devout/"
    scraped_data = scrape_with_scrolling(target_url)
    
    if scraped_data:
        print("\n--- Scraped Data ---")
        for item in scraped_data:
            print(item)
        print("--------------------")
    else:
        print("No data was scraped.")

if __name__ == "__main__":
    # You can choose which test to run
    # test_scrape_api()
    test_selenium_scraper()