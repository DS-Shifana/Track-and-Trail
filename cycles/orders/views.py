from django.utils import timezone 
import random
import string
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from cart.models import CartItem
from product.models import Coupon,ProductVarient
from .forms import OrderForm, ShippingAddressForm, UserForm
from .models import Order, OrderItem, ShippingAddress, Wallet
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.db.models import Q

import razorpay
from django.conf import settings

from django.contrib.auth import get_user

@login_required(login_url='user_login')
def place_order(request, total=0, quantity=0):
    current_user = request.user
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()

    if cart_count <= 0:
        return redirect('shop')

    for cart_item in cart_items:
        total += (cart_item.variation.price * cart_item.quantity)
        quantity += cart_item.quantity
        
    trackNo = 'TRcycles'+str(random.randint(1111111,9999999))    

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():

            order = form.save(commit=False)

            # Get the selected shipping address from the form
            selected_address_id = request.POST.get('billing_address_option')
            shipping_address = ShippingAddress.objects.get(id=selected_address_id)
            shipping_address.status=True
            shipping_address.save()

            user_shipping_addresses = ShippingAddress.objects.filter(user=current_user).exclude(id=selected_address_id)
            for address in user_shipping_addresses:
                address.status=False
                address.save()
            
            order.user = current_user
            order.total_price = total
            order.tracking_no=trackNo
            order.shipping_address = shipping_address
            order.save()
            
            return redirect('payment')
    else:
            form = OrderForm()


    return redirect('checkout')

@login_required(login_url='user_login')
def payment(request, quantity=0):
    current_user = request.user
    
    try:
        orders = Order.objects.get(user=current_user, is_ordered=False)
    except:
        orders = Order.objects.filter(user=current_user, is_ordered=False)

        orders.delete()

        return redirect('place_order')    

    amount = 0  
    if orders:
            Addresses = orders.shipping_address
        
            is_exist_order_items = OrderItem.objects.filter(order=orders.id,user=request.user, ordered=True).exists()
            total = 0
            if is_exist_order_items == False :
            # Handle the exception here
                cart_items = CartItem.objects.filter(user=request.user)

                print(">>>>>>>>>>>>>>>>>>>>>>>>>>>cart items",cart_items)
                
                for cart_item in cart_items:
                    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>cart cart_item",cart_item)

                    variation_instance = ProductVarient.objects.get(id=cart_item.variation.id)
                    quantity += cart_item.quantity
                    order_item = OrderItem.objects.create(
                        order=orders,
                        product=cart_item.product,
                        price=(cart_item.sub_total()),
                        quantity=cart_item.quantity,
                        brake = variation_instance,
                        user=request.user,
                        ordered=True
                    )
                    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>cart order_item",order_item)

                    order_item.save()
                return redirect(reverse('payment'))
            else:        
            # To get the Quantity
                order_items = OrderItem.objects.filter(order=orders.id,user=request.user, ordered=True)
                
                for order_item in order_items:
                    quantity += order_item.quantity
                    total += order_item.price

       
            client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))
            payment = client.order.create({'amount': orders.total_amount * 100, 'currency': 'INR', 'payment_capture': '1'})
            orders.razor_pay_payment_id = payment['id']


            context = { 'orders': orders,
                        'quantity':quantity,
                        'Addresses': Addresses,
                        'payment': payment,
                        'total' : total
                    
                     }
            
             #To get the Coupon 
            coupon_exist = Coupon.objects.filter(
                            Q(is_active=True) &
                            (Q(min_purchase_amount__lte=total) | Q(min_purchase_amount__isnull=True)) &
                            (Q(max_purchase_amount__gte=total) | Q(max_purchase_amount__isnull=True))
                        ).exists()

            if coupon_exist:
                coupons = Coupon.objects.filter(
                            Q(is_active=True) &
                            (Q(min_purchase_amount__lte=total) | Q(min_purchase_amount__isnull=True)) &
                            (Q(max_purchase_amount__gte=total) | Q(max_purchase_amount__isnull=True))
                        )
                context['coupons']=coupons

    return render(request, 'payment.html', context)
@login_required(login_url='user_login')
def apply_coupon(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        coupon_code = request.POST.get('coupon')

        try:
            coupon = Coupon.objects.get(id=coupon_code, is_active=True)

            if coupon.valid_upto < timezone.now():
                messages.error(request, 'Coupon has expired.', extra_tags='danger')
            elif order.total_amount < coupon.min_purchase_amount:
                messages.error(request, f'Amount should be greater than {coupon.min_purchase_amount}', extra_tags='danger')
            elif not coupon.is_user_eligible(request.user):
                messages.error(request, 'You have already used this coupon.', extra_tags='danger')
            elif order.applied_coupon:
                messages.error(request, 'Coupon already applied.', extra_tags='danger')
            else:
                order.applied_coupon = coupon
                order.save()
                coupon.mark_as_used(request.user)
                messages.success(request, 'Coupon successfully applied.', extra_tags='success')

        except Coupon.DoesNotExist:
            messages.error(request, 'Invalid coupon code. Please try again.', extra_tags='danger')

    return redirect('payment')

@login_required(login_url='user_login')
def remove_coupon(request,order_id):
    order = get_object_or_404(Order, id=order_id)
    order.applied_coupon = None
    order.save()


    return redirect('payment')      

    


# ------PROFILE---------
@login_required(login_url='user_login')
def profile(request):

    if request.user.is_authenticated:
        profile = User.objects.get(username=request.user)
    else:
        return redirect('signup')

    return render(request, 'profile.html', {'profile': profile})

def edit_profile(request):

    if request.method == 'POST':
        form = UserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  

    else:
        form = UserForm(instance=request.user)

    return render(request, 'edit_profile.html', {'form': form})

# CHANGE PASSWORD
@login_required(login_url='user_login')
def change_password(request):
    if request.method == 'POST':
        current_user = request.user
        old_password = request.POST['old_password']
        new_password = request.POST['newpassword']
        renew_password = request.POST['renewpassword']
        
        if new_password == renew_password:
            if current_user.check_password(old_password):
                current_user.set_password(new_password)
                current_user.save()
                update_session_auth_hash(request, current_user)
                messages.error(request, "Your Password is changed")     

            else:
                messages.error(request, "Mismatch in Old Password! Re-enter your old password")     
        else:
            messages.error(request, "Mismatch in New Password, Re-enter Password!")

    return redirect('profile')

# ------ADDRESS------
@login_required(login_url='user_login')
def my_address(request): 

    current_user = request.user.id
    if request.user.is_authenticated:
        
        Addresses = ShippingAddress.objects.filter(user_id = current_user)
        

    return render(request,'Address.html',{'Addresses':Addresses})



@login_required(login_url='user_login')
def add_address(request):
    if request.method == 'POST':
        
        form = ShippingAddressForm(request.POST)
        if form.is_valid():
            
            address = form.save(commit=False)
            address.user_id = request.user.id
            
            address.save()
            return redirect('my_address')
        else:
           pass
    else:
        form = ShippingAddressForm()

    return render(request, 'address.html', {'form': form})

@login_required(login_url='user_login')
def edit_address(request, address_id):
    address = get_object_or_404(ShippingAddress, id=address_id)
    form = ShippingAddressForm(instance=address)
    
    return render(request, 'Editaddress.html', {'address': address, 'form': form})

@login_required(login_url='user_login')
def update_address(request, address_id):
    existing_address = get_object_or_404(ShippingAddress, id=address_id)

    if request.method == 'POST':
        form = ShippingAddressForm(request.POST, instance=existing_address)
        if form.is_valid():
            address = form.save(commit=False)
            address.user_id = request.user.id
            address.save()
            return redirect('my_address')
        else:
            return redirect('edit_address', address_id=address_id)
    else:
        form = ShippingAddressForm(instance=existing_address)

    context = {
        'form': form,
        'address_id': address_id,
    }

    return render(request, 'Editaddress.html', context)

@login_required(login_url='user_login')
def remove_address(request, address_id):
    address = get_object_or_404(ShippingAddress, id=address_id)
    address.delete()

    messages.success(request, 'Address removed successfully.')

    return redirect('my_address')

@login_required(login_url='user_login')
def my_orders(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('orderitem_set__product') 

    context ={
        'orders':orders
    }

    return render(request,'my_orders.html',context)



@login_required(login_url='user_login')
def cancel_order(request, order_item_id):
    if request.method == 'POST':
        order_item = get_object_or_404(OrderItem, id=order_item_id)
        order_item.status = "Cancelled"
        order_item.save()
        varient_id = order_item.brake.id
        varient = ProductVarient.objects.get(id = varient_id)
        varient.stock_quantity += order_item.quantity
        varient.save() 

        wallet = Wallet.objects.get(user = request.user)
        wallet.amount += order_item.price
        wallet.save() 

        messages.success(request, 'Order canceled successfully.')

    return redirect('my_orders')

@login_required(login_url='user_login')
def order_success(request):
    order_id = request.GET.get('order_id')
    order = Order.objects.get(razor_pay_order_id = order_id,is_ordered=False)
    order.is_ordered = True
    order.save()
    cart_items = CartItem.objects.filter(user=request.user)
    cart_items.delete()

          
    return render(request,'order_success.html')

#wallet
@login_required(login_url='user_login')
def wallet(request):
    try:
        user_wallet = Wallet.objects.get(user=request.user)
        wallet = user_wallet  
    except Wallet.DoesNotExist:
        def generate_referral_code(request, length=18):
            characters = string.ascii_letters + string.digits
            random_code = ''.join(random.choice(characters) for i in range(length))
            prefix = 'tRacKaNdTrAiL?ReFerReLcODe/'
            referral_code = f"{prefix}{random_code}"
            return referral_code

        wallet = Wallet.objects.create(user=request.user, amount='0', referral_code=generate_referral_code(request))
        wallet.save()

    return render(request,'wallet.html',{'wallet':wallet})

@login_required(login_url='user_login')
def orderby_wallet(request):

    total_price = request.GET.get('total_price')
    total_amount = float(total_price)
   

    user_wallet = Wallet.objects.get(user=request.user)
    user_wallet.amount = user_wallet.amount - total_amount
    user_wallet.save()

    return redirect(order_success)



