import json
import matplotlib
import matplotlib.pyplot as plt
import unicodedata
import sys
import numpy as np
import datetime
import pytz
from dateutil.parser import parse

#get rid of unicode to allow removal of punctuation
tbl = dict.fromkeys(i for i in range(sys.maxunicode) if unicodedata.category(chr(i)).startswith('P'))
def remove_punctuation(text):
    return text.translate(tbl)

with open('donalddata.json') as json_data:
    js = json.load(json_data)

##########################################
#analyze most used words
##########################################

print('donalds most used words:')
counts={}
tweetcount=0
boring_words=['that', 'have', 'there', 'just', 'their', 'were', 'what' , 'with', 'will', 'than', 'about', 'this']
for j in range(len(js)):
    for i in range(len(js[j])):
#        print(i, js[j][i]['text'], js[j][i]['id'],js[j][i]['created_at'] )
        tweetcount=tweetcount+1
        line=remove_punctuation(js[j][i]['text'])
        line = line.lower()
        words = line.split()
        for word in words:
            if len(word)<4 or word in boring_words: #get rid of small and boring words
                continue
            if word not in counts:
                counts[word] = 1
            else:
                counts[word] += 1

lst = list()
for key, val in counts.items():
    try:
        lst.append( (val, str(key) ))
    except:
        continue
    lst.sort(reverse=True)

for i in range(len(lst)):
    if lst[i][0]>10:
        print(lst[i])


print('number of tweets analyzed =', tweetcount)
print('between the dates:', js[0][0]['created_at'], js[len(js)-1][len(js[len(js)-1])-1]['created_at'])


# ##########################################
#plot counts using d3, to view the visualization open the twitterword.htm file in a web browser
# ##########################################
x = sorted(counts, key=counts.get, reverse=True)
highest = None
lowest = None
for k in x[:100]:
    if highest is None or highest < counts[k] :
        highest = counts[k]
    if lowest is None or lowest > counts[k] :
        lowest = counts[k]

# Spread the font sizes across 20-100 based on the count
bigsize = 80
smallsize = 20

fhand = open('donaldwords.js','w')
fhand.write("donaldwords = [")
first = True
for k in x[:100]:
    if not first : fhand.write( ",\n")
    first = False
    size = counts[k]
    size = (size - lowest) / float(highest - lowest)
    size = int((size * bigsize) + smallsize)
    fhand.write("{text: '"+k+"', size: "+str(size)+"}")
fhand.write( "\n];\n")

print ("Output written to donaldwords.js")


# ##########################################
# keep track of what date, time, and day of week he tweeted at
# ##########################################

weekdays=[]
hours=[]
date_list=[]

tz = pytz.timezone('US/Eastern') #convert from UTC time to Eastern Standard Time since Trump is mostly on east coast

for j in range(len(js)):
    for i in range(len(js[j])):
        row=parse(js[j][i]['created_at']).astimezone(tz)
        weekdays.append(row.strftime("%a"))
        hours.append(int(row.strftime("%H")))
        mydate = datetime.datetime.strptime(row.strftime("%d %b %Y"), '%d %b %Y')
        date_list.append(mydate)

# ##########################################
# make a plot of the day versus number of tweets
# ##########################################
#
count_days={}
for day in date_list:
    if day not in count_days:
        count_days[day]=1
    else:
        count_days[day]+=1

days_count=[]
days=[]
for day in count_days:
    days.append(day)
    days_count.append(count_days[day])

print('most tweets per day:', max(days_count), 'on date', days[days_count.index(max(days_count))].date())

plt.figure(1)
plt.subplot(311)

dates = matplotlib.dates.date2num(days)
plt.plot_date(days, days_count)

plt.ylabel('number of tweets per day')
plt.xlabel('month')
plt.title('Trump Twitter Activity')
# ##########################################
# make a plot of the day of the week versus number of tweets
# ##########################################
#
weekday_list=['Mon', 'Tue', 'Wed', "Thu", 'Fri', 'Sat', 'Sun']
weekday_count=[]
for day in weekday_list:
    weekday_count.append(weekdays.count(day))

plt.subplot(312)
y2_pos = np.arange(len(weekday_list))
plt.bar(y2_pos,weekday_count, align='center', alpha=0.5)
plt.xticks(y2_pos,weekday_list)
plt.ylabel('number of tweets')
plt.xlabel('day')


# ##########################################
# make a plot of the hours of the day versus number of tweets
# ##########################################
#
hour_list=np.arange(0,24,1)
hour_count=[]
for hour in hour_list:
    hour_count.append(hours.count(hour))


plt.subplot(313)
y3_pos = np.arange(len(hour_list))
plt.bar(y3_pos,hour_count, align='center', alpha=0.5)
plt.xticks(y3_pos,hour_list)
plt.ylabel('number of tweets')
plt.xlabel('hour in Eastern Standard Time')


plt.show()

