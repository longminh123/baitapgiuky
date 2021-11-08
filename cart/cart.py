from decimal import Decimal
from django.conf import settings
from mydrone.models import Drone


class Cart(object):

    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        """
        Iterate over the items in the cart and get the drones
        from the database.
        """
        drone_ids= self.cart.keys()
        # get the drones objects and add them to the cart
        drones = Drone.objects.filter(id__in=drone_ids)

        cart = self.cart.copy()
        for drone in drones:
            cart[str(drone.id)]['drone'] = drone

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Count all items in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def add(self, drone, quantity=1, override_quantity=False):
        """
        Add a drone to the cart or update its quantity.
        """
        drone_id = str(drone.id)
        if drone_id not in self.cart:
            self.cart[drone_id] = {'quantity': 0,
                                      'price': str(drone.price)}
        if override_quantity:
            self.cart[drone_id]['quantity'] = quantity
        else:
            self.cart[drone_id]['quantity'] += quantity
        self.save()

    def save(self):
        # mark the session as "modified" to make sure it gets saved
        self.session.modified = True

    def remove(self, drone):
        """
        Remove a drone from the cart.
        """
        drone_id = str(drone.id)
        if drone_id in self.cart:
            del self.cart[drone_id]
            self.save()

    def clear(self):
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
