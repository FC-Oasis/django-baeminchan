from rest_framework import serializers
from .models import ParentCategory, Category, Product, ProductImage


class ParentCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ParentCategory
        fields = (
            'name',
            'image_url',
        )


class CategorySerializer(serializers.ModelSerializer):
    parent_category = ParentCategorySerializer()

    class Meta:
        model = Category
        fields = (
            'name',
            'parent_category'
        )


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = (
            'image_url',
        )


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    productimage_set = ProductImageSerializer(many=True)

    class Meta:
        model = Product
        fields = '__all__'
