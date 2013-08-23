# a very simple web crawler to get random sentences from wikipedia

import Queue, urllib2, cookielib, re, threading

class Crawler(object) :
	def __init__(self) :

		# HTTP request headers to mimick a browser
		self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
			'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
			'Accept-Encoding': 'none',
			'Accept-Language': 'en-US,en;q=0.8',
			'Connection': 'keep-alive'}

		self.threads = []

	# loads a page and returns it's contents
	# if a callback is specified, pass the page contents to the callback
	def load(self,url,callback=None) :
		req = urllib2.Request(url, headers=self.headers)
		try:
			page = urllib2.urlopen(req)
			if callback :
				callback(page.read())
			return page.read()
		except urllib2.HTTPError, e:
			pass

	# loads page as a new thread
	def load_threaded(self,url,callback=None) :
		t = threading.Thread(target=self.load, args = (url,callback) )
		# t.daemon = True
		t.start()

if __name__ == '__main__': 

	# f = open('dataset/sentences.list', 'r+')

	# get a random page from the simple english wikipedia.
	# we use the simple english wiki in order to increase the 
	# probability that the words will match our dictionary

	urls = []
	for i in range(0,12) :
		urls.append("http://simple.wikipedia.org/wiki/Special:Random")

	def action(doc) :
		# find the start of the wiki article
		start = doc.find('<div id="mw-content-text" lang="en" dir="ltr" class="mw-content-ltr">') 

		if start != -1 :
			startp = doc.find('<p>',start)
			endp = doc.find('</p>',startp)
			p = doc[startp:endp]
			pattern = re.compile( '<.*?>')
			formatted =  pattern.sub( '', p)
			pattern2 = re.compile( '^(.*?)\.')
			m = pattern2.match( formatted )
			if m :
				sentence = m.group()
				if len(sentence) > 25 :
					# f.write(sentence + '\n')
					# count = count + 1
					print sentence

	crawler = Crawler()

	for url in urls  :
		crawler.load_threaded(url,action)

	# thread.start_new_thread(crawler.load(site,action))
