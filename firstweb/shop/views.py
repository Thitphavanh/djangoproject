from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .models import Brand, Category, Product

PAGE_SIZE = 12

SORT_OPTIONS = {
    'newest': ('-created_at', 'ล่าสุด'),
    'price_asc': ('price', 'ราคา: ต่ำ - สูง'),
    'price_desc': ('-price', 'ราคา: สูง - ต่ำ'),
    'name_asc': ('name', 'ชื่อ: ก - ฮ'),
}


def _querystring(request, **overrides):
    params = request.GET.copy()
    params.pop('page', None)
    for key, value in overrides.items():
        if value:
            params[key] = value
        else:
            params.pop(key, None)
    return params.urlencode()


def product_list(request):
    query = request.GET.get('q', '').strip()
    category_name = request.GET.get('category', '').strip()
    brand_name = request.GET.get('brand', '').strip()
    sort_key = request.GET.get('sort', 'newest')
    if sort_key not in SORT_OPTIONS:
        sort_key = 'newest'

    products = Product.objects.select_related('brand', 'category').all()

    if query:
        products = products.filter(
            Q(name__icontains=query)
            | Q(description__icontains=query)
            | Q(brand__name__icontains=query)
        )

    if category_name:
        products = products.filter(category__name=category_name)

    if brand_name:
        products = products.filter(brand__name=brand_name)

    products = products.order_by(SORT_OPTIONS[sort_key][0])

    paginator = Paginator(products, PAGE_SIZE)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    elided_range = list(
        paginator.get_elided_page_range(page_obj.number, on_each_side=1, on_ends=1)
    ) if paginator.num_pages > 1 else []

    base_qs = _querystring(request)
    page_query_prefix = f'?{base_qs}&page=' if base_qs else '?page='

    categories = Category.objects.order_by('name')
    category_links = [
        {
            'name': 'ทั้งหมด',
            'url': '?' + _querystring(request, category=None),
            'active': not category_name,
        }
    ] + [
        {
            'name': category.name,
            'url': '?' + _querystring(request, category=category.name),
            'active': category.name == category_name,
        }
        for category in categories
    ]

    context = {
        'page_obj': page_obj,
        'products': page_obj.object_list,
        'categories': categories,
        'category_links': category_links,
        'brands': Brand.objects.order_by('name'),
        'query': query,
        'selected_category': category_name,
        'selected_brand': brand_name,
        'sort_key': sort_key,
        'sort_options': SORT_OPTIONS,
        'querystring': base_qs,
        'page_query_prefix': page_query_prefix,
        'elided_range': elided_range,
        'ellipsis': Paginator.ELLIPSIS,
        'total_count': paginator.count,
        'has_filters': bool(query or category_name or brand_name),
    }
    return render(request, 'shop/product_list.html', context)


def product_detail(request, pk):
    product = get_object_or_404(
        Product.objects.select_related('brand', 'category'), pk=pk
    )
    related_products = (
        Product.objects.filter(category=product.category)
        .exclude(pk=product.pk)
        .select_related('brand', 'category')
        .order_by('?')[:4]
    )
    spec_items = [part.strip() for part in product.description.split(',') if part.strip()]

    context = {
        'product': product,
        'related_products': related_products,
        'spec_items': spec_items,
    }
    return render(request, 'shop/product_detail.html', context)
