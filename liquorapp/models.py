from django.db import models
from django.contrib.auth.models import User
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
    
class CustomerModel(models.Model):
    cusname = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='cus_image')
    phone = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    address = models.TextField()

    def __str__(self):
        return self.cusname
    
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
    
class OrderModel(models.Model):
    customer = models.ForeignKey(CustomerModel, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.customer.cusname
    
