from django.shortcuts import render
from django.shortcuts import get_object_or_404
from products.models import products


def product_list(request):
    # 1. Capture both parameters from the URL
    selected_type = request.GET.get('type')
    search_query = request.GET.get('product') # The name from your search input
    
    # 2. Start with the base queryset
    all_products = products.objects.all().order_by('-date_added')

    # 3. Apply Type filter if it exists
    if selected_type:
        all_products = all_products.filter(type=selected_type)

    # 4. Apply Name search if it exists (__icontains makes it case-insensitive)
    if search_query:
        all_products = all_products.filter(product__icontains=search_query)

    context = {
        'all_products': all_products,
        'active_filter': selected_type,
        'search_query': search_query, # Pass back to template to keep the input filled
        'categories': products.PRODUCT_TYPE_CHOICE
    }
    return render(request, 'pro_list.html', context, )

def pro_det(request, pro_id):
  pros = get_object_or_404(products, id=pro_id)
  return render(request, 'pro_detail.html', {'pros' : pros})


