from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_basket, name='get-basket'),
    path('add/', views.add_to_basket, name='add-to-basket'),
    path('items/<int:item_id>/', views.update_basket_item, name='update-basket-item'),
    path('items/<int:item_id>/remove/', views.remove_from_basket, name='remove-from-basket'),
    path('confirm/', views.confirm_basket, name='confirm-basket'),
]