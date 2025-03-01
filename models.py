from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    SIZE_CHOICES = [
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'X-Large'),
        ('XXL', '2X-Large'),
        ('XXXL', '3X-Large'),
    ]

    COLOR_CHOICES = [
        ('Red', 'Red'),
        ('Blue', 'Blue'),
        ('Green', 'Green'),
        ('Black', 'Black'),
        ('White', 'White'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    image = models.ImageField(upload_to='products/', default='media/product/images.jpeg')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  
    size = models.CharField(max_length=4, choices=SIZE_CHOICES, default='M')
    color = models.CharField(max_length=20, choices=COLOR_CHOICES, default='Black')

    def __str__(self):
        return self.name


# Order and OrderItem models for order management
class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)  # link the order to a user
    order_date = models.DateTimeField(default=timezone.now) 
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')  # rorder status
    total_price = models.DecimalField(max_digits=10, decimal_places=2)  # total price of the order
    address = models.TextField()  # delivery address

    def __str__(self):
        return f"Order {self.id} - {self.user.username}"



class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)  # link to the order
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # link to the product
    quantity = models.PositiveIntegerField()  # quantity of the product ordered
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # dsefault price set to 0.00

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
