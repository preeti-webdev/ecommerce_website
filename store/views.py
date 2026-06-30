from django.shortcuts import render, redirect, get_object_or_404
from .models import Product,Wishlist,Product, Cart, Order, OrderItem
from .forms import RegisterForm
from django.contrib.auth import logout
from django.db.models import Q
from django.contrib.auth.decorators import login_required


def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'store/product_detail.html', {'product': product})


def add_to_cart(request, id):
    product = get_object_or_404(Product, id=id)

    cart_item, created = Cart.objects.get_or_create(
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')


def cart(request):
    cart_items = Cart.objects.all()

    total = sum(
        item.product.price * item.quantity
        for item in cart_items
    )

    return render(
        request,
        'store/cart.html',
        {
            'cart_items': cart_items,
            'total': total
        }
    )


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')

    else:
        form = RegisterForm()

    return render(
        request,
        'store/register.html',
        {'form': form}
    )


@login_required
def add_to_cart(request, id):
    product = get_object_or_404(Product, id=id)

    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')


@login_required
def cart(request):
    cart_items = Cart.objects.filter(
        user=request.user
    )

    total = sum(
        item.product.price * item.quantity
        for item in cart_items
    )

    return render(
        request,
        'store/cart.html',
        {
            'cart_items': cart_items,
            'total': total
        }
    )


def product_list(request):
    query = request.GET.get('q')

    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )
    else:
        products = Product.objects.all()

    return render(
        request,
        'store/product_list.html',
        {'products': products}
    )



@login_required
def place_order(request):

    cart_items = Cart.objects.filter(
        user=request.user
    )

    total = sum(
        item.product.price * item.quantity
        for item in cart_items
    )

    order = Order.objects.create(
        user=request.user,
        total_amount=total
    )

    for item in cart_items:

        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )

    cart_items.delete()

    return redirect('my_orders')


@login_required
def my_orders(request):

    orders = Order.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(
        request,
        'store/my_orders.html',
        {'orders': orders}
    )

@login_required
def update_cart(request, id):

    cart_item = get_object_or_404(
        Cart,
        id=id,
        user=request.user
    )

    quantity = int(
        request.POST.get('quantity')
    )

    if quantity > 0:
        cart_item.quantity = quantity
        cart_item.save()

    return redirect('cart')


@login_required
def remove_from_cart(request, id):

    cart_item = get_object_or_404(
        Cart,
        id=id,
        user=request.user
    )

    cart_item.delete()

    return redirect('cart')

@login_required
def add_to_wishlist(request, id):

    product = get_object_or_404(Product, id=id)

    Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )

    return redirect('wishlist')

@login_required
def wishlist(request):

    items = Wishlist.objects.filter(
        user=request.user
    )

    return render(
        request,
        'store/wishlist.html',
        {'items': items}
    )

def logout_view(request):
    logout(request)
    return redirect('/')