# mirrorstr

### Tool for mirroring Nostr posts on Twitter, and Twitter posts on Nostr

Mirrorstr is a tool for mirroring Nostr and Twitter posts. The application will monitor a user's account on the two platforms and reflect posts from one into the other. Mirrorstr will help users save time and make sure all audiences get access to a their posts.

Under early development.

Pronunciation: MIR-ror-str (first syllable is accented)

Disclaimer: With the recent post-Elon restrictions imposed on the free Twitter API, the app needed a Twitter scraper to be plugged in to monitor Twitter posts, instead of relying on the API. A way to authenticate and post to the Twitter handle without relying on the Twitter API will be implemented as well as well. The Twitter API is mostly unsupported as of now in the free tier, and relying on what will be of the API in the future is a sure source of frustration.

The app is intended to be run locally from the command line.

Libraries:
https://github.com/jeffthibault/python-nostr (and its dependencies)
https://github.com/JustAnotherArchivist/snscrape (and its dependencies)

## Dependency
This project depends on the dev version of snscrape, which is not available on PyPI. One place where you can find it is at: https://github.com/JustAnotherArchivist/snscrape.

You can install it by running the following command:

'''
pip3 install git+https://github.com/JustAnotherArchivist/snscrape.git
'''


# TODO & Timeline

The first functionality to develop will be Twitter => Nostr. It will take less time to develop and I think has higher demand at the moment.

On the other hand, I believe that the Nostr => Twitter functionality is the end-goal for the application. The goal is for users to be on Nostr primarily and to use the application as a time-saver so their Nostr posts get mirrored on Twitter while the migration happens.

### 1 - Twitter => Nostr functionality
[x] Twitter scraper - using the excellent tool by JustAnotherArchivist, snscrape (https://github.com/JustAnotherArchivist/snscrape)<br>
[ ] Parse twitter content after scraping<br>
[x] Nostr posting

### 2 - Mirrorstr config file for Twitter => Nostr
[ ] Select relays to post to<br>
[ ] Add private key directly to config file, or always ask during initialization<br>
[ ] Select monitored Twitter handle

### 3 - Nostr => Twitter
[x] Monitoring Nostr notes from a specific npub<br>
  [ ] More granular Nostr note filtration to avoid replies, download images/videos, and more<br>
[ ] Twitter authentication (free API seems to be restricting this functionality as well)<br>
[ ] Post to Twitter<br>

### 4 - Mirrorstr config file for Nostr => Twitter
[ ] Add npub(s) to monitor<br>
[ ] Select monitored relays<br>
[ ] Authenticate Twitter account<br>


npub1ljraxpufmzjnfdvsw0tq9kwnypctwxus8n9w388uhkd8h73pzzlqgmdzfy / @pleblira