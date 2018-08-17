from rest_framework import serializers, permissions
from .models import ParentCategory, Category, Product, ProductImage


class ParentCategorySerializer(serializers.ModelSerializer):
    permission_classes = (
        permissions.AllowAny,
    )

    class Meta:
        model = ParentCategory
        fields = (
            'name',
            'image_url',
        )


class CategorySerializer(serializers.ModelSerializer):
    parent_category = ParentCategorySerializer()
    permission_classes = (
        permissions.AllowAny,
    )

    class Meta:
        model = Category
        fields = (
            'name',
            'parent_category'
        )


class ProductImageSerializer(serializers.ModelSerializer):
    permission_classes = (
        permissions.AllowAny,
    )

    class Meta:
        model = ProductImage
        fields = (
            'image_url',
        )


class RelatedProductSerializer(serializers.ModelSerializer):
    permission_classes = (
        permissions.AllowAny,
    )

    class Meta:
        model = Product
        fields = (
            'id',
            'raw_name',
            'description',
            'price',
            'discount_rate',
            'sale_price',
            'thumbnail_url',
        )


class ProductSerializer(serializers.ModelSerializer):
    related_products = RelatedProductSerializer(many=True)
    category = CategorySerializer()
    productimage_set = ProductImageSerializer(many=True)
    permission_classes = (
        permissions.AllowAny,
    )

    class Meta:
        model = Product
        fields = '__all__'


class ProductSimpleSerializer(ProductSerializer):
    productimage_set = None

    class Meta:
        model = Product
        fields = (
            'id',
            'raw_name',
            'description',
            'price',
            'discount_rate',
            'sale_price',
            'thumbnail_url',
        )
