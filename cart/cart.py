<<<<<<< HEAD
from store.models import Product, Profile
=======
from store.models import Product
>>>>>>> a16a1ec8b722ec404eeb786f560df4dcfe9a66a2

class Cart():
    def __init__(self, request):
        self.session = request.session
<<<<<<< HEAD
        # Get request
        self.request = request
=======

>>>>>>> a16a1ec8b722ec404eeb786f560df4dcfe9a66a2
        # Get the current session key if it exists
        cart = self.session.get('session_key')

        # If the user is new, no session key! Create one!
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

<<<<<<< HEAD

        # Make sure cart is available on all pages of site
        self.cart = cart

    def db_add(self, product, quantity):
        product_id = str(product)
        product_qty = str(quantity)
        # Logic
        if product_id in self.cart:
            pass
        else:
            #self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)

        self.session.modified = True

        # Deal with logged in user
        if self.request.user.is_authenticated:
            # Get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # Convert {'3':1, '2':4} to {"3":1, "2":4}
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # Save carty to the Profile Model
            current_user.update(old_cart=str(carty))


=======
        
        # Make sure cart is available on all pages of site
        self.cart = cart

>>>>>>> a16a1ec8b722ec404eeb786f560df4dcfe9a66a2
    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)
        # Logic
        if product_id in self.cart:
            pass
        else:
            #self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)
<<<<<<< HEAD

        self.session.modified = True

        # Deal with logged in user
        if self.request.user.is_authenticated:
            # Get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # Convert {'3':1, '2':4} to {"3":1, "2":4}
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # Save carty to the Profile Model
            current_user.update(old_cart=str(carty))

=======
        
        self.session.modified = True

>>>>>>> a16a1ec8b722ec404eeb786f560df4dcfe9a66a2
    def cart_total(self):
        # Get product IDS
        product_ids = self.cart.keys()
        # Lookup those keys in our products database model
<<<<<<< HEAD
        products = Product.objects.filter(id__in=product_ids)
=======
        products = Product.object.filter(id__in=product_ids)
>>>>>>> a16a1ec8b722ec404eeb786f560df4dcfe9a66a2
        # Get quantities
        quantities = self.cart
        # Start counting at 0
        total = 0
<<<<<<< HEAD

        for key, value in quantities.items():
            # Convert key string into into so we can do math
            key = int(key)
            for product in products:
                if product.id == key:
                    # if product.is_sale:
                    #     total = total + (product.sale_price * value)
                    # else:
=======
        for key, value in quantities.item():
            # Convert key string into so we can do math
            key = int(key)
            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total = total + (product.sale_price * value)
                    else:
>>>>>>> a16a1ec8b722ec404eeb786f560df4dcfe9a66a2
                        total = total + (product.price * value)



        return total



<<<<<<< HEAD
=======


>>>>>>> a16a1ec8b722ec404eeb786f560df4dcfe9a66a2
    def __len__(self):
        return len(self.cart)
    
    def get_prods(self):
<<<<<<< HEAD
        # Get ids from cart
        product_ids = self.cart.keys()
        # User ids to lookup products in database model
        products = Product.objects.filter(id__in=product_ids)
=======
        # Get ida from cart
        product_ids = self.cart.keys()
        # Use ids to lookup products in database model
        products = Product.object.filter(id__in=product_ids)
>>>>>>> a16a1ec8b722ec404eeb786f560df4dcfe9a66a2

        # Return those looked up products
        return products
    
    def get_quants(self):
        quantities = self.cart
        return quantities
    
<<<<<<< HEAD
    def update(self, product, quantity,):
=======
    def update(self, product, quantity):
>>>>>>> a16a1ec8b722ec404eeb786f560df4dcfe9a66a2
        product_id = str(product)
        product_qty = int(quantity)

        # Get cart
        ourcart = self.cart
        # Update Dictionary/cart
        ourcart[product_id] = product_qty

        self.session.modified = True

<<<<<<< HEAD

        # Deal with logged in user
        if self.request.user.is_authenticated:
            # Get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # Convert {'3':1, '2':4} to {"3":1, "2":4}
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # Save carty to the Profile Model
            current_user.update(old_cart=str(carty))


=======
>>>>>>> a16a1ec8b722ec404eeb786f560df4dcfe9a66a2
        thing = self.cart
        return thing
    
    def delete(self, product):
        product_id = str(product)
<<<<<<< HEAD
        # Delete from dictionary/cart
        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True

        # Deal with logged in user
        if self.request.user.is_authenticated:
            # Get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # Convert {'3':1, '2':4} to {"3":1, "2":4}
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # Save carty to the Profile Model
            current_user.update(old_cart=str(carty))
=======
        # Delete from distionary/cart
        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True
>>>>>>> a16a1ec8b722ec404eeb786f560df4dcfe9a66a2
