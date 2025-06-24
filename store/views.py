from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category, Profile, Order
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm, ProductForm
from django.core.paginator import Paginator

from payment.forms import ShippingForm
from payment.models import ShippingAddress

from django import forms
from django.db.models import Q, Count, Sum
import json
from cart.cart import Cart
from datetime import timedelta, datetime
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required, user_passes_test
from payment.models import Order as PaymentOrder, OrderItem
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponseForbidden

def search(request):
	query = request.GET.get('searched', '')
	products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query)) if query else Product.objects.none()

	if query and not products.exists():
		messages.warning(request, "That product does not exist... Please try again.")

	paginator = Paginator(products, 8)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)

	return render(request, "search.html", {
		'searched': page_obj,
		'query': query
})


def update_info(request):
	if request.user.is_authenticated:
		# Get Current User
		current_user = Profile.objects.get(user__id=request.user.id)
		# Get Current User's Shipping Info
		shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
		
		# Get original User Form
		form = UserInfoForm(request.POST or None, instance=current_user)
		# Get User's Shipping Form
		shipping_form = ShippingForm(request.POST or None, instance=shipping_user)		
		if form.is_valid() or shipping_form.is_valid():
			# Save original form
			form.save()
			# Save shipping form
			shipping_form.save()

			messages.success(request, "Your Info Has Been Updated!!")
			return redirect('home')
		return render(request, "update_info.html", {'form':form, 'shipping_form':shipping_form})
	else:
		messages.success(request, "You Must Be Logged In To Access That Page!!")
		return redirect('home')



def update_password(request):
	if request.user.is_authenticated:
		current_user = request.user
		# Did they fill out the form
		if request.method  == 'POST':
			form = ChangePasswordForm(current_user, request.POST)
			# Is the form valid
			if form.is_valid():
				form.save()
				messages.success(request, "Your Password Has Been Updated...")
				login(request, current_user)
				return redirect('update_user')
			else:
				for error in list(form.errors.values()):
					messages.error(request, error)
					return redirect('update_password')
		else:
			form = ChangePasswordForm(current_user)
			return render(request, "update_password.html", {'form':form})
	else:
		messages.success(request, "You Must Be Logged In To View That Page...")
		return redirect('home')
def update_user(request):
	if request.user.is_authenticated:
		current_user = User.objects.get(id=request.user.id)
		user_form = UpdateUserForm(request.POST or None, instance=current_user)

		if user_form.is_valid():
			user_form.save()

			login(request, current_user)
			messages.success(request, "User Has Been Updated!!")
			return redirect('home')
		return render(request, "update_user.html", {'user_form':user_form})
	else:
		messages.success(request, "You Must Be Logged In To Access That Page!!")
		return redirect('home')


def category_summary(request):
	categories = Category.objects.all()
	return render(request, 'category_summary.html', {"categories":categories})	

def category(request, foo):
    foo = foo.replace('-', ' ')

    try:
        category = Category.objects.get(name=foo)

        product_list = Product.objects.filter(category=category)

        paginator = Paginator(product_list, 8)
        page_number = request.GET.get('page')
        products = paginator.get_page(page_number)

        return render(request, 'category.html', {
            'products': products,
            'category': category
        })

    except Category.DoesNotExist:
        messages.error(request, "That category doesn't exist...")
        return redirect('home')


def product(request,pk):
	product = Product.objects.get(id=pk)
	return render(request, 'product.html', {'product':product})

def confirm_delete(request, pk):
    product = get_object_or_404(Product, id=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, f'Product "{product.name}" was deleted successfully...')
        return redirect('home')

    return render(request, 'confirm_delete.html', {'product': product})

def home(request):
    product_list = Product.objects.all()
    paginator = Paginator(product_list, 8)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'home.html', {'products': page_obj})

def about(request):
	return render(request, 'about.html', {})	

def login_user(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)

			# Do some shopping cart stuff
			current_user = Profile.objects.get(user__id=request.user.id)
			# Get their saved cart from database
			saved_cart = current_user.old_cart
			# Convert database string to python dictionary
			if saved_cart:
				# Convert to dictionary using JSON
				converted_cart = json.loads(saved_cart)
				# Add the loaded cart dictionary to our session
				# Get the cart
				cart = Cart(request)
				# Loop thru the cart and add the items from the database
				for key,value in converted_cart.items():
					cart.db_add(product=key, quantity=value)

			messages.success(request, ("You Have Been Logged In!"))
			return redirect('home')
		else:
			messages.success(request, ("There was an error, please try again..."))
			return redirect('login')

	else:
		return render(request, 'login.html', {})


def logout_user(request):
	logout(request)
	messages.success(request, ("You have been logged out...Thanks for stopping by..."))
	return redirect('home')



def register_user(request):
	form = SignUpForm()
	if request.method == "POST":
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			# log in user
			user = authenticate(username=username, password=password)
			login(request, user)
			messages.success(request, ("Username Created - Please Fill Out Your User Info Below..."))
			return redirect('update_info')
		else:
			messages.success(request, ("Whoops! There was a problem Registering, please try again..."))
			return redirect('register')
	else:
		return render(request, 'register.html', {'form':form})
	
def add_item(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully...')
            return redirect('home')
        else:
            messages.error(request, 'Please fix the errors below...')
    else:
        form = ProductForm()
    return render(request, 'add_item.html', {'form': form})

def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    categories = Category.objects.all()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully...')
            return redirect('product', pk=product.pk)
    else:
        form = ProductForm(instance=product)

    return render(request, 'product_update.html', {
        'form': form,
        'product': product,
        'categories': categories
    })

def add_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            Category.objects.create(name=name)
            messages.success(request, "Category saved successfully!")
            return redirect('add_category')
        else:
            messages.error(request, "Please enter a category name.")
    
    return render(request, 'add_category.html')

def is_staff(user):
    return user.is_authenticated and user.is_superuser

@login_required
@user_passes_test(is_staff)
def sales_report(request):
    """Generate comprehensive sales reports"""
    # Date filter parameters
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    # Base queryset
    orders = PaymentOrder.objects.all()
    
    # Apply date filters if provided
    if start_date:
        orders = orders.filter(date_ordered__date__gte=start_date)
    if end_date:
        orders = orders.filter(date_ordered__date__lte=end_date)
    
    # Calculate summary statistics
    total_orders = orders.count()
    total_revenue = orders.aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
    shipped_orders = orders.filter(shipped=True).count()
    pending_orders = orders.filter(shipped=False).count()
    
    # Calculate average order value
    avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
    
    # Get top selling products
    top_products = OrderItem.objects.filter(order__in=orders)\
        .values('product__name', 'product__id')\
        .annotate(total_quantity=Sum('quantity'), total_revenue=Sum('price'))\
        .order_by('-total_quantity')[:10]    # Daily sales for the last 30 days
    thirty_days_ago = now().date() - timedelta(days=29)  # Include today, so 30 days total
    daily_sales = []
    for i in range(30):
        date = thirty_days_ago + timedelta(days=i)
        day_orders = orders.filter(date_ordered__date=date)
        daily_revenue = day_orders.aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
        daily_sales.append({
            'date': date.strftime('%b %d'),  # More readable format
            'orders': day_orders.count(),
            'revenue': float(daily_revenue)
        })
      # Monthly sales for the last 12 months
    monthly_sales = []
    current_date = now().date()
    
    for i in range(12):
        # Calculate the start of each month going backwards
        if i == 0:
            # Current month
            month_start = current_date.replace(day=1)
            month_end = current_date
        else:
            # Previous months
            year = current_date.year
            month = current_date.month - i
            if month <= 0:
                month += 12
                year -= 1
            month_start = current_date.replace(year=year, month=month, day=1)
            # Get last day of the month
            if month == 12:
                month_end = current_date.replace(year=year + 1, month=1, day=1) - timedelta(days=1)
            else:
                month_end = current_date.replace(year=year, month=month + 1, day=1) - timedelta(days=1)
        
        month_orders = orders.filter(date_ordered__date__range=[month_start, month_end])
        monthly_revenue = month_orders.aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
        monthly_sales.append({
            'month': month_start.strftime('%b %Y'),
            'orders': month_orders.count(),
            'revenue': float(monthly_revenue)
        })
    
    monthly_sales.reverse()  # Show oldest to newest
    
    context = {
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'shipped_orders': shipped_orders,
        'pending_orders': pending_orders,
        'avg_order_value': avg_order_value,
        'top_products': top_products,
        'daily_sales': json.dumps(daily_sales, cls=DjangoJSONEncoder),
        'monthly_sales': json.dumps(monthly_sales, cls=DjangoJSONEncoder),
        'start_date': start_date,
        'end_date': end_date,
    }
    
    return render(request, 'sales_report.html', context)

@login_required
@user_passes_test(is_staff)
def order_management(request):
    """Order management dashboard"""
    # Get filter parameters
    status_filter = request.GET.get('status', 'all')
    search_query = request.GET.get('search', '')
    date_filter = request.GET.get('date_filter', 'all')
    
    # Base queryset
    orders = PaymentOrder.objects.all().order_by('-date_ordered')
    
    # Apply filters
    if status_filter == 'shipped':
        orders = orders.filter(shipped=True)
    elif status_filter == 'pending':
        orders = orders.filter(shipped=False)
    
    if search_query:
        orders = orders.filter(
            Q(full_name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(id__icontains=search_query)
        )
    
    if date_filter == 'today':
        orders = orders.filter(date_ordered__date=now().date())
    elif date_filter == 'week':
        week_ago = now().date() - timedelta(days=7)
        orders = orders.filter(date_ordered__date__gte=week_ago)
    elif date_filter == 'month':
        month_ago = now().date() - timedelta(days=30)
        orders = orders.filter(date_ordered__date__gte=month_ago)
    
    # Pagination
    paginator = Paginator(orders, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Order statistics
    stats = {
        'total_orders': PaymentOrder.objects.count(),
        'shipped_orders': PaymentOrder.objects.filter(shipped=True).count(),
        'pending_orders': PaymentOrder.objects.filter(shipped=False).count(),
        'today_orders': PaymentOrder.objects.filter(date_ordered__date=now().date()).count(),
    }
    
    context = {
        'orders': page_obj,
        'stats': stats,
        'status_filter': status_filter,
        'search_query': search_query,
        'date_filter': date_filter,
    }
    
    return render(request, 'order_management.html', context)

@login_required
@user_passes_test(is_staff)
def order_detail(request, order_id):
    """Detailed view of a specific order"""
    order = get_object_or_404(PaymentOrder, id=order_id)
    order_items = OrderItem.objects.filter(order=order)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'ship_order':
            order.shipped = True
            order.date_shipped = now()
            order.save()
            messages.success(request, f'Order #{order.id} has been marked as shipped.')
        elif action == 'unship_order':
            order.shipped = False
            order.date_shipped = None
            # If unshipping, also mark as not delivered
            order.delivered = False
            order.date_delivered = None
            order.save()
            messages.success(request, f'Order #{order.id} has been marked as unshipped.')
        elif action == 'mark_delivered':
            if order.shipped:
                order.delivered = True
                order.date_delivered = now()
                order.save()
                messages.success(request, f'Order #{order.id} has been marked as delivered.')
            else:
                messages.error(request, 'Cannot mark as delivered - order must be shipped first.')
        elif action == 'unmark_delivered':
            order.delivered = False
            order.date_delivered = None
            order.save()
            messages.success(request, f'Order #{order.id} delivery status has been removed.')
        
        return redirect('order_detail', order_id=order.id)
    
    context = {
        'order': order,
        'order_items': order_items,
    }
    
    return render(request, 'order_detail.html', context)

@login_required
@user_passes_test(is_staff)
def bulk_order_actions(request):
    """Handle bulk actions on orders"""
    if request.method == 'POST':
        action = request.POST.get('action')
        order_ids = request.POST.getlist('order_ids')
        
        if not order_ids:
            messages.error(request, 'No orders selected.')
            return redirect('order_management')
        
        orders = PaymentOrder.objects.filter(id__in=order_ids)
        
        if action == 'ship_selected':
            orders.update(shipped=True, date_shipped=now())
            messages.success(request, f'{orders.count()} orders have been marked as shipped.')
        elif action == 'unship_selected':
            orders.update(shipped=False, date_shipped=None)
            messages.success(request, f'{orders.count()} orders have been marked as unshipped.')
        
    return redirect('order_management')

@login_required
@user_passes_test(is_staff)
def sales_report_api(request):
    """API endpoint for sales data (for AJAX requests)"""
    period = request.GET.get('period', 'daily')
    
    if period == 'daily':
        # Last 30 days
        thirty_days_ago = now().date() - timedelta(days=29)
        data = []
        for i in range(30):
            date = thirty_days_ago + timedelta(days=i)
            day_orders = PaymentOrder.objects.filter(date_ordered__date=date)
            data.append({
                'date': date.strftime('%b %d'),
                'orders': day_orders.count(),
                'revenue': float(day_orders.aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0)
            })
    
    elif period == 'monthly':
        # Last 12 months
        data = []
        current_date = now().date()
        for i in range(12):
            if i == 0:
                month_start = current_date.replace(day=1)
                month_end = current_date
            else:
                year = current_date.year
                month = current_date.month - i
                if month <= 0:
                    month += 12
                    year -= 1
                month_start = current_date.replace(year=year, month=month, day=1)
                if month == 12:
                    month_end = current_date.replace(year=year + 1, month=1, day=1) - timedelta(days=1)
                else:
                    month_end = current_date.replace(year=year, month=month + 1, day=1) - timedelta(days=1)
            
            month_orders = PaymentOrder.objects.filter(date_ordered__date__range=[month_start, month_end])
            data.append({
                'month': month_start.strftime('%b %Y'),
                'orders': month_orders.count(),
                'revenue': float(month_orders.aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0)
            })
        data.reverse()
    
    return JsonResponse({'data': data})

@login_required
def my_orders(request):
    """Customer's order history and tracking"""
    if request.user.is_authenticated:
        orders = PaymentOrder.objects.filter(user=request.user).order_by('-date_ordered')
        
        # Pagination
        paginator = Paginator(orders, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = {
            'orders': page_obj,
        }
        
        return render(request, 'my_orders.html', context)
    else:
        messages.error(request, "You must be logged in to view your orders.")
        return redirect('login')

@login_required
def order_tracking(request, order_id):
    """Detailed order tracking for customers"""
    try:
        order = PaymentOrder.objects.get(id=order_id, user=request.user)
        order_items = OrderItem.objects.filter(order=order)
        
        # Handle delivery confirmation
        if request.method == 'POST':
            action = request.POST.get('action')
            if action == 'confirm_delivery' and order.shipped and not order.delivered:
                order.delivered = True
                order.date_delivered = now()
                order.save()
                messages.success(request, 'Thank you for confirming delivery! Your order is now marked as delivered.')
                return redirect('order_tracking', order_id=order.id)
        
        context = {
            'order': order,
            'order_items': order_items,
        }
        
        return render(request, 'order_tracking.html', context)
        
    except PaymentOrder.DoesNotExist:
        messages.error(request, "Order not found or you don't have permission to view this order.")
        return redirect('my_orders')

def order_lookup(request):
    """Allow guests to lookup orders by email and order ID"""
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        email = request.POST.get('email')
        
        try:
            order = PaymentOrder.objects.get(id=order_id, email=email)
            order_items = OrderItem.objects.filter(order=order)
            
            context = {
                'order': order,
                'order_items': order_items,
                'is_guest': True,
            }
            
            return render(request, 'order_tracking.html', context)
            
        except PaymentOrder.DoesNotExist:
            messages.error(request, "Order not found. Please check your order ID and email address.")
            return render(request, 'order_lookup.html')
    
    return render(request, 'order_lookup.html')


# @login_required
# def cancel_order(request, order_id):
#     # One clean lookup
#     try:
#         order = Order.objects.get(id=order_id)
#     except Order.DoesNotExist:
#         messages.error(request, f"Order #{order_id} does not exist.")
#         return redirect('order_management')

#     # Only allow superusers to cancel
#     if not request.user.is_superuser:
#         messages.error(request, "Unauthorized.")
#         return redirect('order_management')  # Change this if your view name differs

#     if request.method == 'POST':
#         # Cancel confirmed
#         if order.status != 'cancelled':
#             order.status = 'cancelled'
#             order.save()
#             messages.success(request, f"Order #{order.id} has been cancelled.")
#         else:
#             messages.warning(request, f"Order #{order.id} is already cancelled.")
#         return redirect('order_management')

#     # Show confirmation page
#     return render(request, 'cancel_order.html', {'order': order})


