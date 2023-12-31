from datetime import date
import datetime
from os import name
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.db.models import Q
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.contrib import messages
from adminpanel.models import Offers
from orders.models import Order, OrderItem
from .models import Coupon, Product, ProductImage, Category, Brand, ProductVarient 
from adminpanel.views import user_passes_test,is_admin

from .forms import  CouponForm, OffersForm, ProductVariantForm


# ----------product management start--------------

@user_passes_test(is_admin, login_url='adminlogin')
def products(request):
    if 'username' in request.session: 
        products = Product.objects.all()
        context = {
            'products': products,  
        }
        return render(request, 'products.html', context)
    return redirect('adminlogin')

@user_passes_test(is_admin, login_url='adminlogin')
def add_element(request):
    categories = Category.objects.filter(is_deleted=False) 
    brands = Brand.objects.filter(is_deleted=False) 
    offers = Offers.objects.filter(is_active = True)
    
 
    context = {
        'categories': categories,
        'brands': brands,
        'offers' : offers,
    }
    return render(request,'Adding_products.html',context)

@user_passes_test(is_admin, login_url='adminlogin')
def add_product(request):
    if request.method == 'POST':
        
        name = request.POST.get('name')
        description = request.POST.get('description')
        category_id = request.POST.get('category')
        brand_id = request.POST.get('brand')
        offer_id = request.POST.get('offer')
        size = request.POST.get('size')
        
        category = Category.objects.get(pk=category_id)
        brand = Brand.objects.get(pk=brand_id)
        if offer_id:
            offer = Offers.objects.get(pk=offer_id)
        else:
            offer = None    

        product=Product(name = name,
        description = description,
        category = category,
        brand = brand,
        offer = offer,
        size = size
        )
        product.save()
        
        images = request.FILES.getlist('image')

        for image in images:
            ProductImage.objects.create(product=product,image=image)
        return redirect('products')

    return render(request, 'your_template.html')


@user_passes_test(is_admin, login_url='adminlogin')
def edit_element(request,id):
    categories = Category.objects.all() 
    brands = Brand.objects.all()
    offers = Offers.objects.filter(is_active = True)
    product = get_object_or_404(Product, id=id)
    context = {
        'categories': categories,
        'brands': brands,
        'product':product,
        'offers' : offers
    }
    

    return render(request,'editing.html',context)

@user_passes_test(is_admin, login_url='adminlogin')
def update(request, id):
    
    product = get_object_or_404(Product, id=id)

    if request.method == 'POST':
        
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        category_id = request.POST.get('category')
        brand_id = request.POST.get('brand')
        offer_id = request.POST.get('offer')
        size = request.POST.get('size')
        
        category = Category.objects.get(pk=category_id)
        brand = Brand.objects.get(pk=brand_id)
        try:
            offer = Offers.objects.get(pk=offer_id)
        except:
            offer = None


        product.name = name
        product.description = description
        product.category = category
        product.offer = offer
        product.brand = brand
        product.size = size
        
        
        
        images = request.FILES.getlist('new_image')

        delete_images = request.POST.getlist('delete_images')

        # Handle image deletions
        for image_id in delete_images:
            product_image = ProductImage.objects.get(id=image_id)
            product_image.delete()

        for image in images:
            ProductImage.objects.create(product=product,image=image)

        product.save()
        return redirect('products')

    return render(request, 'products.html')

@user_passes_test(is_admin, login_url='adminlogin')
def unlist(request, id):
    product = get_object_or_404(Product, id=id)
    product.is_availability = False
    product.save()
    return redirect('products')


@user_passes_test(is_admin, login_url='adminlogin')
def list(request, id):
    product = get_object_or_404(Product, id=id)
    product.is_availability = True
    product.save()
    return redirect('products')


@user_passes_test(is_admin, login_url='adminlogin')
def varient(request, id=None):
    if id is not None:
        product_id = id

    product = Product.objects.get(id=product_id)
    varients = ProductVarient.objects.filter(product=product)
    
    if request.method == 'POST':
        form = ProductVariantForm(request.POST)

        if form.is_valid():
            variant = form.save(commit=False)
            if variant.brake in [v.brake for v in varients]:
                messages.error(request, 'Same type of brake already exists')
                return redirect('varient',id)
            if variant.price is not None and variant.price < 0:
                messages.error(request, 'Price should be non-negative')
                return redirect('varient',id)
            elif variant.stock_quantity is not None and variant.stock_quantity < 0:
                messages.error(request, 'Stock quantity should be non-negative')      
                return redirect('varient',id)
            else:    
                variant.product = product
                variant.save()
            return redirect('varient', id)
        else:
            messages.error(request, 'Form submission failed. Please check the form.')

    else:
        form = ProductVariantForm()

    return render(request, 'varient.html', {'product': product, 'form': form})


@user_passes_test(is_admin, login_url='adminlogin')
def edit_varient(request,varient_id):
    varient = ProductVarient.objects.get(id = varient_id)

    return render(request,'edit_varient.html',{'varient':varient})

@user_passes_test(is_admin, login_url='adminlogin')
def update_varient(request,id):
    varient = ProductVarient.objects.get(id = id)
    product = varient.product
    if request.method == 'POST':
    
        form = ProductVariantForm(request.POST,instance=varient)
        varients = ProductVarient.objects.filter(product=product).exclude(id=varient.id)


        if form.is_valid():
            varient = form.save(commit=False)
            
        if form.is_valid():
            variant = form.save(commit=False)
            if variant.brake in [v.brake for v in varients]:
                messages.error(request, 'Same type of brake already exists')
                return redirect('varient',varient.product.id)
            if variant.price is not None and variant.price < 0:
                messages.error(request, 'Price should be non-negative')
                return redirect('varient',varient.product.id)
            elif variant.stock_quantity is not None and variant.stock_quantity < 0:
                messages.error(request, 'Stock quantity should be non-negative')      
                return redirect('varient',varient.product.id)
            else:    
                varient.product = product
                varient.save()
            return redirect('varient',varient.product.id)  
        else:
            messages.error(request, 'Form submission failed. Please check the form.')
    
    
    return redirect('edit_varient')

@user_passes_test(is_admin, login_url='adminlogin')
def delete_varient(request,varient_id):
    varient = ProductVarient.objects.get(id = varient_id)
    varient.delete()
    product_id = varient.product.id
    return redirect('varient',product_id)




@user_passes_test(is_admin, login_url='adminlogin')
def search(request):
    query = request.GET.get('query')  
    products = Product.objects.all()

    if query and query.strip():
        products = products.filter(
            Q(name__icontains=query) |
            Q(brand__name__icontains=query) |
            Q(category__name__icontains=query)
        )

    context = {
        'products': products,
    }

    return render(request, 'products.html', context)

 # ----------product management end--------------

@user_passes_test(is_admin, login_url='adminlogin')
def category(request):
    if 'username' in request.session:
        categories = Category.objects.all()  
        context = {
            'categories': categories,
        }
        return render(request, 'category.html', context)
    return redirect('adminlogin')

@user_passes_test(is_admin, login_url='adminlogin')
def category_add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        name = name.capitalize()
        category = Category(name=name)
        category.save()
        return redirect('category')  
    return redirect('category')                        

@user_passes_test(is_admin, login_url='adminlogin')
def category_edit(request, id):
    category = Category.objects.all()

    context = {
        'category':category,
        
    }
    return render(request, 'category.html', context)

@user_passes_test(is_admin, login_url='adminlogin')
def category_update(request, id):
    if request.method == "POST":
        name = request.POST.get('name')
        name = name.capitalize()

        category = Category(
            id=id,
            name=name

        )

        category.save()
        return redirect('category')

    
    return redirect(request,'category.html')

@user_passes_test(is_admin, login_url='adminlogin')
def category_delete(request,id):
    category = get_object_or_404(Category, id=id)
    category.is_deleted = True
    category.save()
    Product.objects.filter(category=category).update(is_availability=False)


    return redirect('category')

@user_passes_test(is_admin, login_url='adminlogin')
def category_undelete(request,id):
    category = get_object_or_404(Category, id=id)
    category.is_deleted = False
    category.save()
    return redirect('category')



@user_passes_test(is_admin, login_url='adminlogin')
def category_search(request):
    query = request.GET.get('query')
    
    if query is not None and query.strip():  
        categories = Category.objects.filter(Q(name__icontains=query) )
    else:
        categories = Category.objects.all()
    
    context = {
        'categories': categories,
    }
    return render(request, 'category.html', context)


# --------------------  category_END ---------------

# --------------------  BRAND ---------------
@user_passes_test(is_admin, login_url='adminlogin')
def brand(request):
    if 'username' in request.session:
        brands = Brand.objects.all()  
        context = {
            'brands': brands,
        }
        return render(request, 'brand.html', context)
    return redirect('adminlogin')

@user_passes_test(is_admin, login_url='adminlogin')
def brand_add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        name = name.upper()
        brand = Brand(name=name)
        brand.save()
        return redirect('brand')  
    return redirect('brand')

@user_passes_test(is_admin, login_url='adminlogin')
def brand_edit(request, id):
    brand = Brand.objects.all()
    

    context = {
        'brand':brand,
        
    }
    return render(request, 'brand.html', context)

@user_passes_test(is_admin, login_url='adminlogin')
def brand_update(request, id):
    if request.method == "POST":
        name = request.POST.get('name')
        name = name.upper()

        brand = Brand(
            id=id,
            name=name

        )

        brand.save()
        return redirect('brand')

    
    return redirect(request,'brand.html')

@user_passes_test(is_admin, login_url='adminlogin')
def brand_delete(request,id):
    brand = get_object_or_404(Brand, id=id)
    brand.is_deleted = True
    brand.save()
    Product.objects.filter(brand=brand).update(is_availability=False)

    return redirect('brand')

@user_passes_test(is_admin, login_url='adminlogin')
def brand_undelete(request,id):
    brand = get_object_or_404(Brand, id=id)
    brand.is_deleted = False
    brand.save()
    return redirect('brand')



@user_passes_test(is_admin, login_url='adminlogin')
def brand_search(request):
    query = request.GET.get('query')
    
    if query is not None and query.strip():  
        brands = Brand.objects.filter(Q(name__icontains=query) )
    else:
        brands = Brand.objects.all()
    
    context = {
        'brands': brands,
    }
    return render(request, 'brand.html', context)




# -----------ORDER MANAGEMNT-----------
@user_passes_test(is_admin, login_url='adminlogin')
def order(request, item_id=None):
    if item_id:
        if request.method == 'POST':
            new_status = request.POST.get('new_status')
            
            choices = [status[0] for status in OrderItem.orderstatuses]
            if new_status in choices:
                item = OrderItem.objects.get(id=item_id)
                item.status = new_status
                item.save()
                return redirect('order') 
    
    order_items = OrderItem.objects.all().order_by('-created_at')
    context = {'order_items': order_items}
    return render(request, 'order.html', context)


@user_passes_test(is_admin, login_url='adminlogin')
def coupon(request):
    
    if request.method == 'POST':
        form = CouponForm(request.POST)
        if form.is_valid():
            coupon = form.save(commit=False)
            if coupon.valid_upto and coupon.valid_upto.date() < date.today():
                coupon.is_active = False
            else:    
                coupon.is_active = True
            coupon.save()  # Save each coupon after updating is_active
            form.save()  # Save the new coupon
            return redirect(reverse('coupon'))
    else:
        form = CouponForm()
        coupon_True = Coupon.objects.filter(is_active=True)
        for coupon_active in coupon_True:
            if coupon_active.valid_upto and coupon_active.valid_upto.date() < date.today():
                coupon_active.is_active = False
            coupon_active.save()  # Save each coupon after updating is_active
        coupons = Coupon.objects.all()        

    return render(request, 'coupon_management.html', {'coupons': coupons, 'form': form})

@user_passes_test(is_admin, login_url='adminlogin')
def delete_coupon(request,coupon_id):

    coupon = Coupon.objects.filter(id = coupon_id)
    coupon.delete()
    
    return redirect('coupon')

@user_passes_test(is_admin, login_url='adminlogin')
def edit_coupon(request, coupon_id=None):
    coupon = Coupon.objects.get(id=coupon_id)

    if request.method == 'POST':
        form = CouponForm(request.POST, instance=coupon)
        if form.is_valid():
            coupon = form.save(commit=False)
            
            if coupon.valid_upto and coupon.valid_upto.date() < date.today():
                coupon.is_active = False
            else:    
                coupon.is_active = True
            coupon.save()
            
            return redirect('coupon')
    else:
        form = CouponForm(instance=coupon)

    return render(request, 'edit_coupon.html', {'coupon': coupon, 'form': form})

# ------------ Offers -------------
@user_passes_test(is_admin, login_url='adminlogin')
def offers(request):

    offers = Offers.objects.all()

    if request.method == 'POST':
        form = OffersForm(request.POST)
        if form.is_valid():
            offer = form.save(commit=False)
            if offer.start_date <= timezone.now() and offer.end_date > timezone.now():
                offer.is_active = True
            else:
                offer.is_active = False    

            offer.save()
            return redirect(reverse('offers'))  
    else:
        form = OffersForm()

        for offer in offers:
            if offer.start_date <= timezone.now() and offer.end_date > timezone.now():
                offer.is_active = True
                offer.save()
            else:
                offer.is_active = False 
                offer.save()   

    context = {
                'offers':offers,
                'form': form
            }    

    return render(request, 'offers.html',context)

@user_passes_test(is_admin, login_url='adminlogin')
def delete_offer(request,offer_id):
    offer = Offers.objects.get(id = offer_id)
    offer.delete()
    return redirect('offers')

@user_passes_test(is_admin, login_url='adminlogin')
def edit_offer(request, offer_id):
    offer = Offers.objects.get(id=offer_id)

    if request.method == 'POST':
        form = OffersForm(request.POST, instance=offer)
        if form.is_valid():
            offer = form.save(commit=False)
            if offer.start_date <= timezone.now() and offer.end_date > timezone.now():
                offer.is_active = True
            else:
                offer.is_active = False
            offer.save()
            return redirect('offers')
    else:
        form = OffersForm(instance=offer)

    return render(request, 'edit_offer.html', {'offer':offer,'form': form})




