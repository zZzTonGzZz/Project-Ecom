from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse
<<<<<<< HEAD
from django.contrib import messages
=======
>>>>>>> a16a1ec8b722ec404eeb786f560df4dcfe9a66a2

def cart_summary(request):
    # Get the cart
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()
    return render(request, "cart_summary.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals})




<<<<<<< HEAD
def cart_add(request):
=======
def cart_summary(request):
>>>>>>> a16a1ec8b722ec404eeb786f560df4dcfe9a66a2
    # Get the cart
    cart = Cart(request)
    # Test for POST
    if request.POST.get('action') == 'post':
        # Get stuff
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        # Lookup product in DB
        product = get_object_or_404(Product, id=product_id)

<<<<<<< HEAD
        # Save to session
        cart.add(product=product, quantity=product_qty)

        # Get cart quantity
        cart_quantity = cart.__len__()

        # Return response
        # response = JsonResponse({'Product Name: ': product.name})
        response = JsonResponse({'qty': cart_quantity})
        messages.success(request, ("Product Added to Cart..."))
        return response

=======
        # Save to Session
        cart.add(product=product, quantity=product_qty)

        # Get Cart Quantity
        cart_quantity = cart.__len__()

        # Return resonse
        # response = JsonResponse({'Product Name: ': product.name})
        response = JsonResponse({'qty: ': cart_quantity})
        return response


>>>>>>> a16a1ec8b722ec404eeb786f560df4dcfe9a66a2
def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        # Get stuff
        product_id = int(request.POST.get('product_id'))
<<<<<<< HEAD
        # Call delete function in Cart
        cart.delete(product=product_id)

        response = JsonResponse({'product':product_id})
        #return redirect('cart_summary')
        messages.success(request, ("Item Deleted From Shopping Cart..."))
        return response

=======
        # Call delete Function in Cart
        cart.delete(product=product_id)
        
        response = JsonResponse({'product':product_id})
        return response
        #return redirect('cart_summary')
>>>>>>> a16a1ec8b722ec404eeb786f560df4dcfe9a66a2

def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        # Get stuff
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        cart.update(product=product_id, quantity=product_qty)

        response = JsonResponse({'qty':product_qty})
<<<<<<< HEAD
        #return redirect('cart_summary')
        messages.success(request, ("Your Cart has Been Updated..."))
        return response
=======
        return response
        #return redirect('cart_summary')

def cart_add(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        # Get stuff
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        cart.update(product=product_id, quantity=product_qty)

        response = JsonResponse({'qty':product_qty})
        return response
        #return redirect('cart_summary')
>>>>>>> a16a1ec8b722ec404eeb786f560df4dcfe9a66a2
