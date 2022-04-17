#!/usr/bin/python3

'''
NOTES

1.  Scrape the feed and find the entries that match all the key_words list.  This will bring back just the 2022 races in SD
2.  Compare the published date of the race with today's date.  
3.  Check if it's a MotoGP or F1 race
4.  If the dates are the same, check to see if that entry is in the log json file
5.  If not, then grabe the link (add .torrent) and use wget to pull down the torrect according to the config file
'''


import feedparser
from datetime import datetime
import subprocess
import read_json
import update_json
import send_email

RaceFeed = feedparser.parse("https://torrentgalaxy.to/rss?user=48067")
entry = RaceFeed.entries[0]
key_word = ["2022", "Race", "SD"] 
time_now = datetime.now().strftime("%d %b %Y")

print("Today is: " + time_now)
print("\n")


formula1_watch = read_json.output_config()["formula1_watch_directory_base"]
motogp_watch = read_json.output_config()["motogp_watch_directory_base"]


# Scrape the fee and find all the races in SD
for entry in RaceFeed.entries:
    # find all the races that are in SD and from 2022
    if all(word in entry.title for word in key_word):
        
        # check if it's a MotoGP race
        if ("MotoGP" in entry.title):

            # this checks to see if the published date is from today
            if(time_now in entry.published):

                # now we can check if what we have found is in the config file
                if(read_json.output_config()["motogp_title"] != entry.title):
                    update_json.updateJsonFile("motogp_title", entry.title)
                    update_json.updateJsonFile("motogp_update","Yes")
                    # if it's new, use wget to download the file
                    entry.link = entry.link + ".torrent"
                    subprocess.call(["wget",entry.link,"-P",motogp_watch])
                    send_email.send_email("New MotoGP Race", entry.title)
                    update_json.updateJsonFile("motogp_rtorrent_email", "No")
                else:
                    update_json.updateJsonFile("motogp_update","No")
                    update_json.updateJsonFile("last_run",time_now)

            else:
                print("No new MotoGP race yet")
                update_json.updateJsonFile("last_run",time_now)

        if ("Formula.1" in entry.title):
            if(time_now in entry.published):

                if(read_json.output_config()["formula1_title"] != entry.title):
                    update_json.updateJsonFile("formula1_title", entry.title)
                    update_json.updateJsonFile("formula1_update","Yes")
                    # if it's new, use wget to download the file
                    entry.link = entry.link + ".torrent"
                    subprocess.call(["wget",entry.link,"-P",formula1_watch])
                    send_email.send_email("New Formula1 Race", entry.title)
                else:
                    update_json.updateJsonFile("formula1_update","No")
                    update_json.updateJsonFile("last_run",time_now)

            else:
                print("No new F1 race yet")
                update_json.updateJsonFile("last_run",time_now)

