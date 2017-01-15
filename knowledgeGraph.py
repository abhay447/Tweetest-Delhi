import pickle
import json
import urllib2,urllib
import pandas as pd
from spacy.en import English

nlp = English()

api_key = "Your_API_KEY_HERE"
service_url = 'https://kgsearch.googleapis.com/v1/entities:search'

myDict = {}

def search(query):	
	params = {
		'query': query,
		'limit': 1,
		'indent': True,
		'key': api_key,
	}
	url = service_url + '?' + urllib.urlencode(params)
	req = urllib2.Request(url)
	req.add_header('User-Agent','Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0')
	response = urllib2.urlopen(req).read()
	response = json.loads(response)

	try:
		name = desc = response['itemListElement'][0]['result']['name']
		desc = response['itemListElement'][0]['result']['detailedDescription']['articleBody']
		parsedData = nlp(desc)
		actors = []
		for t in parsedData:
			if t.pos_ == 'NOUN':
				actors.append(t.text)
		return actors
	except:
		return []
		print "failed at query : "+query

def strip_non_ascii(string):
    ''' Returns the string without non ASCII characters'''
    stripped = (c for c in string if 0 < ord(c) < 127)
    return ''.join(stripped)

def insertIntoDict(arr):
	for a in arr:
		if a not in myDict:
			myDict[a] = 0
		else:
			myDict[a] = myDict[a]+1
			
def main():
	Tweets = open('DelhiTweets.txt').readlines()
	print "Tweets Loaded ..."
	i = 1
	Fails = open('fails.txt','w')
	while i<=len(Tweets):
		try:
			print Tweets[i-1]
			inText = unicode(strip_non_ascii(Tweets[i-1]),'utf-8')
			print inText
			doc = nlp(inText)
			for nc in doc.noun_chunks:
				insertIntoDict(search(nc.text))
			nouns = []
			for d in doc:
				if d.pos_ == 'NOUN':
					print d.text
					nouns.append(d.text)
			insertIntoDict(nouns)
			print "%1.2f percent complete"%(i*100.0/len(Tweets))			
		except:
			print "failed at line: %i"%i
			Fails.write('%i \n'%i)
		i = i+1
	Fails.close()

if __name__ == '__main__':
	main()
	print myDict
	with open('Result.txt', 'wb') as handle:
		pickle.dump(myDict, handle)
	handle.close()