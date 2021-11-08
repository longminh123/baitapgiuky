from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add/add/(?P<drone_id>[0-9]+)/$', views.cart_add, name='cart_add'),
    path('remove/(?P<drone_id>[0-9]+)/$',
         views.cart_remove, name='cart_remove'),
]
