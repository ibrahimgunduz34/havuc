from crawler.exceptions import ParseError
from decimal import Decimal
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
		price = self.get_node_value(xpath).replace('.', '')
		try:
			self.price = Decimal(price)
		except ValueError, TypeError:
			self.price = None

	def parse_currency(self):
		self.currency = 'TL'

	def parse_image_url(self):
		xpath = '//*[@class="slider"]/li[1]/a/img';
		self.image_url = '%s%s' % (self.get_base_url(),
								   self.get_attribute_value(xpath, 'src'))


class BimeksResource(BaseResource):
	def parse_price(self):
		thousand_xpath = '//*[@id="ctl00_cphcontent_detay_urun1_FormView_' \
			'Urun_Detay_PanelPrices"]/div[1]/span'
		decimal_xpath = '//*[@id="ctl00_cphcontent_detay_urun1_FormView_' \
			'Urun_Detay_PanelPrices"]/div[1]/span/small'
		thousand_value = self.get_node_value(thousand_xpath)
		decimal_value = self.get_node_value(decimal_xpath).split(' ')[0][1:]
		price = '%s.%s' % (thousand_value, decimal_value)
		try:
			self.price = Decimal(price)
		except ValueError, TypeError:
			self.price = None

	def parse_currency(self):
		xpath = '//*[@id="ctl00_cphcontent_detay_urun1_FormView_' \
			'Urun_Detay_PanelPrices"]/div[1]/span/small'
		self.currency = self.get_node_value(xpath).split(' ')[1]

	def parse_image_url(self):
		xpath = '//*[@id="thumbs"]/ul/li[1]/a'
		self.image_url = self.get_attribute_value(xpath, 'href')


class HepsiBuradaResource(BaseResource):
	def parse_price(self):
		xpath = '//*[@id="ctl00_ContentPlaceHolder1_ProductControl1_' \
			'MainControl1_ProductMain1_lblPriceFirst"]'
		value = self.get_node_value(xpath).split(' ')
		price = value[0].replace('.', '').replace(',', '.')
		currency = value[1]
		try:
			self.price = Decimal(price)
		except ValueError, TypeError:
			self.price = None
		self.currency = currency

	def parse_currency(self):
		pass

	def parse_image_url(self):
		xpath = '//*[@id="ctl00_ContentPlaceHolder1_ProductControl1_' \
			'MainControl1_TabControl1_TabImage1_rptBigImages_ctl00_imgBigImage"]'
		self.image_url = self.get_attribute_value(xpath, 'src')


class HizliAlResource(BaseResource):
	def parse_price(self):
		xpath = '//*[@id="content_ProductPrices1_divFiyat"]/span'
		values = self.get_items(xpath)
		if len(values) > 1 and 'ndirim' in values[1].text.encode('utf8'):
			xpath = '//*[@id="content_ProductPrices1_divFiyat"]/div[2]'
		else:
			xpath = '//*[@id="content_ProductPrices1_divFiyat"]/div'

		price = self.get_node_value(xpath).strip()
		price = price.replace('.', '').replace(',', '.')
		try:
			self.price = Decimal(price)
		except ValueError, TypeError:
			self.price = None

	def parse_currency(self):
		xpath = '//*[@id="content_ProductPrices1_divFiyat"]/span'
		values = self.get_items(xpath)
		if len(values) > 1 and 'ndirim' in values[1].text.encode('utf8'):
			xpath = '//*[@id="content_ProductPrices1_divFiyat"]/div[2]/span'
		else:
			xpath = '//*[@id="content_ProductPrices1_divFiyat"]/div/span'
		self.currency = self.get_node_value(xpath).strip()

	def parse_image_url(self):
		xpath = '//*[@id="imagezoom_thum"]/div/ul/li[1]/a'
		self.image_url = self.get_attribute_value(xpath, 'href')