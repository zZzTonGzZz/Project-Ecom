from django.contrib import admin
from .models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User
from django.utils import timezone


# Register the model on the admin section thing
admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)

# Create an OrderItem Inline
class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0

# Extend Our Order Model
class OrderAdmin(admin.ModelAdmin):
    model = Order
    readonly_fields = ["date_ordered"]
    fields = ["user", "full_name", "email", "shipping_address", "amount_paid", "date_ordered", "shipped", "date_shipped"]
    inlines = [OrderItemInline]

# Unregister Order Model
admin.site.unregister(Order)

# Re-Register our Order And OrderAdmin
admin.site.register(Order, OrderAdmin)