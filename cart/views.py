from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from mydrone.models import Drone, Category
from .cart import Cart
from .forms import CartAddDroneForm

category_list = Category.objects.all()

@require_POST
def cart_add(request, drone_id):
    cart = Cart(request)
    drone = get_object_or_404(Drone, id=drone_id)
    form = CartAddDroneForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(drone=drone,
                 quantity=cd['quantity'],
                 override_quantity=cd['override'])
    return redirect('cart:cart_detail')


@require_POST
def cart_remove(request, drone_id):
    cart = Cart(request)
    drone = get_object_or_404(Drone, id=drone_id)
    cart.remove(drone)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddDroneForm(initial={'quantity': item['quantity'],
                                                                   'override': True})
    username = request.session.get('username', 0)                                                               
    return render(request, 'cart/detail.html', {'cart': cart, 
                                                'username': username,
                                                'categories': category_list})
