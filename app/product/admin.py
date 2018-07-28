from django.contrib import admin


from .models import Product, Category


class CategoryAdmin(admin.ModelAdmin):
    field = ['name', 'description', 'image']


admin.site.register(Category)


class ProductAdmin(admin.ModelAdmin):
    field = ['name', 'description', 'price', ]


admin.site.register(Product)


