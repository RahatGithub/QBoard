from django.contrib import admin
from .models import Product, User, Employee, Order


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'total_amount', 'status', 'order_date')
    list_filter = ('status', 'order_date', 'user')
    

admin.site.register(User)
admin.site.register(Employee)
admin.site.register(Product)
admin.site.register(Order, OrderAdmin)