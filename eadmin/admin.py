from django.contrib import admin
from .models import BookingTable, Product, Brand, Customer

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'price', 'category', 'quantity', 'created_at', 'updated_at')
    search_fields = ['name', 'brand__name', 'category', 'quantity']
    list_filter = ['category', 'brand__name']
    date_hierarchy = 'created_at'
    fields = ('category','brand', 'name', 'price', 'image', 'description', 'quantity') #for ordering fields in add/update



class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ['name']
    date_hierarchy = 'created_at'
    ordering = ['name']

# class BookingAdmin(admin.ModelAdmin):
#     list_display = ('product', 'customer', 'price','created_at')
#     search_fields = ['product__name', 'customer__first_name', 'product__category']
#     list_filter = ['product__category']
#     date_hierarchy = 'created_at'
#     fields = ('product__name', 'customer__first_name','price', 'created_at') 
    
class BookingAdmin(admin.ModelAdmin):
    list_display = ('product', 'get_customer_name', 'price', 'get_order_datetime')

    def get_customer_name(self, obj):
        return obj.customer.first_name + ' ' + obj.customer.last_name if obj.customer else ''
    get_customer_name.short_description = 'Customer Name'
    def get_order_datetime(self, obj):
        return obj.created_at
    get_order_datetime.short_description = 'Order Date and Time'
    
    search_fields = ['product__name', 'customer__first_name', 'product__category']
    list_filter = ['product__category']
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)



admin.site.register(Product, ProductAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(BookingTable, BookingAdmin)

