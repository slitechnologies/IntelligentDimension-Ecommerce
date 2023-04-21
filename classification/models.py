from django.db import models
from django.urls import reverse


class Classification(models.Model):
    class_name = models.CharField(max_length=50, unique=True)
    #this is the url
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=255, blank=True)
    class_image = models.ImageField(upload_to='photos/classes', blank=True)

    class Meta:
        verbose_name = 'classification'
        verbose_name_plural = 'classifications'


    def get_url(self):
        return reverse('products_by_class', args=[self.slug])


    def __str__(self):
        return self.class_name
