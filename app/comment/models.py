from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from product.models import Product


class Comment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
    )
    content = models.CharField(
        max_length=255,
        blank=True,
    )
    rating = models.PositiveSmallIntegerField(
        default=0,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(0),
        ],
    )
    created_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return f'{self.product.name}: {self.content}, rating: {self.rating} by {self.user}'

    class Meta:
        ordering = ('-created_at',)
