from apscheduler.schedulers.background import BackgroundScheduler
import time
import random
import subprocess
import sys
import json
import datetime
from mirrorstr.post_note import *
from nostr.key import PrivateKey
from mirrorstr.upload_to_voidcat_and_return_url import *
import requests
from mirrorstr.mp4_to_gif import *
   
TWITTER_HANDLE = ""
NOSTR_PRIVATE_KEY = ""

# print(type(result.stdout))
# repr shows escape characters - searching for \n
# print(repr(result.stdout))

def scrape_and_post(TWITTER_HANDLE, NOSTR_PRIVATE_KEY):
    print('running scrape_and_post. Analyzing last 5 scraped tweets')
    scrape = subprocess.run(['snscrape','--jsonl','-n','5','twitter-user', TWITTER_HANDLE], capture_output=True, text=True)
    json_from_scraper_output = json.loads("["+scrape.stdout.strip().replace("\n",",")+"]")
    # print(json_from_scraper_output)
    with open('tweets.json','r+') as f:
        stored_json = json.load(f)
        for scraped_tweet in json_from_scraper_output:
            if scraped_tweet["inReplyToTweetId"] == None:
                new_tweet = True
                while new_tweet == True:
                    for stored_tweet in stored_json:
                        if scraped_tweet["id"] == stored_tweet["id"]:
                            print('tweet already scraped')
                            new_tweet = False
                    if new_tweet == True:
                        print("new tweet found")
                        # removing //t.co addresses at end of tweet message
                        tweet_message = scraped_tweet["rawContent"]
                        if tweet_message[len(tweet_message)-23:len(tweet_message)-20] == "htt":
                            tweet_message_list = [tweet_message]
                            while tweet_message_list[len(tweet_message_list)-1][len(tweet_message_list[len(tweet_message_list)-1])-23:len(tweet_message_list[len(tweet_message_list)-1])-20] == "htt":
                                tweet_message_list.append(tweet_message_list[len(tweet_message_list)+-1][:len(tweet_message_list[len(tweet_message_list)-1])-23].rstrip())
                            tweet_message = tweet_message_list[len(tweet_message_list)-1]
                        scraped_tweet["rawContent"] = tweet_message

                        if scraped_tweet["media"] != None:
                            print("has image")
                            for media_file in scraped_tweet["media"]:
                                if media_file["_type"] == "snscrape.modules.twitter.Photo":
                                    filetype = media_file["fullUrl"]
                                    filetype = filetype[filetype.find("?format=")+8:]
                                    filetype = filetype[:filetype.find("&")]

                                    downloaded_media = requests.get(media_file["fullUrl"])

                                elif media_file["_type"] == "snscrape.modules.twitter.Gif":
                                    filetype = media_file["variants"][0]["url"]
                                    filetype = filetype[filetype.rfind(".")+1:]

                                    downloaded_media = requests.get(media_file["variants"][0]["url"])

                                elif media_file["_type"] == "snscrape.modules.twitter.Video":
                                    temporary_variant_list = media_file["variants"]
                                    for index, variant in enumerate(temporary_variant_list):
                                        if variant["bitrate"] == None:
                                            temporary_variant_list.pop(index)
                                    temporary_variant_list = sorted(temporary_variant_list, key=lambda d: d['bitrate'], reverse=True)

                                    filetype = temporary_variant_list[0]["url"]
                                    filetype = filetype[:filetype.find("?tag=")]
                                    filetype = filetype[filetype.rfind(".")+1:]

                                    downloaded_media = requests.get(temporary_variant_list[0]["url"])
                                
                                with open("temp."+filetype,'wb') as temp_media_file:
                                    temp_media_file.write(downloaded_media.content)

                                if media_file["_type"] == "snscrape.modules.twitter.Gif":
                                    with open("gifcopy."+filetype,'wb') as temp_media_file:
                                        temp_media_file.write(downloaded_media.content)
                                    mp4_to_gif("temp.mp4", "temp.gif")
                                    filetype = "gif"

                                scraped_tweet["rawContent"] = scraped_tweet["rawContent"]+" "+upload_to_voidcat_and_return_url("temp."+filetype, filetype)

                        stored_json.append(scraped_tweet)
                        f.seek(0)
                        f.write(json.dumps(stored_json, indent=2))
                        post_note(NOSTR_PRIVATE_KEY, scraped_tweet["rawContent"])
                        new_tweet = False
                # print('exited while loop')
            else:
                print('tweet is a reply')

def mirrorstr():
    NOSTR_PRIVATE_KEY = input("Type Nostr nsec private key (enter 'test' to use test key nsec16pejvh2hdkf4rzrpejk93tmvuhaf8pv7eqenevk576492zqy6pfqguu985): ")

    TWITTER_HANDLE = input("Type Twitter handle: ")

    if NOSTR_PRIVATE_KEY == "test":
        NOSTR_PRIVATE_KEY = PrivateKey.from_nsec("nsec16pejvh2hdkf4rzrpejk93tmvuhaf8pv7eqenevk576492zqy6pfqguu985")

    with open('tweets.json','w') as f:
        f.write("[]")

    scrape = subprocess.run(['snscrape','--jsonl','-n','5','twitter-user',TWITTER_HANDLE], capture_output=True, text=True)
    json_from_output = json.loads("["+scrape.stdout.strip().replace("\n",",")+"]")
    json_from_output.reverse()
    with open('tweets.json','r+') as f:
        f.seek(0)
        f.write(json.dumps(json_from_output, indent=2))
    
    scheduler = BackgroundScheduler()
    scheduler.add_job(scrape_and_post, 'interval', seconds=10, args=[TWITTER_HANDLE,NOSTR_PRIVATE_KEY])
    print('\nstarting scheduler')
    scheduler.start()

    while True:
#     with open('tweets.json', 'r') as f:
#         tweets = json.load(f)
#         last_queried_event_datetime = int(datetime.fromisoformat(tweets[len(tweets)-1]['date']).timestamp())
#     # print(f"last queried event datetime {last_queried_event_datetime}")
#     # quit()
#     time.sleep(600)
#     print('closing connections to relays')
#     close_connections(relay_manager)
#     time.sleep(5)
#     print('restarting connection on relay manager')
#     relay_manager = main(public_key.hex(), since=last_queried_event_datetime)
#     print('resuming')
        print('\nkeeping process alive')
        time.sleep(30)

