from django.db import models

class Specification(models.Model):
    type = models.CharField(max_length=100)
    size = models.CharField(max_length=100)
    power = models.CharField(max_length=100)
    voltage = models.CharField(max_length=100)
    frequency = models.CharField(max_length=100)
    speed = models.CharField(max_length=100)
    capacity_wood = models.CharField(max_length=100, blank=True, null=True)
    capacity_steel = models.CharField(max_length=100, blank=True, null=True)
    weight = models.CharField(max_length=100)
    supplied_in = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.type}'

class Category(models.Model):
    image = models.ImageField(upload_to='category/')
    name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.name

class Product(models.Model):
    image = models.ImageField(upload_to='products/')
    name = models.CharField(max_length=200)
    model = models.CharField(max_length=100)
    features = models.TextField()
    description = models.TextField()
    specification = models.ForeignKey(Specification, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return f'{self.name}'
    