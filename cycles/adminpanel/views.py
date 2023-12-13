from datetime import date, datetime
from itertools import count
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.views.decorators.cache import never_cache
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q,Count

from product.models import Product, ProductVarient

from orders.models import Order, OrderItem



# Create your views here.
def adminlogin(request):
    if 'username' not in request.session:
       
        if request.method=='POST':
            username=request.POST.get('username')
            password=request.POST.get('password')
            admin=authenticate(username=username,password=password)
            if admin and admin.is_superuser:
                login(request, admin)
                request.session['username'] = admin.username 
                return redirect('dashboard')
            else:
                messages.error(request,"Bad Credentials.! ")
                return redirect('adminlogin')


        return render(request,'admin_login.html')
    return redirect('dashboard')

@never_cache
def dashboard(request,filter=None):
    if 'username' in request.session and request.user.is_superuser:
        if filter!= None:
            today = date.today()
            start_of_month = datetime(today.year, today.month, 1)
            start_of_year = datetime(today.year, 1, 1)

            if filter == 'today':
                delivered_order_items = OrderItem.objects.filter(
                    status='Delivered',
                    created_at__date=today
                )
            elif filter == 'month':
                delivered_order_items = OrderItem.objects.filter(
                    status='Delivered',
                    created_at__gte=start_of_month
                )
            elif filter == 'year':
                delivered_order_items = OrderItem.objects.filter(
                    status='Delivered',
                    created_at__gte=start_of_year
                )

        else:    
            delivered_order_items = OrderItem.objects.filter(status='Delivered')
        count_of_selled_product = 0 
        revenue = 0
        for order_items in delivered_order_items:
            count_of_selled_product  += order_items.quantity
            revenue += order_items.price
        all_variations = ProductVarient.objects.all()    
        total_stock = sum(variation.stock_quantity for variation in all_variations)

        context={'count_of_selled_product':count_of_selled_product,
                 'revenue':revenue,
                 'total_stock':total_stock}    


        return render(request,'dashboard.html',context)

    return redirect('adminlogin')

@login_required
def customers(request):
    if 'username' in request.session and request.user.is_superuser:
        user = User.objects.all()
        query = request.GET.get('text')

        if query:
            emp = emp.filter(Q(first_name__icontains=query) | Q(email__icontains=query) | Q(username__icontains=query))



        context = {
            'user':user,
            
        }

        return render(request,'customers.html',context)
    return redirect('adminlogin')



@login_required
def block_customer(request, user_id):
    try:
        if request.user.is_superuser:
            user = User.objects.get(id=user_id)
            user.is_active = False  
            user.save()
    except User.DoesNotExist:
        pass
    return redirect('customers')

def unblock_customer(request, id):
    if request.user.is_superuser:  
        user = User.objects.get(id=id)
        user.is_active = True  
        user.save()
        return redirect('customers')
    else:
        return redirect('customers')


def search(request):
    query = request.GET.get('text')
    user = User.objects.filter(Q(first_name__icontains=query) | Q(email__icontains=query) | Q(username__icontains=query))

    context = {
        'user': user,
    }
    return render(request, 'customers.html', context)

@never_cache
def adminlogout(request):
    if request.user.is_authenticated and request.user.is_superuser:
        request.session.flush()
    return redirect('adminlogin')


from django.db.models import Sum

def report(request):
    if request.method == 'POST':
        start_date_str = request.POST.get('startDate')
        end_date_str = request.POST.get('endDate')

        # Convert string representations of dates to datetime objects
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

        # Filter OrderItem objects based on the date range
        order_items = OrderItem.objects.filter(created_at__range=(start_date, end_date))

        # Aggregate the quantity of each product ordered on the specified date
        product_quantities = order_items.values('product__name').annotate(total_quantity=Sum('quantity'))
       

        # product_quantities_per_day = order_items.values('created_at', 'product__name').annotate(total_quantity=Sum('quantity'))
        # print(product_quantities_per_day)

    return render(request, 'sales_report.html', {'order_items': order_items, 'product_quantities': product_quantities,'start_date':start_date_str,'end_date':end_date_str})




