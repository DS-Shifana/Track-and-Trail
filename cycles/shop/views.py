from django.shortcuts import render
from cart.models import CartItem, Wishlist
from product.models import Product,ProductImage,Category, ProductVarient
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.db.models import Count

from cart.views import _cart_id

# Create your views here.




def shop(request):
    query = request.GET.get('query', '')  # Get the 'query' parameter from the request
    category = request.GET.get('category', '') 
    products = Product.objects.filter(is_availability=True).annotate(variant_count=Count('productvarient')).filter(variant_count__gt=0).order_by('id')



    if query:
        products = products.filter(category__name__icontains=query)
    

    if category:

        products = products.filter(category__name__icontains=category)


    paginator = Paginator(products, 9)  

    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    if request.user.is_authenticated:
        wishlist_items = Wishlist.objects.filter(user=request.user)
        wishlist_product_ids = wishlist_items.values_list('product__id', flat=True)
    else:
        wishlist_product_ids = []  # If the user is not authenticated, handle it accordingly
     

    return render(request, 'shop.html', {'products': products,'wishlist_product_ids':wishlist_product_ids})

def product_detail(request, product_id):
    product = Product.objects.get(pk=product_id)
    current_user = request.user

    if current_user.is_authenticated:
        in_cart = CartItem.objects.filter(user=current_user, product=product).exists()
    else:
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=product).exists()

    variants = ProductVarient.objects.filter(product=product)
    if request.user.is_authenticated:
        wishlist_items = Wishlist.objects.filter(user=request.user)
        wishlist_product_ids = wishlist_items.values_list('product__id', flat=True)
    else:
        wishlist_product_ids = [] 

    context = {
        'product': product,
        'variants': variants,
        'in_cart': in_cart,
        'wishlist_product_ids':wishlist_product_ids
    }
    
    return render(request, 'product_detailes.html', context)




def category_suggestions(request):
    query = request.GET.get('query','')

    # Query the database to get category suggestions
    categories = Category.objects.filter(name__icontains=query)

    suggestions = [category.name for category in categories]

    return JsonResponse({'suggestions': suggestions})


