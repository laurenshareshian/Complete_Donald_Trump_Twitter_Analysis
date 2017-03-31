These files are compatible with Python 3.  For Python 2 compatibility, see my other [Python 2 Trump twitter repo](https://github.com/laurenshareshian/analyze_donald_trump_twitter_feed).

This code was originally forked from [Leah Culver and Andy Smith's oauth.py code](http://github.com/leah/python-oauth/)
and then [Joe Stump](https://github.com/joestump/python-oauth2)

To use, make a separate file called hidden.py that contains the secret keys you get from Twitter:
``` python
def oauth() :
    return { "consumer_key" : "????", "consumer_secret" : "???", "token_key" : "???", "token_secret" : "???? }
```
Then run get_new_tweets.py to pull approximately 3200 of Donald's latest tweets that are stored in donalddata_new.json.
Then run merge_old_and_new_tweets.py to merge the older tweets contained in donalddata.json with your newer ones.
Then run analyze_merged_tweets.py to plot his twitter usage versus time and to make a plot of a d3 visualization of his most used words.
To see the visualization, open twitterword.htm in a web browser.

To use the Donald Twitter Chat Bot, created using a Markov chain similar to the one described [here](http://stackoverflow.com/questions/5306729/how-do-markov-chain-chatbots-work), run markov.py.

To start the Twitter analysis from scratch instead of merging with the older tweets, use the files contained in the folder get_and_analyze_original_tweets.