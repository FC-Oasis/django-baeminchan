from django.db import models


class ParentCategory(models.Model):
    PARENT_CATEGORY_CHOICES = (
        ('side-dish', '밑반찬'),
        ('soup', '국,찌개'),
        ('main-courses', '메인반찬'),
        ('kids', '아이반찬'),
        ('set-of-side', '정기반찬'),
        ('fresh', '간편식'),
        ('refreshment', '간식'),
    )
    name = models.CharField(max_length=250, choices=PARENT_CATEGORY_CHOICES)
    image_url = models.URLField(blank=True)

    def __str__(self):
        return '{}'.format(self.get_name_display())


class Category(models.Model):
    parent_category = models.ForeignKey(ParentCategory, max_length=250, on_delete=models.CASCADE)
    name = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return '{} {}'.format(self.parent_category.name, self.name)
