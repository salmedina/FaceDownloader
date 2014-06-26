import json
import os
import time
import requests
import urllib
import urllib2
from urlparse import urlparse
from os.path import splitext, basename
from requests.exceptions import ConnectionError

 
def query(query, path):
  """Download full size images from Google image search.
 
  Don't print or republish images without permission.
  I used this to train a learning algorithm.
  """
  BASE_URL = 'https://ajax.googleapis.com/ajax/services/search/images?'\
             'v=1.0&q=' + query + '&start=%d'
 
  BASE_PATH = path
 
  if not os.path.exists(BASE_PATH):
    os.makedirs(BASE_PATH)
 
  start = 0 # Google's start query string parameter for pagination.
  maxQueryIdx = start + 60
  imgIndex = 0
  while start < maxQueryIdx: # Google will only return a max of 56 results.
    r = requests.get(BASE_URL % start)
    for image_info in json.loads(r.text)['responseData']['results']:
      imgIndex += 1
      img_url = image_info['unescapedUrl']
      try:
        urllib2.urlopen(img_url)
      except:
        print 'Could not open %s' % img_url
        continue

      disassembled = urlparse(img_url)
      _, img_ext = splitext(basename(disassembled.path))
      print("%s: %s"%(img_ext, img_url))
      
      try:
        #title = image_info['titleNoFormatting'].encode('ascii', 'ignore').translate(None, "/\\|*?<>:\".")
        if img_ext != '':
          title = "%s_%d"%(query.replace(' ', '_'), imgIndex)
          fileName = os.path.join(BASE_PATH, '%s%s'% (title,img_ext))
          if not os.path.isfile(fileName):
            urllib.urlretrieve(img_url, fileName)
      except IOError, e:
        print 'Could not download %s' % img_url
        continue
 
    print start
    start += 4
 
    # Be nice to Google and they'll be nice back :)
    time.sleep(0.5)
 
# Example use
# query('keanu reeves face', '.\\Data\\Faces')