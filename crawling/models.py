from django.db import models


class BmcDataMuchim(models.Model):
    title = models.CharField(max_length=50)
    price = models.CharField(max_length=50, null=False)
    image = models.ImageField(default='media')

    def __str__(self):
        return self.title
