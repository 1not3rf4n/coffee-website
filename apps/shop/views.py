from django.shortcuts import render, get_object_or_404
from apps.shop.models import ProductCategory, Product

def shop_index_view(request):
    categories = ProductCategory.objects.filter(is_active=True)
    products = Product.objects.filter(is_active=True).select_related('category')
    
    category_slug = request.GET.get('category')
    roast = request.GET.get('roast')
    search = request.GET.get('q')

    if category_slug:
        products = products.filter(category__slug=category_slug)
    if roast:
        products = products.filter(roast_level=roast)
    if search:
        products = products.filter(title__icontains=search) | products.filter(flavor_notes__icontains=search)

    context = {
        'categories': categories,
        'products': products,
        'selected_category': category_slug,
        'selected_roast': roast or '',
        'search_query': search or ''
    }
    return render(request, 'shop/index.html', context)

def product_detail_view(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    related_products = Product.objects.filter(category=product.category, is_active=True).exclude(id=product.id)[:4]
    
    context = {
        'product': product,
        'related_products': related_products
    }
    return render(request, 'shop/detail.html', context)
