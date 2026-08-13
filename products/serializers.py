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
    category = serializers.CharField(source="category.name", read_only=True)
    final_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    in_stock = serializers.BooleanField(read_only=True)

    class Meta:
        model = Product
        fields = ["id", "name", "slug", "category", "price", "discount_price",
                  "final_price", "unit", "image", "in_stock", "is_daily_listing"]


class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    extra_images = ProductImageSerializer(many=True, read_only=True)
    final_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    in_stock = serializers.BooleanField(read_only=True)
    vendor = serializers.CharField(source="vendor.username", read_only=True)

    class Meta:
        model = Product
        fields = ["id", "name", "slug", "description", "category", "vendor",
                  "price", "discount_price", "final_price", "unit",
                  "stock", "in_stock", "image", "extra_images",
                  "is_daily_listing", "is_active", "created_at", "updated_at"]


class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["category", "name", "description", "price", "discount_price",
                  "unit", "stock", "image", "is_daily_listing", "is_active"]

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than 0.")
        return value

    def validate(self, data):
        discount = data.get("discount_price")
        price = data.get("price")
        if discount and price and discount >= price:
            raise serializers.ValidationError("Discount price must be lower than regular price.")
        return data