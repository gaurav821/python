import json
from .models import *

def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
        
    print('cart:',cart)
    item = []
    order = {'get_cart_total' : 0 , 'get_cart_item' :0,'shiping' : False}
    cartItem = order['get_cart_item']

    for i in cart:
        try:
            cartItem += cart[i]['quantity']

            product = Product.objects.get(id=i)
            total = (product.prize * cart[i]["quantity"])

            order['get_cart_total'] += total
            order['get_cart_item'] += cart[i]["quantity"]

            ite = {

                'product' :{
                'id' : product.id,
                'name' : product.name,
                'prize' : product.prize,
                'imageURL' : product.imageURL

                },

                'quantity': cart[i]["quantity"],
                'get_total' : total

                }
            item.append(ite)

            if product.digital == False:
                order['shiping'] = True

        except:
            pass
    return {'cartItem' : cartItem,'order': order,'item':item}

def cartDate(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False )
        item = order.orderitem_set.all()
        cartItem = order.get_cart_item

    else:
        cookieData = cookieCart(request)
        cartItem = cookieData['cartItem']
        order = cookieData['order']
        item = cookieData['item']
    return {'cartItem' : cartItem,'order': order,'item':item}    

def guestOrder(request,data):
    
    print('user isnt log in')

    print('cookies:',request.COOKIES)
    name = data['form']['name']
    email = data['form']['email']

    cartData = cookieCart(request)
    item = cartData['item']

    customer,created = Customer.objects.get_or_create(email=email,)
    customer.name = name
    customer.save()

    order = Order.objects.create(customer=customer,complete=False)

    for ite in item:
        product = Product.objects.get(id=ite['product']['id'])

        orderIte = orderItem.objects.create(
            product=product,
            order=order,
            quantity = ite['quantity']
        )


    return customer,order