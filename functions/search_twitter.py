import os
import requests
from typing import List, Optional, Dict, Any
import json
import time

# It's good practice to load sensitive data from environment variables.
# The user should have a .env file with DATA365_ACCESS_TOKEN="your_token"
# and use a library like python-dotenv to load it.
# For now, I'll use os.environ.get()
ACCESS_TOKEN = os.environ.get("DATA365_ACCESS_TOKEN")

TASK_API_URL = "https://api.data365.co/v1.1/twitter/search/post/update"
RESULTS_API_URL = "https://api.data365.co/v1.1/twitter/search/post/posts"

def create_twitter_search_task(
    keywords: str,
    from_profile: Optional[str] = None,
    to_profile: Optional[str] = None,
    tagged_profile: Optional[str] = None,
    min_faves: Optional[int] = None,
    min_replies: Optional[int] = None,
    min_retweets: Optional[int] = None,
    lang: Optional[str] = None,
    content_filters: Optional[List[str]] = None,
    search_type: str = "top",
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
    max_posts: int = 100,
    load_replies: bool = False,
    max_replies: int = 100,
    callback_url: Optional[str] = None,
    auto_update_interval: Optional[int] = None,
    auto_update_expire_at: Optional[str] = None,
    access_token: Optional[str] = None
) -> Dict[str, Any]:
    """
    Creates a Twitter post search update task using the Data365 API.
    """
    token = access_token or ACCESS_TOKEN
    if not token:
        raise ValueError("Data365 access token is required.")

    params = {
        "access_token": token,
        "keywords": keywords,
        "from_profile": from_profile,
        "to_profile": to_profile,
        "tagged_profile": tagged_profile,
        "min_faves": min_faves,
        "min_replies": min_replies,
        "min_retweets": min_retweets,
        "lang": lang,
        "content_filters": content_filters,
        "search_type": search_type,
        "from_date": from_date,
        "to_date": to_date,
        "max_posts": max_posts,
        "load_replies": load_replies,
        "max_replies": max_replies,
        "callback_url": callback_url,
        "auto_update_interval": auto_update_interval,
        "auto_update_expire_at": auto_update_expire_at,
    }

    params = {k: v for k, v in params.items() if v is not None}

    try:
        response = requests.post(TASK_API_URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        return {"status": "error", "error": f"HTTP error occurred: {http_err}", "data": response.text}
    except requests.exceptions.RequestException as req_err:
        return {"status": "error", "error": f"Request error occurred: {req_err}", "data": None}

def get_twitter_search_status(
    keywords: str,
    from_profile: Optional[str] = None,
    to_profile: Optional[str] = None,
    tagged_profile: Optional[str] = None,
    min_faves: Optional[int] = None,
    min_replies: Optional[int] = None,
    min_retweets: Optional[int] = None,
    lang: Optional[str] = None,
    content_filters: Optional[List[str]] = None,
    search_type: str = "top",
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
    access_token: Optional[str] = None
) -> Dict[str, Any]:
    """
    Gets the status of a Twitter post search task using the Data365 API.
    """
    token = access_token or ACCESS_TOKEN
    if not token:
        raise ValueError("Data365 access token is required.")

    params = {
        "access_token": token,
        "keywords": keywords,
        "from_profile": from_profile,
        "to_profile": to_profile,
        "tagged_profile": tagged_profile,
        "min_faves": min_faves,
        "min_replies": min_replies,
        "min_retweets": min_retweets,
        "lang": lang,
        "content_filters": content_filters,
        "search_type": search_type,
        "from_date": from_date,
        "to_date": to_date,
    }
    params = {k: v for k, v in params.items() if v is not None}

    try:
        response = requests.get(TASK_API_URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        return {"status": "error", "error": f"HTTP error occurred: {http_err}", "data": response.text}
    except requests.exceptions.RequestException as req_err:
        return {"status": "error", "error": f"Request error occurred: {req_err}", "data": None}

def get_twitter_search_results(
    keywords: str,
    from_profile: Optional[str] = None,
    to_profile: Optional[str] = None,
    tagged_profile: Optional[str] = None,
    min_faves: Optional[int] = None,
    min_replies: Optional[int] = None,
    min_retweets: Optional[int] = None,
    content_filters: Optional[List[str]] = None,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
    lang: Optional[str] = None,
    location_name: Optional[str] = None,
    query: Optional[str] = None,
    order_by: Optional[str] = None,
    cursor: Optional[str] = None,
    max_page_size: int = 25,
    access_token: Optional[str] = None
) -> Dict[str, Any]:
    """
    Retrieves cached posts from a Twitter search using the Data365 API.
    """
    token = access_token or ACCESS_TOKEN
    if not token:
        raise ValueError("Data365 access token is required.")

    params = {
        "access_token": token,
        "keywords": keywords,
        "from_profile": from_profile,
        "to_profile": to_profile,
        "tagged_profile": tagged_profile,
        "min_faves": min_faves,
        "min_replies": min_replies,
        "min_retweets": min_retweets,
        "content_filters": content_filters,
        "from_date": from_date,
        "to_date": to_date,
        "lang": lang,
        "location_name": location_name,
        "query": query,
        "order_by": order_by,
        "cursor": cursor,
        "max_page_size": max_page_size,
    }
    params = {k: v for k, v in params.items() if v is not None}

    try:
        response = requests.get(RESULTS_API_URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        return {"status": "error", "error": f"HTTP error occurred: {http_err}", "data": response.text}
    except requests.exceptions.RequestException as req_err:
        return {"status": "error", "error": f"Request error occurred: {req_err}", "data": None}

def poll_for_twitter_search_results(
    search_params: Dict[str, Any],
    poll_interval: int = 5,
    max_attempts: int = 12
) -> Dict[str, Any]:
    """
    Polls the task status and retrieves results when the task is complete.
    """
    status_check_params = {
        key: search_params[key]
        for key in [
            "keywords", "from_profile", "to_profile", "tagged_profile",
            "min_faves", "min_replies", "min_retweets", "lang",
            "content_filters", "search_type", "from_date", "to_date"
        ] if key in search_params
    }

    print("Polling for task completion...")
    for attempt in range(max_attempts):
        status_response = get_twitter_search_status(**status_check_params)
        if status_response.get("status") == "ok":
            task_status = status_response.get("data", {}).get("status")
            print(f"  Attempt {attempt + 1}/{max_attempts}: Task status is '{task_status}'")
            if task_status == "finished":
                print("Task is complete. Fetching results...")
                results_params = {
                    key: search_params[key]
                    for key in [
                        "keywords", "from_profile", "to_profile", "tagged_profile",
                        "min_faves", "min_replies", "min_retweets", "content_filters",
                        "from_date", "to_date", "lang"
                    ] if key in search_params
                }
                return get_twitter_search_results(**results_params)
            elif task_status == "error":
                print("Task failed.")
                return {"status": "error", "error": "Task processing failed.", "data": status_response}
        else:
            print(f"  Attempt {attempt + 1}/{max_attempts}: Could not get task status. Response: {status_response}")

        time.sleep(poll_interval)

    return {"status": "error", "error": "Polling timed out.", "data": None}

if __name__ == '__main__':
    # Example of how to use the function.
    # Before running, set the access token in your environment:
    # export DATA365_ACCESS_TOKEN='your_real_access_token'
    
    if not ACCESS_TOKEN:
        print("Error: The DATA365_ACCESS_TOKEN environment variable is not set.")
        print("Please set it to your Data365 API access token to run this example.")
    else:
        print("Attempting to create a Twitter search task...")
        
        # Define the search parameters
        # "(#python OR #developer) -#job"
        search_params = {
            "keywords":  '("good places to travel in ipoh" OR "best food in ipoh" OR #ipoh)',
            #'("good places to travel in ipoh" OR "best food in ipoh" OR #ipoh)',
            "lang": "en",
            "max_posts": 20,
            "search_type": "top",
            "min_faves":50
        }
        
        print(f"Search parameters:\n{json.dumps(search_params, indent=2)}")
        
        # Call the function to create the task
        creation_result = create_twitter_search_task(**search_params)
        
        print("\n--- Task Creation API Response ---")
        print(json.dumps(creation_result, indent=2))
        
        # Interpret the creation result
        if creation_result and creation_result.get("status") == "accepted":
            task_id = creation_result.get("data", {}).get("task_id")
            print(f"\n[SUCCESS] Task created successfully!")
            print(f"  Task ID: {task_id}")

            # Now, poll for the results
            results = poll_for_twitter_search_results(search_params)
            
            print("\n--- Polling Results ---")
            print(json.dumps(results, indent=2))

            if results and results.get("status") == "ok":
                print("\n[SUCCESS] Successfully retrieved search results.")
            else:
                error_message = results.get("error", "Unknown error during polling.")
                print(f"\n[FAILURE] Did not get results.")
                print(f"  Error: {error_message}")

        else:
            error_message = creation_result.get("error", "Unknown error.")
            print(f"\n[FAILURE] Failed to create task.")
            print(f"  Error: {error_message}")