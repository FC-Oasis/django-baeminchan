from django.db import models


class ParentCategory(models.Model):
    PARENT_CATEGORY_CHOICES = (
        ('PARENT_CATEGORY_side', '밑반찬'),
        ('PARENT_CATEGORY_soup', '국,찌개'),
        ('PARENT_CATEGORY_main', '메인반찬'),
        ('PARENT_CATEGORYSIDE_child', '아이반찬'),
        ('PARENT_CATEGORYSIDE_regular', '정기반찬'),
        ('PARENT_CATEGORYSIDE_simple', '간편식'),
        ('PARENT_CATEGORYSIDE_snack', '간식'),
        ('PARENT_CATEGORYSIDE_brand', '브랜드관'),

    )
    name = models.CharField(max_length=250, choices=PARENT_CATEGORY_CHOICES)


class Category(models.Model):
    parent_category = models.ForeignKey(ParentCategory, max_length=250, on_delete=models.CASCADE)
    name = models.CharField(max_length=250, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='category', blank=True)

    def __str__(self):
        return '{}'.format(self.name)


