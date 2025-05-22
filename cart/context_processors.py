from .cart import Cart

<<<<<<< HEAD
# Create context processor so our cart can work on all pages of the site
def cart(request):
    # Return the default data from our cart
=======
# Create context processor so our cart can work on all pages
def cart(request):
    # Return the default data from our Cart
>>>>>>> a16a1ec8b722ec404eeb786f560df4dcfe9a66a2
    return {'cart': Cart(request)}