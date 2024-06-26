import gzip
from collections import defaultdict
from datetime import datetime
import os
import json
import pickle

save_dir_preprocess = os.path.join("server", "data")

def parse(path):
    g = gzip.open(path, 'r')
    for l in g:
        #yield eval(l)
        yield json.loads(l.decode())

countU = defaultdict(lambda: 0)
countP = defaultdict(lambda: 0)
line = 0

# Save the count of each user interactions in `countU` and 
# the count of each product being interacted with in `countP`  

dataset_name = 'All_Beauty'
f = open(os.path.join(save_dir_preprocess, 'UserAndProductInteractionsCount' + dataset_name + '.txt'), 'w')
for l in parse(os.path.join(save_dir_preprocess, dataset_name + '.jsonl.gz')):
    line += 1
    f.write(" ".join([l['user_id'], l['asin'], str(l['timestamp'])]) + ' \n')
    asin = l['asin']
    rev = l['user_id']
    time = l['timestamp']
    countU[rev] += 1
    countP[asin] += 1
f.close()

usermap = dict()
usernum = 0
itemmap = dict()
itemnum = 0
User = dict()

# Reassign user ids and product ids
for l in parse(os.path.join(save_dir_preprocess, dataset_name + '.jsonl.gz')):
    line += 1
    asin = l['asin']
    rev = l['user_id']
    time = l['timestamp']
    if countU[rev] < 5 or countP[asin] < 5:
        continue

    if rev in usermap:
        userid = usermap[rev]
    else:
        usernum += 1
        userid = usernum
        usermap[rev] = userid
        User[userid] = []
    if asin in itemmap:
        itemid = itemmap[asin]
    else:
        itemnum += 1
        itemid = itemnum
        itemmap[asin] = itemid
    User[userid].append([time, itemid])
# sort reviews in User according to time

# Save the mapping between actual ids and reassign ids
with open(os.path.join(save_dir_preprocess, 'UserIdUserIdMap' + dataset_name + '.pkl'), 'wb') as fp:
    pickle.dump(usermap, fp)

with open(os.path.join(save_dir_preprocess, 'ItemIdItemIdMap' + dataset_name + '.pkl'), 'wb') as fp:
    pickle.dump(itemmap, fp)

# Sort each user interaction (an interaction is a list having multiple vectors, each one ) by the timestamp
for userid in User.keys():
    User[userid].sort(key=lambda x: x[0])

with open(os.path.join(save_dir_preprocess, "PreProcessInfo" + dataset_name + '.pkl'), 'wb') as fp:
    pickle.dump({"usernum": usernum, "itemnum": itemnum}, fp)
print(f"Number of users: {usernum}\nNumber of items: {itemnum}")

f = open(os.path.join(save_dir_preprocess, dataset_name + '.txt'), 'w')
for user in User.keys():
    for i in User[user]:
        f.write('%d %d\n' % (user, i[1]))
f.close()
