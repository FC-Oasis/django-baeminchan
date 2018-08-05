from django.contrib import admin


from .models import Product, Category, ParentCategory


admin.site.register(Category)
admin.site.register(ParentCategory)


class ProductAdmin(admin.ModelAdmin):
    field = ['name', 'description', 'price', ]


admin.site.register(Product)


