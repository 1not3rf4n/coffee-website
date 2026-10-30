from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from apps.shop.models import Product
from apps.cart.cart import Cart

def cart_detail_view(request):
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})

@require_POST
def cart_add_api(request):
    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity', 1))
    grind_type = request.POST.get('grind_type', 'دانه کامل')
    
    product = get_object_or_404(Product, id=product_id)
    cart = Cart(request)
    cart.add(product=product, quantity=quantity, grind_type=grind_type)
    
    return JsonResponse({
        'success': True,
        'message': f'{product.title} به سبد خرید اضافه شد.',
        'cart_total_items': len(cart),
        'cart_total_price': cart.get_total_price()
    })

@require_POST
def cart_remove_api(request):
    item_key = request.POST.get('item_key')
    cart = Cart(request)
    cart.remove(item_key)
    
    return JsonResponse({
        'success': True,
        'cart_total_items': len(cart),
        'cart_total_price': cart.get_total_price()
    })
