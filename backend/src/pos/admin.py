from django.contrib import admin
from .models import *

# Register your models here.


class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('cat_name', 'date_updated')


class ProductUnitAdmin(admin.ModelAdmin):
    list_display = ('p_name', 'category')


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'retail_price', 'wholesale_price',
                    'stock_quantity', 'in_stock')
    list_filter = ('in_stock', 'unit_name')
    search_fields = ('name', 'unit_name')


class SaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'issue_date', 'customer_name', 'cashier')

    def save_model(self, request, obj, form, change):
        # If it's a new Sale instance (not being edited)
        if not change:
            obj.cashier = request.user  # Set the cashier to the currently logged-in user
        super().save_model(request, obj, form, change)


class SaleItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity',
                    'get_unit_price_at_sale', 'get_subtotal')
    list_filter = ('product__name',)
    search_fields = ('product__name',)

    def get_unit_price_at_sale(self, obj):
        return obj.unit_price_at_sale

    def get_subtotal(self, obj):
        return obj.subtotal

    # Set column headers for custom methods
    get_unit_price_at_sale.short_description = 'Unit Price at Sale'
    get_subtotal.short_description = 'Subtotal'


admin.site.register(User)
admin.site.register(Product_Category, ProductCategoryAdmin)
admin.site.register(Product_Unit, ProductUnitAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Sale, SaleAdmin)
admin.site.register(SaleItem, SaleItemAdmin)
