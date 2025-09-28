from django.utils import timezone
from liquorapp.models import CartModel, OrderModel, ProductModel, ShopModel
from django.db.models import Sum,Value, DecimalField
from django.shortcuts import render, redirect
from decimal import Decimal
from django.db.models.functions import Coalesce

def nowtime(request):
    return{
        'now':timezone.now()
    }

def cart_context(request):
    if request.user.is_authenticated:
        carts = (CartModel.objects
                 .filter(user=request.user)
                 .select_related('product')
                 .order_by('-created_at'))
        cart_shop = carts.first().shop if carts.exists() else None
        cart_shop_id = carts.first().shop.id if carts.exists() and carts.first().shop else None
        cart_total = carts.filter(status=False).aggregate(x=Sum('total'))['x'] or Decimal('0.00')
        cart_quantity = carts.filter(status=False).aggregate(q=Sum('quantity'))['q'] or 0
        return {"carts": carts, "cart_total": cart_total, "cart_quantity": cart_quantity, "cart_shop":cart_shop, "cart_shop_id":cart_shop_id}
    return {"carts": []}

def order_context(request):
    orders_receive = (OrderModel.objects
                      .filter(shopkeeper=request.user)
                      .select_related("cart", "cart__product", "customer")
                      .order_by("-created_at"))

    orders_send = (OrderModel.objects
                   .filter(customer=request.user)
                   .select_related("cart", "cart__product", "shopkeeper")
                   .order_by("-created_at"))

    return render(request, "orders_list.html", {
        "orders_receive": orders_receive,
        "orders_send": orders_send,
       
    })

def notifications(request):
    if not request.user.is_authenticated:
        return {
            "pending_receive_count": 0,
            "pending_send_count": 0,
        }

    pending_receive_count = OrderModel.objects.filter(
        shopkeeper=request.user, purchase=False
    ).count()

    pending_send_count = OrderModel.objects.filter(
        customer=request.user, purchase=False
    ).count()

    # (optional) cart badge total items
    cart_quantity = (
        CartModel.objects.filter(user=request.user, status=False)
        .aggregate(q=Sum("quantity"))["q"] or 0
    )

    return {
        "pending_receive_count": pending_receive_count,
        "pending_send_count": pending_send_count,
        "cart_quantity": cart_quantity,  # if you weren’t already providing it
    }

# def SearchBy(request):
#     if request.method == "GET":
#         search = request.GET.get('search')

#         if not search:  # if search is None or empty
#             # show all shops & products on the current page
#             shops = ShopModel.objects.all().order_by('created_at')
#             products = ProductModel.objects.all().order_by('created_at')
#         else:
#             # filter by search
#             shops = ShopModel.objects.filter(
#                 Q(shopname__icontains=search)
#             ).order_by('created_at')

#             products = ProductModel.objects.filter(
#                 Q(productname__icontains=search)
#             ).order_by('created_at')

#         context = {
#             "shops": shops,
#             "products": products,
#         }
#         return render(request, "search_results.html", context)