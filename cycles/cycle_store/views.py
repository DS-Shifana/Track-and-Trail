import random
import string
from telnetlib import LOGOUT
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib import messages,auth
from django.contrib.auth.hashers import make_password,check_password
from django.views.decorators.cache import never_cache
from django.utils import timezone
from datetime import timedelta
from cart.models import Cart,CartItem
from cart.views import _cart_id

from urllib.parse import urlparse, parse_qs
from django.utils import timezone

from orders.models import Wallet




# Create your views here.


def custom_404(request, exception):
    return render(request, '404.html', status=404)


@never_cache
def home(request):
    return render(request,'index.html')


@never_cache
def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                try:
                    guest_cart = Cart.objects.get(cart_id=_cart_id(request))
                    user_cart = Cart.objects.filter(user=user)
                    is_cart_item_exists = CartItem.objects.filter(cart=guest_cart).exists()
                    if user_cart.exists() and is_cart_item_exists:
                        user_cart_items = CartItem.objects.filter(cart=user_cart.first(), user=user)
                        if is_cart_item_exists:
                            guest_cart_items = CartItem.objects.filter(cart=guest_cart)
                            for item in guest_cart_items:
                                if CartItem.objects.filter(user=user, cart=user_cart.first(),product=item.product).exists():
                                    user_cart_item =  CartItem.objects.get(cart=user_cart.first(), product = item.product)
                                    user_cart_item.quantity += item.quantity
                                    user_cart_item.save()
                                else:
                                    new_cart_item = CartItem.objects.create(
                                        cart=user_cart.first(),
                                        product=item.product,
                                        quantity=item.quantity,
                                        user=user
                                    )
                                    new_cart_item.save()
                        guest_cart.delete()
                    else:
                        guest_cart.user = user
                        guest_cart.save()
                        if is_cart_item_exists:
                            guest_cart_items = CartItem.objects.filter(cart=guest_cart)
                            for item in guest_cart_items:
                                item.user = user
                                item.save()


                except Cart.DoesNotExist:
                    pass
                auth.login(request, user)
                url = request.META.get('HTTP_REFERER')
                # redirect to the previous page
                try:
                    parsed_url = urlparse(url)
                    query_params = parse_qs(parsed_url.query)
                    
                    # Extract the 'next' parameter
                    nextPage = query_params.get('next', [])[0]

                    if nextPage:
                        return redirect(nextPage)
                except Exception as e:
                    # Log the exception for debugging purposes
                    pass

                
                return redirect('home')
            else:
                messages.error(request, "Incorrect Username or Password!")
                return redirect('user_login')     

    return render(request, 'login.html')
    

@never_cache
def signup(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        referral_code = request.POST.get('referrel_code')

        request.session['fname'] = fname
        request.session['lname'] = lname
        request.session['username']=username
        request.session['password']=pass1
        request.session['email']=email
        request.session['referral_code']=referral_code

        if pass1==pass2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username already exist')
                return redirect('signup')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'Email already exist')
                return redirect('signup')
            else:
                send_otp(request)
                return render(request,'otp.html',{"email":email})
        else:
            messages.info(request,"Password mismatch")
            return redirect("signup")        

    return render(request, 'signup.html')

@never_cache
def send_otp(request):
    s = ""
    for x in range(0, 4):
        s += str(random.randint(0, 9))
    
    # Calculate the OTP expiration time (e.g., 2 minutes from now)
    otp_expiry_time = timezone.now() + timezone.timedelta(minutes=2)

    # Convert the datetime to a string in ISO 8601 format
    otp_expiry_time_str = otp_expiry_time.isoformat()
    
    request.session["otp"] = s
    request.session["otp_expiry_time"] = otp_expiry_time_str
    
    send_mail("otp for sign up", s, "shifanashifa471@gmail.com", [request.session['email']], fail_silently=False)
    return render(request, "otp.html")



@never_cache
def otp_verification(request):
    if request.method == 'POST':
        otp_ = request.POST.get("otp")
        otp_expiry_time_str = request.session.get("otp_expiry_time")

        if otp_expiry_time_str is None:
            # Handle the case where OTP expiration time is missing or not set
            messages.error(request, "OTP has expired or was never generated.")
            return render(request, 'otp.html')

        otp_expiry_time = timezone.datetime.fromisoformat(otp_expiry_time_str)

        if timezone.now() > otp_expiry_time:
            messages.error(request, "OTP has expired. Please request a new OTP.")
            return redirect('signup')
        if otp_ == request.session["otp"]:
            encryptedpassword = make_password(request.session['password'])
            user = User(username=request.session['username'], email=request.session['email'], password=encryptedpassword)
            user.first_name = request.session.get("fname")
            user.last_name = request.session.get("lname")
            user.referral_code = request.session.get("referral_code")
            def generate_referral_code(request,length=18):
                characters = string.ascii_letters + string.digits
                random_code = ''.join(random.choice(characters) for i in range(length))
                prefix = 'tRacKaNdTrAiL'
                referral_code = f"{prefix}{random_code}"
                return referral_code
            
            
            user.save()
            messages.info(request, 'Signed in successfully...')
            user.is_active = True

            wallet = Wallet.objects.create(user=user,amount ='0',referral_code = generate_referral_code(request))
            wallet.save()

            if user.referral_code is not None:
                try:
                    referred_by = Wallet.objects.get(referral_code=user.referral_code)
                    referred_by.amount += 100
                    referred_by.save()

                    referrint_to = Wallet.objects.get(user=user)
                    referrint_to.amount += 50
                    referrint_to.save()
                except:
                    pass    

            
            return redirect('home')
        else:
            messages.error(request, "OTP doesn't match")
            return render(request, 'otp.html')



@never_cache
def contact(request):
    if 'username' in request.session:
        return render(request,'contact.html')
    return redirect('user_login')

def custom_logout(request):
    if request.user.is_authenticated:
        logout(request)
        request.session.clear()
    return redirect('user_login')

@never_cache
def forgotPassword(request):
    if request.method == 'POST':
        # Get the user's email from the submitted form
        email = request.POST.get('email')

        is_email_exist = User.objects.filter(email=email).exists()

        if is_email_exist:

            # Store the email in the session
            request.session['email'] = email

            # Call the send_otp function to send the OTP
            pass_send_otp(request)

            return render(request, 'pass_otp.html', {"email": email})
        else:
            messages.error(request, "Email doesnot exist!Enter your existing Email Address")
           


    return render(request, 'forgotpassword.html')

@never_cache
def pass_send_otp(request):
    s = ""
    for x in range(0, 4):
        s += str(random.randint(0, 9))
    
    # Calculate the OTP expiration time (e.g., 2 minutes from now)
    otp_expiry_time = timezone.now() + timezone.timedelta(minutes=2)

    # Convert the datetime to a string in ISO 8601 format
    otp_expiry_time_str = otp_expiry_time.isoformat()
    
    request.session["otp"] = s
    request.session["otp_expiry_time"] = otp_expiry_time_str
    
    send_mail("OTP for set another password", s, "shifanashifa471@gmail.com", [request.session['email']], fail_silently=False)
    return render(request, "pass_otp.html")


@never_cache
def pass_otp_verification(request):
    if request.method == 'POST':
        otp_ = request.POST.get("otp")
        otp_expiry_time_str = request.session.get("otp_expiry_time")

        if otp_expiry_time_str is None:
            # Handle the case where OTP expiration time is missing or not set
            messages.error(request, "OTP has expired or was never generated.")
            return render(request, 'pass_otp.html')

        otp_expiry_time = timezone.datetime.fromisoformat(otp_expiry_time_str)

        if timezone.now() > otp_expiry_time:
            messages.error(request, "OTP has expired. Please request a new OTP.")
            return render(request, 'pass_otp.html')
        if otp_ == request.session["otp"]:
            
            return render(request,'set_newpass.html')
        else:
            messages.error(request, "OTP doesn't match")
            return render(request, 'pass_otp.html')

def set_newpassword(request):
    if request.method == 'POST':
        new_password = request.POST['password']
        encrypted_password = make_password(new_password)

   
    user = User.objects.get(email=request.session['email'])
    user.password = encrypted_password 
    user.save()  
    return render(request,'login.html')                


