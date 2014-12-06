from datetime import datetime

from celery import task

from catalog.models import ProductResource, ProductPrice

from crawler.backends import WebCrawler
from crawler.exceptions import ConnectionError, ParseError
from crawler.helpers import load_resource



@task(name="crawler.tasks.crawler_job")
def crawler_job():
	product_resources = ProductResource.objects.filter(
		is_active=True, product__is_active=True)
	for product_resource in product_resources:
		crawle_resource.delay(product_resource)


@task(name="crawler.tasks.crawle_resource")
def crawle_resource(product_resource):

	web_resource = load_resource(product_resource.resource.resource_name)(
		product_resource.url)
	try:
		WebCrawler.crawle_resource(web_resource)
	except (ConnectionError, ParseError):
		raise Exception('Crawler error. Url: %s ' % web_resource.get_url())

	product = product_resource.product
	resource = product_resource.resource

	product.last_check_date = datetime.now()

	try:
		latest_price = ProductPrice.objects.latest('id')
		if latest_price.price == product.last_price and \
				latest_price.currency == product.last_price:
			product.save()
			return False
	except ProductPrice.DoesNotExist:
		pass

	product_price = ProductPrice.objects.create(
		product=product, resource=resource,
		price=web_resource.get_price(),
		currency=web_resource.get_currency())

	product.last_price = product_price.price
	product.last_currency = product_price.currency
	product.last_change_date = datetime.now()
	product.save()

