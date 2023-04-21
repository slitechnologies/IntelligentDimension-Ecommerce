from django.shortcuts import render, get_object_or_404
from . models import Product
from classification.models import Classification

# Main store page with all products
def store(request, classification_slug=None):
    classifications =None
    products = None
    if classification_slug != None:
        classifications = get_object_or_404(Classification, slug=classification_slug)
        products = Product.objects.filter(classification=classifications, is_available=True)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True)
        product_count = products.count()

    context = {'products': products, 'product_count': product_count}

    return render(request, 'store/store.html', context)

# Product specific detail
def product_detail(request, classification_slug, product_slug):
    try:
        single_product = Product.objects.get(classification__slug=classification_slug, slug=product_slug)
    except Exception as e:
        raise e
    context = {'single_product': single_product}
    return render(request, 'store/product_detail.html', context)
