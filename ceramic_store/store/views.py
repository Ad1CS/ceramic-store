# store/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Category, Product, Cart, CartItem


def get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key)
    return cart


def home(request):
    products = Product.objects.filter(is_featured=True)
    categories = Category.objects.all()
    return render(request, 'store/home.html', {'products': products, 'categories': categories})


def product_list(request):
    products = Product.objects.filter(in_stock=True)
    categories = Category.objects.all()
    category_slug = request.GET.get('category')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    if min_price:
        products = products.filter(price__gte=min_price)

    if max_price:
        products = products.filter(price__lte=max_price)

    return render(request, 'store/product_list.html',
                  {'products': products, 'categories': categories})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, in_stock=True)
    return render(request, 'store/product_detail.html', {'product': product})


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_or_create_cart(request)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f'{product.name} added to your cart')
    return redirect('cart_detail')


def cart_detail(request):
    cart = get_or_create_cart(request)
    cart_items = CartItem.objects.filter(cart=cart)
    total = sum(item.get_total() for item in cart_items)

    return render(request, 'store/cart.html', {
        'cart_items': cart_items,
        'total': total
    })


def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.delete()
    messages.success(request, 'Item removed from cart')
    return redirect('cart_detail')


def update_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    quantity = int(request.POST.get('quantity', 1))

    if quantity > 0:
        item.quantity = quantity
        item.save()
    else:
        item.delete()

    return redirect('cart_detail')