from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Product, Order, OrderItem
from django.templatetags.static import static as static_url
from django.contrib import messages


def home(request):
    products = Product.objects.all()
    products_data = []
    for p in products:
        if p.image:
            img = p.image.url
        else:
            # fallback to a static image named by slug
            img = static_url(f'images/{p.slug}.svg')
        products_data.append({'product': p, 'image_url': img})
    return render(request, 'home.html', {'products_data': products_data})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if product.image:
        img = product.image.url
    else:
        img = static_url(f'images/{product.slug}.svg')
    return render(request, 'product_detail.html', {'product': product, 'image_url': img})


def _get_cart(request):
    return request.session.get('cart', {})


def _save_cart(request, cart):
    request.session['cart'] = cart
    request.session.modified = True


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = _get_cart(request)
    pid = str(product.id)
    cart[pid] = cart.get(pid, 0) + int(request.POST.get('quantity', 1))
    _save_cart(request, cart)
    messages.success(request, f'Added {product.name} to cart.')
    return redirect('cart')


def cart(request):
    cart = _get_cart(request)
    products = []
    total = 0
    for pid, qty in cart.items():
        try:
            p = Product.objects.get(id=pid)
        except Product.DoesNotExist:
            continue
        item_total = p.price * qty
        products.append({'product': p, 'quantity': qty, 'total': item_total})
        total += item_total
    return render(request, 'cart.html', {'cart_items': products, 'total': total})


def update_cart(request):
    if request.method == 'POST':
        cart = _get_cart(request)
        for pid, qty in request.POST.items():
            if not pid.startswith('qty_'):
                continue
            prod_id = pid.split('_', 1)[1]
            try:
                q = int(qty)
            except ValueError:
                q = 0
            if q <= 0:
                cart.pop(prod_id, None)
            else:
                cart[prod_id] = q
        _save_cart(request, cart)
    return redirect('cart')


def checkout(request):
    cart = _get_cart(request)
    if not cart:
        messages.info(request, 'Your cart is empty.')
        return redirect('home')

    products = []
    total = 0
    for pid, qty in cart.items():
        try:
            p = Product.objects.get(id=pid)
        except Product.DoesNotExist:
            continue
        item_total = p.price * qty
        products.append({'product': p, 'quantity': qty, 'total': item_total})
        total += item_total

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            full_name=full_name,
            email=email,
            address=address,
        )
        for entry in products:
            OrderItem.objects.create(
                order=order,
                product=entry['product'],
                price=entry['product'].price,
                quantity=entry['quantity'],
            )
        # clear cart
        request.session['cart'] = {}
        messages.success(request, 'Order placed successfully.')
        return redirect('order_success', order_id=order.id)

    return render(request, 'checkout.html', {'cart_items': products, 'total': total})


def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order_success.html', {'order': order})


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')
