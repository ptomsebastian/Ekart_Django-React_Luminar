from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db import models

# class User(AbstractUser):
#     user_type = models.CharField(max_length=20)

# class Customer(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer')
#     phone = models.CharField(max_length=20, blank=True, null=True)

#     def save(self, *args, **kwargs):
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return self.user.username

class Customer(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255,  default='')
    last_name = models.CharField(max_length=255,  default='')
    username = models.CharField(max_length=255, unique=True,  default='')
    email = models.EmailField(unique=True,  default='')
    password = models.CharField(max_length=255, default='') 
    phone = models.CharField(max_length=20, blank=True, null=True,  default='')

    def save(self, *args, **kwargs):   
        self.password = make_password(self.password) # django password hashing
        super().save(*args, **kwargs)
    def __str__(self):
        return self.username
    



class Brand(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    categories = (
        ("Mobiles", "Mobiles"),
        ("Televisions", "Televisions"),
        ("Laptops", "Laptops"),
        ("Cameras", "Cameras"),
        ("Audio", "Audio"),
        ("Appliances", "Appliances"),
    )
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.IntegerField(default=1)
    image = models.ImageField(upload_to='images')
    description = models.CharField(max_length=250, null=True)
    category = models.CharField(max_length=20, choices=categories)
    quantity = models.IntegerField(default=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class BookingTable(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.IntegerField(default=1000)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     return f"Booking {self.id} - {self.customer.username} - {self.product.name}"



