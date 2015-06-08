import eventlet
from eventlet.green import urllib2
import csv
import time 
import sys
import os

if len(sys.argv) > 1:
  file_path = sys.argv[1]
  directory_to_save = sys.argv[2]
else:
  #file_path = '/Users/myazdaniUCSD/Documents/twitter_data_grant/data/results_sample.csv'
  file_path = '../../data/all_tweets/all_links/results.csv'
  #directory_to_save = '/Users/myazdaniUCSD/Documents/twitter_data_grant/data/sample_tweets/'
  directory_to_save = '../../data/all_tweets/'



def return_rows(filename, file_encoding = 'rU'):
  with open(filename, file_encoding) as f: 
    reader = csv.reader(f, delimiter='\t', quotechar="'")
    rowsInData = [row for row in reader]
  return rowsInData 



file_urls = return_rows(file_path)
#file_urls = file_urls[-1000:]

start_time = time.time()

def fetch(file_url):
  try:
    url = file_url[1]
    filename = file_url[0]
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