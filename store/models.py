from django.db import models
from classification.models import Classification
from django.urls import reverse

# Create your models here.

class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(max_length=500, blank=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    images = models.ImageField(upload_to='photos/products')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    classification = models.ForeignKey(Classification, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse('products_detail', args=[self.classification.slug, self.slug])

    def __str__(self):
        return self.product_name


class VariationManager(models.Manager):

    def colors(self):
        return super(VariationManager, self).filter(variation_class='color', is_active=True)

    def sizes(self):
        return super(VariationManager, self).filter(variation_class='size', is_active=True)


variation_class_choice = (
    ('color','color'),
    ('size', 'size'),
)


class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_class = models.CharField(max_length=100, choices=variation_class_choice)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)

    objects = VariationManager()

    def __unicode__(self):
        return self.product

    def __str__(self):
        return self.variation_value
