from django.db import models

from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
	name = models.CharField(max_length=50, unique=True)
	parent = TreeForeignKey('self', null=True, blank=True, related_name='children')

	class MPTTMeta:
		order_insertion_by = ['name']

	def __unicode__(self):
		return self.name


class Product(models.Model):
	name = models.CharField(max_length=120)
	category = models.ForeignKey(Category)
	small_description = models.CharField(max_length=255, null=True, blank=True)
	long_description = models.TextField(null=True, blank=True)
	last_price = models.DecimalField(max_digits=7, decimal_places=2,
									 null=True, blank=True)
	last_currency = models.CharField(max_length=3, null=True, blank=True)
	image = models.ImageField(upload_to='product/%Y/%m')
	is_active = models.BooleanField(default=True)
	last_check_date = models.DateTimeField(null=True, blank=True)
	last_change_date = models.DateTimeField(null=True, blank=True)

	def __unicode__(self):
		return self.name

	def admin_detail_image(self):
		return '<img src="%s" height="120"/>' % self.image.url
	admin_detail_image.allow_tags = True


class Resource(models.Model):
	name = models.CharField(max_length=50)
	icon = models.ImageField(upload_to='resources')
	resource_name = models.CharField(max_length=50)
	is_active = models.BooleanField(default=True)

	def admin_image(self):
		return '<img src="%s" height="30"/>' % self.icon.url
	admin_image.allow_tags = True

	def __unicode__(self):
		return self.name


class ProductResource(models.Model):
	product = models.ForeignKey(Product)
	resource = models.ForeignKey(Resource)
	url = models.URLField()
	is_active = models.BooleanField(default=True)


class ProductPrice(models.Model):
	product = models.ForeignKey(Product)
	resource = models.ForeignKey(Resource)
	creation_date = models.DateTimeField(auto_now_add=True)
	price = models.DecimalField(max_digits=7, decimal_places=2)
	currency = models.CharField(max_length=3)
