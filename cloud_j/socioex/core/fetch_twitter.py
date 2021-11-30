import tweepy
import json
import xml.etree.ElementTree as ET
import re
from variables import CONFIG

TAG_RE = re.compile(r'<[^>]+>')

consumer_key = CONFIG["TWITTER_CONSUMER_KEY"]
consumer_secret = CONFIG["TWITTER_CONSUMER_SECRET"]
access_key = CONFIG["TWITTER_ACCESS_KEY"]
access_secret = CONFIG["TWITTER_ACCESS_SECRET"]

auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
auth.set_access_token(access_key, access_secret) 

# langs = {'ar': 'Arabic', 'bg': 'Bulgarian', 'ca': 'Catalan', 'cs': 'Czech', 'da': 'Danish', 'de': 'German', 'el': 'Greek', 'en': 'English', 'es': 'Spanish', 'et': 'Estonian',
#         'fa': 'Persian', 'fi': 'Finnish', 'fr': 'French', 'hi': 'Hindi', 'hr': 'Croatian', 'hu': 'Hungarian', 'id': 'Indonesian', 'is': 'Icelandic', 'it': 'Italian', 'iw': 'Hebrew',
#         'ja': 'Japanese', 'ko': 'Korean', 'lt': 'Lithuanian', 'lv': 'Latvian', 'ms': 'Malay', 'nl': 'Dutch', 'no': 'Norwegian', 'pl': 'Polish', 'pt': 'Portuguese', 'ro': 'Romanian',
#         'ru': 'Russian', 'sk': 'Slovak', 'sl': 'Slovenian', 'sr': 'Serbian', 'sv': 'Swedish', 'th': 'Thai', 'tl': 'Filipino', 'tr': 'Turkish', 'uk': 'Ukrainian', 'ur': 'Urdu',
#         'vi': 'Vietnamese', 'zh_CN': 'Chinese (simplified)', 'zh_TW': 'Chinese (traditional)','und':'Undetermined'}

def get_tweets(username): 
    data = []

    api = tweepy.API(auth) 

    tweets = api.user_timeline(screen_name=username) 
    
    for tweet in tweets:
        temp_data = {
            "text": tweet.text,
            "time": str(tweet.created_at).split()[0],
        }
            
        media = tweet.entities.get('media', [])
        
        if(len(media) > 0):
            temp_data["image"] = media[0]['media_url'] 
        else:
            temp_data["image"] = None
        
        pre_lang = str(tweet.lang)
        if pre_lang == "et":
            pre_lang="en"
        
        status = tweet
        json_str = json.dumps(status._json)
        
        if 'extended_entities' in json_str and 'video_info' in json_str:
            temp_data["video"] = tweet.extended_entities['media'][0]['video_info']['variants'][0]['url']
        else:
            temp_data["video"] = None
    
        data.append(temp_data)
    return data