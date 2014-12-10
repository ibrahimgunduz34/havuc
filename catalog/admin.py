from django.contrib import admin

from catalog.models import (Product, Resource, ProductResource,
                            Category, ProductPrice, ProviderProduct)

from mptt.admin import MPTTModelAdmin


class ChildCategory(admin.TabularInline):
    model = Category


class CategoryAdmin(MPTTModelAdmin):
    mptt_level_indent = 20
    inlines = [ChildCategory, ]


class ProductResourceAdmin(admin.TabularInline):
    model = ProductResource


class ProductPriceAdmin(admin.TabularInline):
    model = ProductPrice
    readonly_fields = ['creation_date']
    ordering = ['-creation_date', 'resource__name', 'price']


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductResourceAdmin, ProductPriceAdmin]
    list_display = ['name', 'category', 'last_price', 'last_currency',
                    'last_check_date', 'last_change_date']
    readonly_fields = ['admin_detail_image']


class ResourceAdmin(admin.ModelAdmin):
    list_display = ['name', 'admin_image']
    prepopulated_fields = {'slug': ('name', )}


class ProviderProductIsMatchedFilter(admin.SimpleListFilter):
    title = 'Is matched ?'
    parameter_name = 'is_matched'

    def lookups(self, request, model_admin):
        return (
            (1, 'Matched'),
            (0, 'Not Matched'),
        )

    def queryset(self, request, queryset):
        if self.value() is not None:
            return queryset.filter(product__isnull=not bool(int(self.value())))


class ProviderProductAdmin(admin.ModelAdmin):
    raw_id_fields = ('product', )
    list_display = ['name', 'resource', 'is_matched']
    list_filter = ['resource', ProviderProductIsMatchedFilter]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Resource, ResourceAdmin)
admin.site.register(ProviderProduct, ProviderProductAdmin)
