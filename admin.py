from django.contrib import admin
from .models import Product, Category, Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'category', 'size', 'color')
    list_filter = ('category', 'size', 'color', 'price', 'stock')
    search_fields = ('name', 'category__name', 'description')
    actions = ['mark_as_out_of_stock']

    # custom action to mark products as out of stock
    def mark_as_out_of_stock(self, request, queryset):
        queryset.update(stock=0)
        self.message_user(request, "Selected products marked as out of stock.")
    mark_as_out_of_stock.short_description = "Mark selected products as Out of Stock"

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_count')  # dsisplay category name and product count
    search_fields = ('name',)

    def product_count(self, obj):
        return Product.objects.filter(category=obj).count()  # count products in category
    product_count.short_description = "Number of Products"

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'order_date', 'total_price', 'status', 'address')
    search_fields = ('user__username', 'address', 'status')
    
    def total_price(self, obj):
        return obj.total_amount  # using the total_price property from the Order model
    total_price.short_description = "Total Price"  # display name in the admin panel

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Order, OrderAdmin)
