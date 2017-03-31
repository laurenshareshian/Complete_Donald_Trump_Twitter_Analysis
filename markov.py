#Donald Trump Chat Bot
#I wrote this chatbot using this link: http://stackoverflow.com/questions/5306729/how-do-markov-chain-chatbots-work
#This program uses donald's tweets saved in donalddata.json.

import random
import re
import string
import json

#get donald's tweets
with open('donalddata.json') as json_data:
    js = json.load(json_data)

words=[]

for j in range(len(js)):
    line=js[j]['text']

    #clean up tweets by getting rid of hyperlinks and some punctuation and adding spaces after other punctuation
    line = re.sub(r"http\S+", "", line) #remove hyperlinks
    line = re.sub(r"amp\S+", "", line) #remove ampersand symbol
    line = re.sub(r"\t", "", line)  # remove tabs
    line = re.sub(r"\v", "", line)  # remove vertical space
    line = re.sub(r"\r", "", line)  # remove carriage return
    line = re.sub(r"\n", "", line)  # remove new lines
    line = re.sub(r"\(", "", line)  # remove parenthesis
    line = re.sub(r"\)", "", line)  # remove parenthesis
    line = re.sub(r"\.\.\.", "", line)  # remove ...
    line = re.sub(r"\. \. \. ", "", line)  # remove . . .
    line = re.sub(r"\"", "", line)  # remove quotations
    line = re.sub(r"!", "! ", line)  # insert space after !
    line = re.sub(r"\.", ". ", line)  # insert space after .
    line = re.sub(r"\?", "? ", line)  # insert space after .

    for word in line.split(): #store all of Donald's words in a list
        words.append(word)

#get rid of punctuation stored as words
bad_words=['…', '.', '!', '?', ',']
for word in words:
    if word in bad_words:
        words.remove(word)

#create dictionary by generating key/value pairs of phrases of a given length and the words that follow those phrases
word_dict=dict()
num_of_words = 2  # create phrases of length 2

for i in range(len(words)-num_of_words):
    phrase = ' '.join([words[j] for j in range(i, i+num_of_words)])
    if phrase not in word_dict:
        word_dict[phrase]=[words[i+num_of_words]]
    else:
        word_dict[phrase] = word_dict[phrase]+[words[i+num_of_words]]


number_of_tweets=20 #how many tweets do you want to generate?

for i in range(number_of_tweets):
    #pick a random key value to start with
    words = ' '
    starting_phrase = random.choice(list(word_dict.keys()))
    rand_num = random.randint(0, len(word_dict[starting_phrase]) - 1)
    words = ' '.join([starting_phrase.capitalize(), word_dict[starting_phrase][rand_num]])
    starting_phrase =starting_phrase.split()[1] + ' ' + word_dict[starting_phrase][rand_num]

    #run chat_bot
    count = num_of_words

    while len(words) <= 140: #get approximately 140 characters
        try:
            rand_num = random.randint(0, len(word_dict[starting_phrase]) - 1)
            words = ' '.join([words, word_dict[starting_phrase][rand_num]])
            starting_phrase = starting_phrase.split()[1] + ' ' + word_dict[starting_phrase][rand_num]
        except:
            if words[-1] not in string.punctuation: #if we run out of pairs but it isn't the end of a line, make it the end of a sentence.
                words = ''.join([words, '.'])
            starting_phrase = random.choice(list(word_dict.keys())) #generate a new phrase to start a new sentence
            words = ' '.join([words, starting_phrase.capitalize()])

        count=count+1


    #capitalize first letter of every sentence
    p = re.compile(r'(?<=[\.\?!]\s)(\w+)')
    cap = lambda match: match.group().capitalize()
    words=p.sub(cap, words)

    if len(words) > 140: #if your tweet goes beyond 140 characters, delete any sentence fragments
        for m in re.finditer(r"\.|!|\?", words):
            continue
        print('@realDonaldTrump: '+words[0:m.end()]+'\n')

    elif 10 <= len(words) <= 140:
        print('@realDonaldTrump: '+words+'\n')

    else: #don't print tweets less than 10 characters long
        continue

