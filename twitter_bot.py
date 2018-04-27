from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
from tweepy import Cursor
import graph
import tweepy
from datetime import datetime, timedelta
from collections import Counter
import re
import string
""" All required libraries that are used in the following code"""

import twitter_credentials      # importing the credentials file containing all twitter credentials

class Authentification():

    def auntenticateApp(self):

        """Authentification of the user account by using OAuthHandler from the tweepy library."""

        auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
        return auth

class Twitterclient():
    def __init__(self,user_name=None):
        self.auth = Authentification().auntenticateApp()    #Using auntenticateApp class to connect the account
        self.twitter_client = API(self.auth)
        self.twitter_user = user_name       #user_name containg the screen_name/user_id of the account of which we wants to fetch tweets.

    def get_tweets(self,time_limit,files):
        result = []         #list to store final output
        marker = 0          #marker to keep track of files to be created to store tweets.
        for companies in self.twitter_user:
            number_of_tweets = 0
            tweets = []         #to store tweets of individual companies
            with open(files[marker],'w') as writing:
                for tweet in Cursor(self.twitter_client.user_timeline,id = companies,tweet_mode="extended").items():    #fetching all tweets
                    #Reading tweets based on the id as the company name  and then writing the text (extended/complete) to 4 different files
                    tweet_text = tweet.full_text
                    date_created = tweet.created_at
                    #Loop break point checking for all posts before the time_limit passed by the user.
                    if date_created < time_limit:
                        break
                    writing.write(tweet_text)
                    number_of_tweets += 1
            result.append(number_of_tweets)
            marker +=1
        return result    #Final result containg tweet count of each company.

class MentionTwitterclient():           #To retrive all mentions of a company.

    def __init__(self,companyName,today):

        self.auth = Authentification().auntenticateApp()
        self.twitter_client = API(self.auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)  #Rate limit parameters. To wait for the sleeping period.
        self.company = companyName      #All companies
        self.today = today          #passing the present date

    def tweetcount(self):

        desired_date = self.today - timedelta(days = 1)    #limited time period recommended so that program can finish within the rate limit range
        result = []
        for companyN in self.company:
            tweetcount = 0
            loopCheck = True
            try:
                while loopCheck == True:
                    for results in Cursor(self.twitter_client.search, q=companyN).items(9999999):       #iterating through all tweets mentioning the company screen_name
                        r_date = results.created_at         #date check paramter
                        if r_date < desired_date:
                            loopCheck = False     #while loop break point
                            break
                        else:
                            tweetcount +=1       #counting tweets of every company sperately.
                result.append(tweetcount)
            except tweepy.TweepError:               #checking error conditions
                print(TweepError.message[0]['code'])    #whenever TweepError is raised twitter response with a error code.
                time.sleep(60 * 1)
        return result


class Calculations():

    def __init__(self,company_name, company_tweets):
        self.name = company_name
        self.c_tweets = company_tweets

    def Rank(self):
        result = []
        for company, number in zip(self.name, self.c_tweets):   #looping both company name and the number of tweets to store than togeter
            output = (number, company)
            result.append(output)

        return sorted(result,reverse = True)        # Ranked result format:- (number of tweets, company name)

class SearchKeywords():

    """To find the count of tweets by a company including a specific word"""

    def __init__(self,company_name,files, keyword):
        self.name  = company_name
        self.file_name = files
        self.wordToBeSearched = keyword

    def CountingWords(self):
        result = []
        marker = 0              #to track company name
        for file_num in self.file_name:
            document_text = open(file_num, 'r')                 #retriving text from each companies tweet_text file.
            text_string = document_text.read().lower()
            cp_data = []
            for keyWord in self.wordToBeSearched:
                match_pattern = re.findall(keyWord, text_string)            #using regular expressions to find the word.
                temp = (self.name[marker], keyWord, len(match_pattern))      #stroing company name, keyword, keyowrd count among all tweets
                cp_data.append(temp)            #stroing different keyword and keyword count of same company
            result.append(cp_data)              #storing all companies result
            marker +=1
        return result

class WordPattern():
    def __init__(self,files):
        self.file_name = files

    def commonHashTags(self):
        result = []
        c = Counter()       # defining a variable of counter class
        for f in self.file_name:
            document_text = open(f, 'r')
            text_string = document_text.read().lower()
            match_pattern = re.findall(r"([#]\w+)\b", text_string)          #Using regular expression to seprate words containing hastags
            c += Counter(match_pattern)
        for word, _ in c.most_common(3):        # Tally occurrences of words in a list
            result.append(word)
        return result

    def commonWords(self, exceptWord):

        """To find the most common word among all companies tweets"""

        result = []
        for file_name in self.file_name:
            with open(file_name) as f:              #Reading all files
                passage = f.read()
            words = re.findall(r'\w+', passage)         #Taking all words in account
            cap_words = [word.upper() for word in words]    #changing all words to lower case
            word_counts = Counter(cap_words)            # Tally occurrences of words in a list
        #return word_counts
        for word in word_counts.most_common(100):
            if word[0] in exceptWord:           #checking the exceptWord list to ignore common words
                pass
            else:
                return word                  #returing the most common word


if __name__ == '__main__':

    today = datetime.today()
    desired_date = today - timedelta(weeks = 4)
    CommonWord = ['WE', 'TO', 'YOU', 'YOUR', 'FOR', 'THE', 'A', 'US', 'WITH', 'THIS', 'PLEASE', 'SORRY', 'DM', 'ARE', 'CAN', 'AND',
 'OUR', 'T', 'HEAR', 'HTTPS', 'CO', 'BE', 'SEND', 'RE', 'ORDER', 'NUMBER', 'S', 'OF', 'ANY', 'INFORMATION', 'IF',
'MORE', 'SO', 'LOOK', 'HAVE', 'STORE', 'IN', 'KOHL', 'IS', 'IT', 'WILL', 'WHAT', 'SHARE', 'THAT', 'ABOUT', 'LIKE',
 'AT', 'SEE', 'WOULD', 'HELP', 'LL', 'TEAM', 'FEEL', 'ON', 'TAKE', 'THERE', 'THANK' ]         #Words to be excluded from Word Pattren.

    toBeSearched = ["@jcpenney","@Macys","@Nordstrom","@Kohls"]             #company names

    keyy = ["cash","reward","discount"]                 #keywords to be searched

    files = ['file1.txt','file2.txt','file3.txt','file4.txt']

    #calling all required functions
    Up_to_4_weeksTweets = Twitterclient(toBeSearched).get_tweets(desired_date,files)
    Ranked_data = Calculations(toBeSearched,Up_to_4_weeksTweets).Rank()

    Number_of_mentions = MentionTwitterclient(toBeSearched,today).tweetcount()
    Ranked_Mentions = Calculations(toBeSearched,Number_of_mentions).Rank()

    Wpattern = WordPattern(files).commonWords(CommonWord)       #finding the word Pattern
    keyy.append(Wpattern[0].lower())            #appending the found pattern to the keyword
    Search = SearchKeywords(toBeSearched,files,keyy).CountingWords()


    # writing result to file 'Result.txt'
    with open('result.txt', 'w') as writing:
        writing.write('Following are the number of tweets posted by respective companies in last 4 weeks:' +'\n')
        writing.write(str(Ranked_data) +'\n' +'\n')
        writing.write('Number of times each company name was mention in last 1 days' + '\n')
        writing.write(str(Ranked_Mentions)+'\n'+'\n')
        writing.write('Number of times keywords (cash, discount, rewards) used by each company'+ '\n')
        writing.write(str(Search) + '\n'+'\n')
        writing.write('Top 1 keyword used among all companies' +'\n')
        writing.write(str(Wpattern))

    #graphing results
    graph.graphData().RankGraph(Ranked_data,'t4weektweet.png')
    graph.graphData().RankGraph(Ranked_Mentions,'t4mention.png')
    graph.graphData().KeyWordsGraph(Search,'keywordcount.png')
