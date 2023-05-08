from django.shortcuts import render, redirect
from carts.models import CartItem
from .forms import OrderForm
from . models import Order, Payment, OrderProduct
from store.models import Product
import datetime
import json

from django.http import HttpResponse


def payments(request):
    body = json.loads(request.body)
    order = Order.objects.get(user=request.user, is_ordered=False, order_number=body['orderId'])

    # store transaction details inside Payment model

    payment = Payment(
        user = request.user,
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        amount_paid = order.order_total,
        status = body['status'],
    )

    payment.save()
    order.payment = payment
    order.is_ordered = True
    order.save()

    # move cart items to Order Products table
    cart_items = CartItem.objects.filter(user=request.user)

    for item in cart_items:
        orderProduct = OrderProduct()
        orderProduct.order_id = order.id
        orderProduct.payment = payment
        orderProduct.user_id = request.user.id
        orderProduct.product_id = item.product_id
        orderProduct.quantity = item.quantity
        orderProduct.product_price = item.product.price
        orderProduct.ordered = True
        orderProduct.save()

        cart_item = CartItem.objects.get(id=item.id)
        product_variation = cart_item.variations.all()
        orderProduct = OrderProduct.objects.get(id=orderProduct.id)
        orderProduct.variations.set(product_variation)
        orderProduct.save()

        # reduce the quantity of the sold products from the inventory
        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()

    # clear cart

    CartItem.objects.filter(user=request.user).delete()


    # send order received email to customer
    # send order number and transaction id back to sendData() method via JsonResponse
    return render(request, 'orders/payments.html')


def place_order(request, total=0, quantity=0):
    current_user = request.user

    # if cart count is less than or equal to zero redirect the user to store page

    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')


    grand_total = 0
    tax = 0

    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (2 * total) / 100
    grand_total = total + tax

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # storing all the billing information inside order table
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone_number = form.cleaned_data['phone_number']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')

            data.save()

            # Generate order number
            yr =  int(datetime.date.today().strftime('%Y'))
            dt =  int(datetime.date.today().strftime('%d'))
            mt =  int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime('%Y%m%d')

            # concatenate current_date and order_id to make oder phone_number
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)

            context = {'order': order, 'cart_items': cart_items,
                        'tax': tax, 'total': total, 'grand_total': grand_total
            }
            return render(request, 'orders/payments.html', context)
        else:
            return redirect('checkout')
