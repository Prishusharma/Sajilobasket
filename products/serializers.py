from rest_framework import serializers
from .models import Category, Product, ProductImage


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "image"]


class ProductListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing products (grid/search page)"""
    category = serializers.CharField(source="category.name", read_only=True)
    final_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )
    in_stock = serializers.BooleanField(read_only=True)

    class Meta:
        model = Product
        fields = [
            "id", "name", "slug", "category",
            "price", "discount_price", "final_price",
            "image", "in_stock",
        ]


class ProductDetailSerializer(serializers.ModelSerializer):
    """Full serializer for single product page"""
    category = CategorySerializer(read_only=True)
    extra_images = ProductImageSerializer(many=True, read_only=True)
    final_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )
    in_stock = serializers.BooleanField(read_only=True)

    class Meta:
        model = Product
        fields = [
            "id", "name", "slug", "description", "category",
            "price", "discount_price", "final_price",
            "stock", "in_stock", "image", "extra_images",
            "is_active", "created_at", "updated_at",
        ]


class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    """Used by admin/staff to create or update a product"""
    class Meta:
        model = Product
        fields = [
            "category", "name", "description",
            "price", "discount_price", "stock", "image", "is_active",
        ]

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than 0.")
        return value

    def validate(self, data):
        discount = data.get("discount_price")
        price = data.get("price")
        if discount and price and discount >= price:
            raise serializers.ValidationError(
                "Discount price must be lower than regular price."
            )
        return data