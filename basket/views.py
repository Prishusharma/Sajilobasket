from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Basket, BasketItem
from .serializers import BasketSerializer
from products.models import Product


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_basket(request):
    basket, created = Basket.objects.get_or_create(
        user=request.user,
        status='active'
    )

    serializer = BasketSerializer(basket)

    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_basket(request):

    product_id = request.data.get('product')
    quantity = request.data.get('quantity', 1)

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response(
            {'error': 'Product not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    if not product.available:
        return Response(
            {'error': 'Product is not available'},
            status=status.HTTP_400_BAD_REQUEST
        )

    basket, created = Basket.objects.get_or_create(
        user=request.user,
        status='active'
    )

    item, created = BasketItem.objects.get_or_create(
        basket=basket,
        product=product,
        defaults={
            'quantity': quantity,
            'price': product.price
        }
    )

    if not created:
        item.quantity += int(quantity)
        item.save()

    update_total(basket)

    serializer = BasketSerializer(basket)

    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_basket_item(request, item_id):

    try:
        item = BasketItem.objects.get(
            id=item_id,
            basket__user=request.user
        )
    except BasketItem.DoesNotExist:
        return Response(
            {'error': 'Basket item not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    quantity = request.data.get('quantity')

    if quantity is None:
        return Response(
            {'error': 'Quantity is required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    item.quantity = quantity
    item.save()

    update_total(item.basket)

    serializer = BasketSerializer(item.basket)

    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_from_basket(request, item_id):

    try:
        item = BasketItem.objects.get(
            id=item_id,
            basket__user=request.user
        )
    except BasketItem.DoesNotExist:
        return Response(
            {'error': 'Basket item not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    basket = item.basket

    item.delete()

    update_total(basket)

    serializer = BasketSerializer(basket)

    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def confirm_basket(request):

    try:
        basket = Basket.objects.get(
            user=request.user,
            status='active'
        )
    except Basket.DoesNotExist:
        return Response(
            {'error': 'No active basket found'},
            status=status.HTTP_404_NOT_FOUND
        )

    if not basket.items.exists():
        return Response(
            {'error': 'Basket is empty'},
            status=status.HTTP_400_BAD_REQUEST
        )

    basket.status = 'confirmed'
    basket.save()

    serializer = BasketSerializer(basket)

    return Response(serializer.data)


def update_total(basket):

    total = sum(
        item.price * item.quantity
        for item in basket.items.all()
    )

    basket.total_price = total
    basket.save()