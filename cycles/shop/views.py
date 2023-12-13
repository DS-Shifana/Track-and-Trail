from django.shortcuts import render
from cart.models import CartItem
from product.models import Product,ProductImage,Category, ProductVarient
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from cart.views import _cart_id

# Create your views here.




def shop(request):
    query = request.GET.get('query', '')  # Get the 'query' parameter from the request

    products = Product.objects.filter(is_availability=True).order_by('id')

    if query:
        products = products.filter(category__name__icontains=query)


    paginator = Paginator(products, 9)  

    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    return render(request, 'shop.html', {'products': products})

def product_detail(request, product_id):
    product = Product.objects.get(pk=product_id)
    current_user = request.user

    if current_user.is_authenticated:
        in_cart = CartItem.objects.filter(user=current_user, product=product).exists()
    else:
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=product).exists()

    variants = ProductVarient.objects.filter(product=product)

    context = {
        'product': product,
        'variants': variants,
        'in_cart': in_cart
    }

    return render(request, 'product_detailes.html', context)




def category_suggestions(request):
    query = request.GET.get('query','')

    # Query the database to get category suggestions
    categories = Category.objects.filter(name__icontains=query)

    suggestions = [category.name for category in categories]

    return JsonResponse({'suggestions': suggestions})


