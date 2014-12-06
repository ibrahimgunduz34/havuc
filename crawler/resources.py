from crawler.exceptions import ParseError
from lxml import html as parser
from urlparse import urlparse


class BaseResource(object):
	def __init__(self, url):
		self.url = url
		self.price = 0
		self.currency = None
		self.image_url = 0
		self.document = None

	def prepare_document(self, content):
		try:
			self.document = parser.fromstring(content)
		except:
			raise ParseError('Error occured while parsing '
							 'content. Url: %s' % self.url)
		self.parse_price()
		self.parse_currency()
		self.parse_image_url()

	def get_document(self):
		return self.document

	def get_items(self, xpath):
		return self.document.xpath(xpath)

	def get_item(self, xpath):
		return self.get_items(xpath)[0]

	def get_node_value(self, xpath):
		return self.get_item(xpath).text

	def get_attribute_value(self, xpath, attr):
		return self.get_item(xpath).get(attr)

	def get_url(self):
		return self.url

	def get_base_url(self):
		parsed_url = urlparse(self.url)
		return '%s://%s' % (parsed_url.scheme, parsed_url.hostname)

	def parse_price(self):
		raise NotImplemented()

	def parse_image_url(self):
		raise NotImplemented()

	def parse_currency(self):
		raise NotImplemented()

	def get_price(self):
		return self.price

	def get_currency(self):
		return self.currency

	def get_image_url(self):
		return self.image_url


class VatanBilgisayarResource(BaseResource):
	def parse_price(self):
		xpath = '//*[@id="ctl00_u14_ascUrunDetay_dtUrunD' \
				'etay_ctl00_lblSatisFiyat"]'
		self.price = self.get_node_value(xpath)

	def parse_currency(self):
		self.currency = 'TRL'

	def parse_image_url(self):
		xpath = '//*[@class="slider"]/li[1]/a/img';
		self.image_url = '%s%s' % (self.get_base_url(),
								   self.get_attribute_value(xpath, 'src'))


