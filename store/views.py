
from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime

from .models import *


# Create your views here.
#view for home page

def store(request):
    try:
        if request.user.is_authenticated:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items
        else:
            items = []
            order = {'get_cart_total':0, 'get_cart_items':0,'shipping': False}
            cartItems = order['get_cart_items']
    except Customer.DoesNotExist:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0,'shipping': False}
        cartItems = order['get_cart_items']

    products = Product.objects.all()
    context = {'products': products,'cartItems':cartItems}
    return render(request,'store/index.html',context)






def cart(request):
    try:
        if request.user.is_authenticated:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items
        else:
            items = []
            order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
            cartItems = order['get_cart_items']
    except Customer.DoesNotExist:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)


def checkout(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0,'shipping':False}
        cartItems =order['get_cart_items']

    context = {'items': items, 'order': order,'cartItems':cartItems}

    return render(request, 'store/checkout.html', context)


def login(request):
    context = {}
    return render(request, 'store/login.html', context)


def jsonsonResponse(param, safe):
    pass


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('productId:', productId)

    # Check if the user is authenticated
    if request.user.is_authenticated:
        try:
            customer = request.user.customer
        except Customer.DoesNotExist:
            # Create a Customer object for the user if it doesn't exist
            customer = Customer.objects.create(user=request.user)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        # For anonymous users, use session to store the cart
        order = request.session.get('order')
        if order is None:
            order = {'cart': {}}
            request.session['order'] = order

    product = Product.objects.get(id=productId)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    if orderItem.quantity <= 0:
        orderItem.delete()
    else:
        orderItem.save()

    # Update the session with the new cart data for anonymous users
    if not request.user.is_authenticated:
        request.session['order'] = order

    return JsonResponse('Item was added', safe=False)
# from django.views.decorators.csrf import csrf_exempt
# @csrf_exempt

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
        order.save()

        if order.shipping == True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],

            )



    else:
        print('User is not logged in')

    return JsonResponse('Payment complete!', safe=False)
