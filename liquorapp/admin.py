from django.contrib import admin
from liquorapp import models
# Register your models here.

admin.site.register(models.ShopModel)
admin.site.register(models.CustomerModel)
admin.site.register(models.ProductModel)
admin.site.register(models.OrderModel)

