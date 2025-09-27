import os
import json
import praw
from dotenv import load_dotenv

load_dotenv()

def get_subreddit_topics(reddit, query, limit=5):
    """
    Gets a list of subreddit objects based on a search query.

    Args:
        reddit (praw.Reddit): An authenticated PRAW instance.
        query (str): The search term to find relevant subreddits.
        limit (int, optional): The maximum number of subreddits to return. Defaults to 5.

    Returns:
        list: A list of praw.models.Subreddit objects.
    """
    print(f"Searching for subreddits matching '{query}'...")
    found_subreddits = reddit.subreddits.search(query)
    return [subreddit for i, subreddit in enumerate(found_subreddits) if i < limit]

def get_links_from_subreddit(subreddit, limit=10):
    """
    Gets a list of top post links from a given subreddit.

    Args:
        subreddit (praw.models.Subreddit): The subreddit to get links from.
        limit (int, optional): The maximum number of posts to retrieve. Defaults to 10.

    Returns:
        list: A list of dictionaries, each containing post details.
    """
    print(f"Getting top {limit} links from r/{subreddit.display_name}...")
    posts = []
    # Fetch a larger number of posts to get a better pool for sorting by score.
    for submission in subreddit.hot(limit=50):
        posts.append({
            "title": submission.title,
            "score": submission.score,
            "url": submission.url
        })

    # Sort the collected posts by score in descending order.
    sorted_posts = sorted(posts, key=lambda post: post['score'], reverse=True)

    # Return the top 'limit' posts.
    return sorted_posts[:limit]

def search_reddit_for_links(query, subreddit_limit=5, post_limit=10):
    """
    Searches for subreddits and retrieves top post links from them.

    Args:
        query (str): The search term to find relevant subreddits.
        subreddit_limit (int, optional): The maximum number of subreddits to search. Defaults to 5.
        post_limit (int, optional): The maximum number of posts to retrieve from each subreddit. Defaults to 10.

    Returns:
        str: A JSON string containing the results.
    """
    try:
        # https://github.com/reddit-archive/reddit/wiki/API
        key="PRstrGuFpxrIIaKiFFL0SSz4CKDxvg"
        #os.environ.get('REDDIT_API')
        print(key)
        reddit = praw.Reddit(
            client_id="aZcYTDGSdHga2MV_VLbL8A",
            #"9O1nyv4ufNDcYLEGFuFeCQ",
            client_secret=key,
            user_agent="city-weaver-ai:v0.1 /u/Frosty_Pack2990"
        )
        print("Reddit authentication successful!")

        subreddits = get_subreddit_topics(reddit, query, limit=subreddit_limit)
        print(subreddits)
        
        all_links = {}
        for subreddit in subreddits:
            links = get_links_from_subreddit(subreddit, limit=post_limit)
            all_links[f"r/{subreddit.display_name}"] = links
            
        return json.dumps(all_links, indent=2)

    except Exception as e:
        return json.dumps({"error": f"An error occurred: {e}"}, indent=2)

if __name__ == '__main__':
    # Example usage:
    # Make sure to set the REDDIT_API environment variable before running
    search_query = 'kl food'
    results_json = search_reddit_for_links(search_query, subreddit_limit=3, post_limit=5)
    print(results_json)
# the output example
# {
#   "r/malaysia": [
#     {
#       "title": "A lady was almost knocked down at a pedestrian crossing in KL after Bezza drove through a red light. Glad she's unhurt, it must have been traumatizing.",
#       "score": 1256,
#       "url": "https://v.redd.it/ngi8m1v970rf1"
#     },
#     {
#       "title": "Malaysian Tourists impress Running Man cast in South Korea by successfully solving the game show's mission despite language barrier",
#       "score": 1244,
#       "url": "https://v.redd.it/yif3e3zbwxqf1"
#     },
#     {
#       "title": "Starbucks barista fired for calling tourist \u201cbodoh\u201d",
#       "score": 633,
#       "url": "https://v.redd.it/bhdcpvv3gxqf1"
#     },
#     {
#       "title": "Dumb driver",
#       "score": 623,
#       "url": "https://v.redd.it/bseod6e5k2rf1"
#     },
#     {
#       "title": "Another incident in Malaysia where both vehicles got into an accident right after a toll. Black car driving in a way that expects others to drive around it, and met with a lorry that happens to drive exactly the same way. Is this our new driving culture?",
#       "score": 555,
#       "url": "https://v.redd.it/ph1werg732rf1"
#     }
#   ],
#   "r/KualaLumpur": [
#     {
#       "title": "Kejadian di Epal T-ahlek",
#       "score": 128,
#       "url": "https://v.redd.it/oqyz9ob77bqf1"
#     },
#     {
#       "title": "Scary Grab experience in KL \u2014 warning for other travellers",
#       "score": 107,
#       "url": "https://i.redd.it/qg2p8uzl08rf1.jpeg"
#     },
#     {
#       "title": "Large Plumes of Smoke Clouds from Buildings in Pudu",
#       "score": 47,
#       "url": "https://i.redd.it/iao8h4g060rf1.png"
#     },
#     {
#       "title": "Exchange Student looking for friends!",
#       "score": 27,
#       "url": "https://www.reddit.com/r/KualaLumpur/comments/1nngn2u/exchange_student_looking_for_friends/"       
#     },
#     {
#       "title": "A note on self-promotion and commercial activities",
#       "score": 23,
#       "url": "https://www.reddit.com/r/KualaLumpur/comments/1b7xqsg/a_note_on_selfpromotion_and_commercial_activities/"
#     }
#   ],
#   "r/MalaysianFood": [
#     {
#       "title": "What I cooked as a Malaysian student living abroad pt9",
#       "score": 1261,
#       "url": "https://www.reddit.com/gallery/1nkqo3l"
#     },
#     {
#       "title": "My wife serves me this every morning before work - is this considered healthy and Malay food?",  
#       "score": 435,
#       "url": "https://i.redd.it/77k6r11setqf1.jpeg"
#     },
#     {
#       "title": "Nasi dagang by the Terengganu beach",
#       "score": 260,
#       "url": "https://www.reddit.com/gallery/1nnhm35"
#     },
#     {
#       "title": "Is this safe to eat? (nasi ayam)",
#       "score": 205,
#       "url": "https://i.redd.it/5kih7bk18hqf1.jpeg"
#     },
#     {
#       "title": "Roast Duck and noodles",
#     },
#     {
#       "title": "Nasi dagang by the Terengganu beach",
#       "score": 260,
#       "url": "https://www.reddit.com/gallery/1nnhm35"
#     },
#     {
#       "title": "Is this safe to eat? (nasi ayam)",
#       "score": 205,
#       "url": "https://i.redd.it/5kih7bk18hqf1.jpeg"
#     },
#     {
#       "title": "Roast Duck and noodles",
#       "title": "Is this safe to eat? (nasi ayam)",
#       "score": 205,
#       "url": "https://i.redd.it/5kih7bk18hqf1.jpeg"
#     },
#     {
#       "title": "Roast Duck and noodles",
#       "title": "Roast Duck and noodles",
#       "score": 188,
#       "url": "https://www.reddit.com/gallery/1nmf7xs"
#     }
#   ]
# }
