from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from .models import Product, CartItem, Order
# Create your views here.

def home(request):
    products = Product.objects.all()
    featured_product = products.filter(featured = True)
    number_product_in_cart = None
    total_in_cart = None
    if request.user.is_authenticated:
        cart = request.user.customer.cart
        number_product_in_cart = len(cart.cartitem_set.all())
        total_in_cart = sum([cartitem.total for cartitem in cart.cartitem_set.all()])
    return render(request, 'shop/index.html', 
                  {'products':featured_product, 
                   'request':request, 
                   'numprd':number_product_in_cart, 
                   'total': total_in_cart})

def products(request):
    products = Product.objects.all()
    perpage = request.GET.get('perpage', 9)
    page = request.GET.get('page', 1)
    order = request.GET.get('order')
    category = request.GET.get('category')

    filter_params = {}
    filter_params['page'] = page
    filter_params['order'] = order
    filter_params['category'] = category
    
    if category:
        products = products.filter(category__icontains=category)
    if order == 'price':
        products = products.order_by('price')
    paginator = Paginator(products, per_page=perpage)
    page_products = paginator.get_page(page)

    number_product_in_cart = None
    total_in_cart = None
    if request.user.is_authenticated:
        cart = request.user.customer.cart
        number_product_in_cart = len(cart.cartitem_set.all())
        total_in_cart = sum([cartitem.total for cartitem in cart.cartitem_set.all()])

    return render(request, 'shop/products.html', {'products':page_products,
                                                    'paginator':paginator,
                                                    'filter':filter_params,
                                                    'request':request, 
                                                    'numprd':number_product_in_cart,
                                                    'total': total_in_cart})

def detail(request, id):
    product = Product.objects.get(id=id)
    category = product.category
    related_products = Product.objects.filter(category=category).exclude(name=product.name)
    if len(related_products) > 4:
        related_products = related_products[:4]

    number_product_in_cart = None
    total_in_cart = None
    if request.user.is_authenticated:
        cart = request.user.customer.cart
        number_product_in_cart = len(cart.cartitem_set.all())
        total_in_cart = sum([cartitem.total for cartitem in cart.cartitem_set.all()])

    return render(request, 'shop/detail.html', {'product':product, 
                                                'related_products':related_products,
                                                'request':request, 
                                                'numprd':number_product_in_cart, 
                                                'total': total_in_cart})



@login_required()
def view_cart(request):
    cart = request.user.customer.cart
    if request.method == 'POST':
        for item in cart.cartitem_set.all():
            item.quantity = int(request.POST.get(item.product.name))
            item.save()
        
    total_item = sum([cartitem.quantity for cartitem in cart.cartitem_set.all()])
    total_money = sum([cartitem.total for cartitem in cart.cartitem_set.all()])

    number_product_in_cart = len(cart.cartitem_set.all())
    return render(request, 'shop/cart.html', {'cart':cart, 
                                              'total_item':total_item, 
                                              'total':total_money,
                                              'request':request, 
                                              'numprd':number_product_in_cart,})

@login_required()
def add_to_cart(request, product_id):
    cart = request.user.customer.cart
    quantity = None
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity'))
    if product_id in [item.product.id for item in cart.cartitem_set.all()]:
        item_in_cart = cart.cartitem_set.get(product_id=product_id)
        if quantity:
            item_in_cart.quantity += quantity
        else:
            item_in_cart.quantity += 1
        item_in_cart.save()
        return redirect(reverse('shop:view_cart'))
    product = Product.objects.get(id=product_id)
    if quantity:
        cart_item = CartItem(product=product, cart=cart, quantity=quantity)
    else:
        cart_item = CartItem(product=product, cart=cart)
    cart_item.save()
    return redirect(reverse('shop:view_cart'))


@login_required()
def delete_from_cart(request, product_id):
    cart = request.user.customer.cart
    del_item = cart.cartitem_set.get(product_id=product_id)
    del_item.delete()
    return redirect(reverse('shop:view_cart'))


@login_required
def checkout(request):
    cart = request.user.customer.cart
    total_in_cart = sum([item.total for item in cart.cartitem_set.all()])
    number_product_in_cart = len(cart.cartitem_set.all())
    if request.method == 'POST':
        username = request.user.username
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            name_to_deliver = request.POST.get('name')
            phone_to_deliver = request.POST.get('phone')
            address = request.POST.get('address')
            note = request.POST.get('note')
            order = Order(customer=request.user.customer, 
                          address=address, 
                          name_to_deliver=name_to_deliver,
                          phone_to_deliver=phone_to_deliver,
                          total = total_in_cart)
            if note:
                order.note = note
            order.save()
            for item in cart.cartitem_set.all():
                item.order = order
                item.cart = None # don't delete item because order referent to them
                item.save()
            return render(request, 'shop/success_od.html', {'order':order, 
                                                            'total':0, 
                                                            'total_money':total_in_cart,
                                                            'request':request, 
                                                            'numprd':0})
        else:
            return render(request, 'shop/checkout.html', {'cart':cart, 
                                                          'total':total_in_cart, 
                                                          'request':request,
                                                          'numprd':number_product_in_cart})
        
    return render(request, 'shop/checkout.html', {'cart':cart, 
                                                  'total':total_in_cart, 
                                                  'request':request, 
                                                  'numprd':number_product_in_cart})