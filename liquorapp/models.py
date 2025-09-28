from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
# Create your models here.

class ShopModel(models.Model):
    shopname = models.CharField(max_length=100)
    shop_image = models.ImageField(upload_to='shop_image')
    owner = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    photo = models.ImageField(upload_to='shop_image')
    phone = models.CharField(max_length=100)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.shopname
    
# class CustomerModel(models.Model):
#     cusname = models.CharField(max_length=100)
#     photo = models.ImageField(upload_to='cus_image')
#     phone = models.CharField(max_length=100)
#     email = models.CharField(max_length=100)
#     address = models.TextField()

#     def __str__(self):
#         return self.cusname
    
class ProductModel(models.Model):
    productname = models.CharField(max_length=100)
    product_image = models.ImageField(upload_to='product_image')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    description = models.TextField()
    shop = models.ForeignKey(ShopModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.productname
    
class CartModel(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    shop = models.ForeignKey(ShopModel,on_delete=models.CASCADE,null=True,)
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        # return f"{self.total}"
        return self.user.username
    
class OrderModel(models.Model):
    customer    = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders_sent",  null=True)
    shopkeeper  = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders_recv",  null=True)
    cart = models.ForeignKey(CartModel, on_delete=models.CASCADE)
    purchase = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.pk} - {self.customer.username}"
