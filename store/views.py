from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from . models import Product, ReviewRating, ProductGallery
from classification.models import Classification
from carts.models import CartItem
from carts.views import _cart_id
from django.db.models import Q
from . forms import ReviewForm
from django.contrib import messages
from orders.models import OrderProduct
from accounts.models import UserProfile


# Main store page with all products
def store(request, classification_slug=None):
    classifications =None
    products = None
    if classification_slug != None:
        classifications = get_object_or_404(Classification, slug=classification_slug)
        products = Product.objects.filter(classification=classifications, is_available=True)
        paginator = Paginator(products, 2)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(products, 12)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()

    context = {'products': paged_products, 'product_count': product_count}

    return render(request, 'store/store.html', context)


# Product specific detail
def product_detail(request, classification_slug, product_slug):
    try:
        single_product = Product.objects.get(classification__slug=classification_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
    except Exception as e:
        raise e

    # Checking if the user has purchased the product in question
    if request.user.is_authenticated:
        try:
            orderProduct = OrderProduct.objects.filter(user=request.user, product_id=single_product.id).exists()
        except OrderProduct.DoesNotExist:
            orderProduct = None
    else:
        orderProduct = None

    # Get Reviews
    reviews = ReviewRating.objects.filter(product_id=single_product.id, status=True)

    # Get the product gallery

    products_gallery = ProductGallery.objects.filter(product_id=single_product.id)
    userprofile = None
    try:
        userprofile = UserProfile.objects.get(user_id=request.user.id)
    except:
        messages.error(request, 'Login first ')
        return redirect('login')

    context = {
    'single_product': single_product, 'in_cart': in_cart,
     'orderProduct': orderProduct, 'reviews': reviews,
     'products_gallery': products_gallery, 'userprofile': userprofile
     }

    return render(request, 'store/product_detail.html', context)


def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword)| Q(product_name__icontains=keyword) |
             Q(product_color__icontains=keyword)| Q(drive__icontains=keyword) | Q(transmission__icontains=keyword) | Q(fuel__icontains=keyword) |
              Q(product_year__icontains=keyword))
            product_count = products.count()
    context = {'products': products, 'product_count': product_count}
    return render(request, 'store/store.html', context)


def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            review = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=review)
            form.save()
            messages.success(request, 'Thank you for reviewing. Your review has been updated!')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank you for reviewing. Your review has been submitted!')
                return redirect(url)
