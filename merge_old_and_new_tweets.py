import json

js=[]

#load older tweets
with open('donalddata.json') as json_data1:
    js1 = json.load(json_data1)

#load newer tweets
with open('donalddata_new.json') as json_data2:
    js2 = json.load(json_data2)

#merge both tweets
js.append(js1)
js.append(js2)

#delete duplicates based on creation time
datelist=[]
count=0
dups_removed=[]
for j in range(len(js)):
    for i in range(len(js[j])):
        for k in range(len(js[j][i])):
            date=js[j][i][k]['created_at']
            if date not in datelist: #remove duplicates
                datelist.append(date)
#                print(j, count, js[j][i][k]['text'], js[j][i][k]['id'],js[j][i][k]['created_at'] )
                count = count + 1
                dups_removed.append(js[j][i][k])


print('number of unique tweets:', len(dups_removed))

#update donalddata.json to include all non-duplicate tweets
outfile = open('donalddata.json', 'w')
json.dump(dups_removed, outfile)
outfile.close()
