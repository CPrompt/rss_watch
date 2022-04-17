# rss_watch 

This script monitors the page on torrentgalaxy for the MotoGP and F1 races uploaded by a single user SMcGill1969.

### Process:
What I entended the use for this, was to have a more automated way to see if there was a new race
without having to continually refresh the page.  So in this case, I wanted the script to monitor
the page for me, and if there is a new race, send a text message.  Then, once the race was downloaded
and ready to watch, send a message for notification.

### More in depth:

We are monitoring the rss feed provided by torrentgalaxy that is specified in the initial file (rss\_watch.py)
The script uses BeautifulSoup to scrape the page and look for the link to download the torrent file. The information in the list "key\_words" is set to Races in 2022 that are in SD (standard definition).

The last step is to simply use wget to download the torrent file that is linked.  We specify the directory in the "log/config.json" file for each differnt race.
From there, rtorrent is used to download the file.

Rtorrent can also send notification when a download is complete.  To do this we can simply use a bash file to call the "send\_email.py" script.  That is the reason the call to main
reads the json file so that the name of the race comes through in the text message.

### A bit of manual configs:
First you will need to create a python file called simply "creds.py" and place in the "loginfo" directory.
This is a simple python dictionary in this format, and a sample is in the repo:

```python
login = {
	"fromEmail": "<YOUR EMAIL>",
	"toEmail": "<THE PHONE NUMBER TO SEND THE TEXT>",
	"emailLogin": "<SMTP LOGIN USER>",
	"emailPass": "<SMTP LOGIN PASSWORD>",
	"emailServer": "<SMTP SERVER>",
	"emailPort": "<SMTP SERVER PORT>"												}
```

In the file "log/config.json", you will need to specify the directories you would like the downloads to end up.

```python
"formula1_watch_directory_base": "/path/to/f1/watch/folder"
```

Then I have a cron set to run every 1/2 hour only on Sundays because...that's Race Day!
(i.e. ``*/30 * * * 0 python3 /path/to/scrtip/rss_watch.py``)

