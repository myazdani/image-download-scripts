import eventlet
from eventlet.green import urllib2
import csv
import time 
import sys
import os
import pandas as pd

if len(sys.argv) > 1:
  file_path = sys.argv[1]
  directory_to_save = sys.argv[2]
else:
  #file_path = '/Users/myazdaniUCSD/Documents/twitter_data_grant/data/results_sample.csv'
  file_path = "~/Downloads/Sentiment-polarity-DFE.csv"
  #directory_to_save = '/Users/myazdaniUCSD/Documents/twitter_data_grant/data/sample_tweets/'
  directory_to_save = '~/Desktop/JPGs'


df = pd.read_csv("/Users/myazdaniUCSD/Downloads/Sentiment-polarity-DFE.csv")
file_urls = list(df["imageurl"])

start_time = time.time()

def fetch(file_url):
  try:
    url = file_url
    filename = file_url.split("/")[-1]
    #urllib.urlretrieve(url, directory_to_save+filename)
    
    tweet = urllib2.urlopen(url).read()

    dir = filename[29:42].replace("_", "/")
    dir_to_save = os.path.join(directory_to_save,dir)
    if not os.path.exists(dir_to_save): os.makedirs(dir_to_save)
    output = open(os.path.join(dir_to_save,filename),'wb')
    output.write(tweet)
    output.close()
  except:
    msg = filename + ' failed\n'
    with open("failed_downloads.txt", "a") as myfile: myfile.write(msg)
    return msg


pool = eventlet.GreenPool(size = 5)
start_time = time.time()
success_urls = []
failed_urls = []
for body in pool.imap(fetch, file_urls):
    if body != None: 
        print body
        failed_urls.append(body[0])    
end_time = time.time()

print("Elapsed time was %g seconds" % (end_time - start_time))