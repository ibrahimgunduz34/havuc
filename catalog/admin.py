from django.contrib import admin

from catalog.models import Product, Resource, ProductResource, \
						   Category

from mptt.admin import MPTTModelAdmin


class ChildCategory(admin.TabularInline):
	model = Category


class CategoryAdmin(MPTTModelAdmin):
	mptt_level_indent = 20
	inlines = [ChildCategory,]


class ProductResourceAdmin(admin.TabularInline):
	model = ProductResource


class ProductAdmin(admin.ModelAdmin):
	inlines = [ProductResourceAdmin,]
	list_display = ['name', 'category']
	readonly_fields = ['admin_detail_image']



class ResourceAdmin(admin.ModelAdmin):
	list_display = ['name', 'admin_image']

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Resource, ResourceAdmin)


