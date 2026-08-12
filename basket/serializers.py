from rest_framework import serializers
from .models import Basket, BasketItem


class BasketItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasketItem
        fields = ['id', 'product', 'quantity', 'price']


class BasketSerializer(serializers.ModelSerializer):
    items = BasketItemSerializer(many=True, read_only=True)

    class Meta:
        model = Basket
        fields = ['id', 'user', 'date', 'status', 'total_price', 'items']
        