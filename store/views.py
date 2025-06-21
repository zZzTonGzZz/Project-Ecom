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
from datetime import timedelta
from django.utils.timezone import now

def search(request):
	# Determine if they filled out the form
	if request.method == "POST":
		searched = request.POST['searched']
		# Query The Products DB Model
		searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))
		# Test for null
		if not searched:
			messages.success(request, "That Product Does Not Exist...Please try Again.")
			return render(request, "search.html", {})
		else:
			return render(request, "search.html", {'searched':searched})
	else:
		return render(request, "search.html", {})	


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
    # Replace hyphens with spaces
    foo = foo.replace('-', ' ')

    try:
        # Look up the category
        category = Category.objects.get(name=foo)

        # Filter products by category
        product_list = Product.objects.filter(category=category)

        # Add pagination — 8 per page
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

# def home(request):
# 	products = Product.objects.all()
# 	return render(request, 'home.html', {'products':products})

def home(request):
    product_list = Product.objects.all()
    paginator = Paginator(product_list, 8)  # Show 8 products per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'home.html', {'products': page_obj})

def analytics(request):
	products = Product.objects.all()
	return render(request, 'analytics.html', {'products':products})

def add_item(request):
	products = Product.objects.all()
	return render(request, 'add_item.html', {'products':products})

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


# def order_dashboard(request):
#     today = now().date()
#     last_7_days = [today - timedelta(days=i) for i in range(6, -1, -1)]

#     daily_counts = []
#     for day in last_7_days:
#         count = Order.objects.filter(created_at__date=day).count()
#         daily_counts.append(count)

#     daily_labels = [day.strftime('%b %d') for day in last_7_days]

#     stats = {
#         'total_orders': Order.objects.count(),
#         'pending_orders': Order.objects.filter(status='pending').count(),
#         'processing_orders': Order.objects.filter(status='processing').count(),
#         'shipped_orders': Order.objects.filter(status='shipped').count(),
#         'delivered_orders': Order.objects.filter(status='delivered').count(),
#         'total_revenue': Order.objects.aggregate(total=Sum('total_amount'))['total'] or 0
#     }

#     return render(request, 'admin/order_dashboard.html', {
#         'stats': stats,
#         'daily_labels': json.dumps(daily_labels),
#         'daily_counts': json.dumps(daily_counts),
#     })



