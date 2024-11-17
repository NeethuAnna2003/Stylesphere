from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    image = models.ImageField(upload_to='category_images/', null=True, blank=True)

    def __str__(self):
        return self.name

class Clothes(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='clothes_images/')

    def _str_(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # ForeignKey for User
    product = models.ForeignKey(Clothes, on_delete=models.CASCADE)  # ForeignKey for Product
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)  # Total price calculated from product price

    def save(self, *args, **kwargs):
        # Calculate total price dynamically from product's price and quantity
        self.total_price = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def _str_(self):
        return f"{self.user.username} - {self.product.name} - {self.quantity}"
