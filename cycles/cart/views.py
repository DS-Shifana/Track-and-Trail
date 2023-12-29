
from django.shortcuts import get_object_or_404, redirect, render
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from orders.models import ShippingAddress, Wallet
from product.models import Product, ProductVarient
from cart.models import Cart,CartItem,Wishlist
from django.utils import timezone
from django.urls import reverse
from orders.forms import OrderForm, ShippingAddressForm


def _cart_id(request):
    cart=request.session.session_key
    if not cart:
        cart=request.session.create()
    return cart  


#ADDING CART USING SESSION ID

def add_to_cart(request, variant_id):
    variation = get_object_or_404(ProductVarient, id=variant_id)
    product = variation.product
    current_user = request.user

    if current_user.is_authenticated:
        wishlist_items = Wishlist.objects.filter(user=request.user)
        try:
            cart= Cart.objects.get(user=current_user)

        except Cart.DoesNotExist:
            cart = Cart.objects.create(user=current_user,cart_id=_cart_id(request))
            cart.save()

        is_cart_item_exists = CartItem.objects.filter(cart=cart, product=product, user=current_user, variation=variation).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.get(product=product, user=current_user, variation=variation)
            cart_item.quantity += 1
            # variation.stock_quantity -= 1
            # variation.save()
            wishlist_items.filter(product=product).delete()        
            cart_item.save()
        else:
            cart_item = CartItem.objects.create(
                cart=cart,
                product=product,
                quantity=1,
                user=current_user,
                variation = variation,
            )

            # variation.stock_quantity -= 1
            # variation.save()
            cart_item.save()
        return redirect('cart')
        


    else:
        wishlist_product_ids = []
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id=_cart_id(request))
            cart.save()
        is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart, variant=variation).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.get(product=product, cart=cart,variant=variation)
            if cart_item:
                item = CartItem.objects.get(product=product, variant=variation, id=variant_id)
                item.quantity += 1
                item.save()
            else:
                item = CartItem.objects.create(product=product, variant=variation, quantity=1, cart=cart)
                item.save()
        else:
            cart_item = CartItem.objects.create(
                product=product,
                variant=variation,
                quantity=1,
                cart=cart,
            )
            # variation.stock_quantity -= 1
            # variation.save()
            cart_item.save()
        return redirect(reverse('cart'))




def decrement_cartItem(request,variant_id,cart_item_id):
    variation = get_object_or_404(ProductVarient, id=variant_id)
    product = variation.product
    try:
        if request.user.is_authenticated:
           cart_item    = CartItem.objects.get(product=product,variation=variation,user=request.user, id=cart_item_id)
        else:
           cart    = Cart.objects.get(cart_id=_cart_id(request))
           cart_item    = CartItem.objects.get(product=product, variation=variation,cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            variation.stock_quantity +=1
            variation.save()
            cart_item.save() 
        else:
            cart_item.delete()
            # variation.stock_quantity +=1
            # variation.save()
    except:
        pass   
    return redirect ('cart')  

def increment_cartItem(request, variant_id):
    variation = get_object_or_404(ProductVarient, id=variant_id)
    product = variation.product

    if request.user.is_authenticated:
        cart_item, _ = CartItem.objects.get_or_create(product=product,variation=variation, user=request.user)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item, _ = CartItem.objects.get_or_create(product=product,variation=variation, cart=cart)
    if variation.stock_quantity > 0: 
        cart_item.quantity += 1
        # variation.stock_quantity -=1
        # variation.save()
        cart_item.save()

    return redirect('cart')


def delete_cart(request,variant_id,cart_item_id):
    
    variation = get_object_or_404(ProductVarient, id=variant_id)
    product = variation.product
    if request.user.is_authenticated:
        cart_item = CartItem.objects.filter(product=product,variation=variation,user=request.user,id=cart_item_id)
    else:
        cart      = Cart.objects.get(cart_id=_cart_id(request))    
        cart_item = CartItem.objects.filter(product=product,variation=variation,cart=cart,id=cart_item_id)

    # Get the cart item before deletion to retrieve the quantity
    cart_item_instance = cart_item.first()

    cart_item.delete()

    # variation.stock_quantity += cart_item_instance.quantity
    # variation.save()

    
    return redirect('cart')   

def cart(request,total=0 , quantity = 0 , cart_item= None):
    try:
        if request.user.is_authenticated:
           cart_items   = CartItem.objects.filter(user=request.user, is_active=True)
        else:
           cart         = Cart.objects.get(cart_id=_cart_id(request))
           cart_items   = CartItem.objects.filter(cart=cart, is_active=True)
        total = 0.0
        for cart_item in cart_items:
            total += cart_item.sub_total()
            quantity += cart_item.quantity

    except ObjectDoesNotExist:
       cart_items = []
        
    context ={
        'total' : total,
        'quantity' : quantity,
        'cart_items' : cart_items,
    }        
    
    return render(request,'cart.html',context)

  
@login_required(login_url='user_login')
def checkout(request,total=0 , quantity = 0 , cart_item= None):
    current_user = request.user
    Addresses = ShippingAddress.objects.filter(user_id=current_user)
    Addresses_exist = Addresses.exists()

    if request.method == 'POST':
        form = ShippingAddressForm(request.POST)
        if form.is_valid():
            
            address = form.save(commit=False)
            address.user_id = request.user.id
            address.status = True
            address.save()
            return redirect(reverse('checkout'))
        else:
            pass
    else:
        form = ShippingAddressForm()

    try:
        if request.user.is_authenticated:
           cart_items   = CartItem.objects.filter(user=request.user, is_active=True)
        else:
           cart         = Cart.objects.get(cart_id=_cart_id(request))
           cart_items   = CartItem.objects.filter(cart=cart, is_active=True)

        total = 0.0
        for cart_item in cart_items:
            total += cart_item.sub_total()
            quantity += cart_item.quantity

    except ObjectDoesNotExist:

        pass 
    forms = OrderForm()

    context ={
                'total' : total,
                'quantity' : quantity,
                'cart_items' : cart_items,
                'forms' : forms,
                'Addresses':Addresses,
                'Addresses_exist':Addresses_exist,
                'form':form
            }  
    user_wallet_exist = Wallet.objects.filter(user=request.user).exists()
    if user_wallet_exist:
        wallet = Wallet.objects.get(user=request.user)
        if wallet.amount >= total:
            context['wallet'] = True
        else: 
            context['wallet'] = False   

       

    return render(request, 'checkout.html', context)

@login_required(login_url='user_login')
def wishlist(request):

    wishlist_items = Wishlist.objects.filter(user=request.user)
    
        
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})

@login_required(login_url='user_login')
def add_to_wishlist(request, product_id):

    product = get_object_or_404(Product, id=product_id)
    if not Wishlist.objects.filter(user=request.user, product=product).exists():
        Wishlist.objects.create(user=request.user, product=product)  
    return redirect('shop')
@login_required(login_url='user_login')
def delete_from_wishlist(request, product_id):

    product = get_object_or_404(Product, id=product_id)
    wishlist_item = Wishlist.objects.filter(user=request.user,product=product)
    wishlist_item.delete()
    return redirect('wishlist')



