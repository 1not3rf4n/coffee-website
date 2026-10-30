from django.shortcuts import render
from apps.menu.models import MenuCategory, MenuItem

def menu_view(request):
    categories = MenuCategory.objects.filter(is_active=True).order_by('display_order')
    items = MenuItem.objects.filter(is_active=True, category__is_active=True).select_related('category')
    
    category_slug = request.GET.get('category')
    search_query = request.GET.get('q')
    temp_filter = request.GET.get('temp')
    table_num = request.GET.get('table')

    if category_slug:
        items = items.filter(category__slug=category_slug)
    if search_query:
        items = items.filter(title__icontains=search_query) | items.filter(description__icontains=search_query)
    if temp_filter in ['hot', 'cold']:
        items = items.filter(temperature=temp_filter)

    context = {
        'categories': categories,
        'items': items,
        'selected_category': category_slug,
        'search_query': search_query or '',
        'temp_filter': temp_filter or '',
        'table_num': table_num or ''
    }
    return render(request, 'menu.html', context)
