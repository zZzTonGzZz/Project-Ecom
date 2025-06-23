"""
Sample data creation script for testing Sales Report and Order Management features.
Run this in Django shell: python manage.py shell < create_sample_data.py
"""

from django.contrib.auth.models import User
from store.models import Product, Category, Profile
from payment.models import ShippingAddress, Order, OrderItem
from django.utils.timezone import now
from decimal import Decimal
import random
from datetime import timedelta

# Create superuser if doesn't exist
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("Created superuser: admin/admin123")

# Create some categories
categories_data = ['Electronics', 'Clothing', 'Books', 'Home & Garden']
categories = []
for cat_name in categories_data:
    category, created = Category.objects.get_or_create(name=cat_name)
    categories.append(category)
    if created:
        print(f"Created category: {cat_name}")

# Create some products
products_data = [
    {'name': 'Smartphone', 'price': 299.99, 'category': 'Electronics'},
    {'name': 'Laptop', 'price': 899.99, 'category': 'Electronics'},
    {'name': 'T-Shirt', 'price': 19.99, 'category': 'Clothing'},
    {'name': 'Jeans', 'price': 49.99, 'category': 'Clothing'},
    {'name': 'Python Programming Book', 'price': 34.99, 'category': 'Books'},
    {'name': 'Garden Tools Set', 'price': 79.99, 'category': 'Home & Garden'},
]

products = []
for prod_data in products_data:
    category = Category.objects.get(name=prod_data['category'])
    product, created = Product.objects.get_or_create(
        name=prod_data['name'],
        defaults={
            'price': prod_data['price'],
            'category': category,
            'description': f"Description for {prod_data['name']}",
            'quantity': random.randint(10, 100)
        }
    )
    products.append(product)
    if created:
        print(f"Created product: {prod_data['name']}")

# Create some test users
for i in range(5):
    username = f'customer{i+1}'
    if not User.objects.filter(username=username).exists():
        user = User.objects.create_user(
            username=username,
            email=f'customer{i+1}@example.com',
            password='password123',
            first_name=f'Customer{i+1}',
            last_name='User'
        )
        print(f"Created user: {username}")

# Create sample orders from the last 30 days
users = User.objects.filter(username__startswith='customer')
for i in range(20):  # Create 20 sample orders
    # Random date within last 30 days
    days_ago = random.randint(0, 30)
    order_date = now() - timedelta(days=days_ago)
    
    user = random.choice(users) if random.choice([True, False]) else None
    
    # Create order
    order = Order.objects.create(
        user=user,
        full_name=f"{user.first_name} {user.last_name}" if user else f"Guest Customer {i+1}",
        email=user.email if user else f"guest{i+1}@example.com",
        shipping_address=f"123 Test Street\nCity, State 12345\nCountry",
        amount_paid=Decimal('0.00'),  # Will be calculated
        shipped=random.choice([True, False]),
        date_ordered=order_date
    )
    
    if order.shipped:
        order.date_shipped = order_date + timedelta(days=random.randint(1, 5))
        order.save()
    
    # Add 1-4 random items to order
    total_amount = Decimal('0.00')
    num_items = random.randint(1, 4)
    
    for _ in range(num_items):
        product = random.choice(products)
        quantity = random.randint(1, 3)
        price = product.price * Decimal(str(random.uniform(0.8, 1.2)))  # Small price variation
        
        OrderItem.objects.create(
            order=order,
            product=product,
            user=user,
            quantity=quantity,
            price=price
        )
        
        total_amount += price * Decimal(str(quantity))
    
    # Update order total
    order.amount_paid = total_amount
    order.save()
    
    print(f"Created order #{order.id} with {num_items} items - Total: ${total_amount:.2f}")

print("\nSample data creation completed!")
print("You can now test the Sales Report and Order Management features.")
print("Access them through the admin navigation menu after logging in as admin.")
