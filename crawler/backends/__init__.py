import urllib2
from crawler.exceptions import ConnectionError

class WebCrawler(object):
	@classmethod
	def send_request(cls, url):
		try:
			request = urllib2.Request(url, headers={
				'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
							  'AppleWebKit/537.36 (KHTML, like '
							  'Gecko) Chrome/38.0.2125.122 Safari/537.36'
				})
			return urllib2.urlopen(request).read()
		except urllib2.URLError:
			raise ConnectionError('Connection failed. Url: %s' % url)

	@classmethod
	def crawle_resource(cls, resource):
		response = WebCrawler.send_request(resource.get_url())
		resource.prepare_document(response)
		return resource