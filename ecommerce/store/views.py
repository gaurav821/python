from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
from .models import *
from .utils import cookieCart,cartDate,guestOrder
# Create your views here.

def store(request):
    data = cartDate(request)
        
   
    cartItem = data['cartItem']
  
    
   
    products = Product.objects.all()
    context = {'products' : products , 'cartItem' :cartItem,}
    return render(request,'store/store.html',context)


def cart(request):
    data = cartDate(request)
        
   
    cartItem = data['cartItem']
    order = data['order']
    item = data['item']


    context = {'item' : item ,'order' : order ,'cartItem' :cartItem,'shiping':False}
    return render(request,'store/cart.html',context)


def checkout(request):
    data = cartDate(request)
        
   
    cartItem = data['cartItem']
    order = data['order']
    item = data['item']


    context = {'item' : item ,'order' : order, 'cartItem' :cartItem}
    return render(request,'store/checkout.html',context)


def updateitem(request):
    data = json.loads(request.body)
    productid = data['productid']
    action = data['action']
    print('action:',action)
    print('product:',productid)
    
    
    customer = request.user.customer
    product = Product.objects.get(id=productid)
    order, created = Order.objects.get_or_create(customer=customer,complete=False)

    orderIte, created =orderItem.objects.get_or_create(order=order,product=product) 
    

    if action =='add':
        orderIte.quantity=orderIte.quantity + 1

    elif action =='remove':
        orderIte.quantity=orderIte.quantity - 1

    orderIte.save()

    if orderIte.quantity <= 0:
        orderIte.delete()


   
    return JsonResponse('item is added',safe=False)    

def procesorder(request):
    transection_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False)



    else:
        customer,order =guestOrder(request,data)
        



    total = float(data['form']['total'])
    order.transection_id = transection_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()  

    if order.shiping == True:
        ShippingAddress.objects.create(
        customer=customer,
        order=order,
        address = data['shiping']['address'],
        city = data['shiping']['city'],
        state = data['shiping']['state'],
        zip_code= data['shiping']['zipcode'],

        )


    return JsonResponse('payment completed',safe=False)
      