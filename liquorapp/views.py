from django.shortcuts import render, redirect, get_object_or_404
from liquorapp.models import *
from django.db.models import Q
from django.db.models import F
from django.conf import settings
from django.contrib.auth import authenticate, login, logout 
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator 
from django.core.mail import send_mail
from django.db import transaction
from django.core.paginator import Paginator
from django import forms



def Custom404Page(request):
    return render(request, '404page.html')

def About(request):
    return render(request, 'about.html')

def TermsOfService(request):
    return render(request, 'terms_and_conditions.html')

def PrivacyAndPolicy(request):
    return render(request,'privacy_and_policy.html')

# search
def SearchBy(request):
    if request.method == "GET":
        search = request.GET.get('search')

        if not search:  # if search is None or empty
            # show all shops & products on the current page
            shops = ShopModel.objects.all().order_by('created_at')
            products = ProductModel.objects.all().order_by('created_at')
        else:
            # filter by search
            shops = ShopModel.objects.filter(
                Q(shopname__icontains=search)
            ).order_by('created_at')

            products = ProductModel.objects.filter(
                Q(productname__icontains=search)
            ).order_by('created_at')

        context = {
            "shops": shops,
            "products": products,
        }
        return render(request, "search_results.html", context)

# Create your views here.
def Index(request):
    return render(request, 'index.html')

def ShopTitle(request):
    return render(request, "shop.html")

def LoginView(request):
   if request.method == "GET": 
        return render(request, "login.html")
   if request.method == "POST":
        user = authenticate(
            username=request.POST['username'], 
            password=request.POST['password']
        )
        # if user is not None:
        if user:
            login(request,user)
            messages.success(request, "Login successfully")
            return redirect('/')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('/login/')
        
def LogoutView(request):
    logout(request)
    return redirect('/login/')

def Register(request):
    if request.method == "GET":
        return render(request, "register.html")
    if request.method == "POST":
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        password_confirm=request.POST['password_confirm']
        if User.objects.filter(username =username):
            messages.error(request, "Username already exists")
            return redirect('/register/')
        if User.objects.filter(email =email):
            messages.error(request, "Email already exists")
            return redirect('/register/')
        if password == password_confirm:
            user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=password,
            )
            user.save()
            # subject = 'New User Registered'
            # message = f'Username is {user.username}, Email is {user.email}'
            # email_from = settings.EMAIL_HOST_USER
            # recipient_list = [user.email,]
            # send_mail(subject,message,email_from,recipient_list)
            login(request,user)
            messages.success(request,"Register successfully")
            return redirect('/')
        else:
            messages.error(request,"Password does not match")
            return redirect('/register/')
        
# profile views
# (Optional) tiny form for editing basic fields
class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "First name"}),
            "last_name":  forms.TextInput(attrs={"class": "form-control", "placeholder": "Last name"}),
            "email":      forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email"}),
        }

@login_required
def profile_view(request):
    user = request.user
    # Optional: quick stats (adjust/remove if not needed)
    from liquorapp.models import OrderModel, CartModel
    pending_orders = OrderModel.objects.filter(shopkeeper=user, purchase=False).count()
    sent_orders = OrderModel.objects.filter(customer=user, purchase=False).count()
    cart_items = CartModel.objects.filter(user=user, status=False).count()

    return render(request, "account/profile.html", {
        "u": user,
        "pending_orders": pending_orders,
        "sent_orders": sent_orders,
        "cart_items": cart_items,
    })

@login_required
def profile_view_cus(request,name):
    user = User.objects.get(username=name)
    # Optional: quick stats (adjust/remove if not needed)
    from liquorapp.models import OrderModel, CartModel
    pending_orders = OrderModel.objects.filter(shopkeeper=user, purchase=False).count()
    sent_orders = OrderModel.objects.filter(customer=user, purchase=False).count()
    cart_items = CartModel.objects.filter(user=user, status=False).count()

    return render(request, "account/profile.html", {
        "u": user,
        "pending_orders": pending_orders,
        "sent_orders": sent_orders,
        "cart_items": cart_items,
    })

@login_required
def profile_edit(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect("profile_view")
    else:
        form = ProfileForm(instance=request.user)
    return render(request, "account/profile_edit.html", {"form": form})



def ShopList(request):
    shops = ShopModel.objects.all().order_by('-created_at')
    paginator = Paginator(shops, 4) 
    page_number = request.GET.get('page') 
    page_obj = paginator.get_page(page_number) 
    context = {
        'shops': page_obj,
    }
    return render(request, "shop_list.html", context)

@login_required(login_url="/login/")
def ShopCreate(request):
    if request.method == "GET":
       return render(request, "shop_create.html")
    if request.method == 'POST':
        shop = ShopModel.objects.create(
            shopname =  request.POST['shopname'],
            shop_image = request.FILES.get('shop_image'),
            owner = request.user,
            photo =request.FILES.get('photo'),
            phone = request.POST['phone'],
            address = request.POST['address'],
        )
        shop.save()
        shop.owner.is_staff = True
        shop.owner.save()
        return redirect('/shops/list/')

def ShopUpdate(request,pk):
    shop = ShopModel.objects.get(id=pk)
    if request.method == "GET":
       return render(request, "shop_update.html", {'shop':shop})
    if request.method == "POST":
        shop.shopname =  request.POST['shopname']
        if request.FILES.get('shop_image'):
            shop.shop_image.delete()
            shop.shop_image = request.FILES.get('shop_image')
        owner = request.user
        if request.FILES.get('photo'):
            shop.photo.delete()
            shop.photo =request.FILES.get('photo')
        shop.phone = request.POST['phone']
        shop.address = request.POST['address']
        shop.save()
        return redirect('/shops/list/')
    
def ShopDelete(request,pk):
    shop = ShopModel.objects.get(id=pk)
    owner = shop.owner
    if request.method == "POST":
        if shop.shop_image:
            shop.shop_image.delete()
        if shop.photo:
            shop.photo.delete()
        if owner.is_staff:   
            owner.is_staff = False
            owner.save(update_fields=["is_staff"])
        shop.delete()
        return redirect('/shops/list/')
    
def ShopAvailable(request,pk):
    shop = ShopModel.objects.get(id=pk)
    products = ProductModel.objects.filter(shop_id=shop.id).order_by('created_at')
    context = {
        'shop': shop,
        'products': products,
    }
    return render(request, 'shop_available.html', context)

def ProductList(request):
    products = ProductModel.objects.all().order_by('productname')
    paginator = Paginator(products, 4) 
    page_number = request.GET.get('page') 
    page_obj = paginator.get_page(page_number) 
    context = {
        'products':page_obj
    }
    return render(request, "product_list.html", context)

@login_required(login_url="/login/")
@staff_member_required
def ProductCreate(request):
    if request.method == 'GET':
        return render(request, "product_create.html")
    if request.method == 'POST':
        shop = get_object_or_404(ShopModel, owner=request.user)
        product = ProductModel.objects.create(
            productname =  request.POST['productname'],
            product_image = request.FILES.get('product_image'),
            quantity = request.POST['quantity'],
            price = request.POST['price'],
            shop = shop,
            description = request.POST['description'],
            )
        product.save()
        return redirect('/products/list/')
    
@login_required(login_url="/login/")
@staff_member_required
def ProductUpdate (request,pk):
    product = ProductModel.objects.get(id=pk)
    if request.method == "GET":
        return render(request, "product_update.html", {'product':product})
    if request.method == "POST":
        product.productname = request.POST['productname']
        if request.FILES.get('product_image'):
            product.product_image.delete()
            product.product_image = request.FILES.get('product_image')
        product.price = request.POST['price']
        product.quantity = request.POST['quantity']
        product.description = request.POST['description']
        product.shop = get_object_or_404(ShopModel, owner=request.user)
        product.save()
        messages.success(request, "successfully product updated")
        return redirect('/products/list/')


@login_required(login_url="/login/")
def ShopCartList(request):
    products = ProductModel.objects.all()
    carts = (CartModel.objects
             .filter(user=request.user)        # current user only
             .select_related('product')
             .order_by('-created_at'))
    
    return render(request, "cart_list.html", {
        "products": products,
        "carts": carts,
        
    })

@login_required(login_url="/login/")
def ShopCartCreate(request):
    if request.method != 'POST':
        return redirect('/products/list/')
    product_id = request.POST.get("product_id")
    shop_id = request.POST.get("shop_id")
    qty = int(request.POST.get('quantity', 1))
    if qty <= 0:
        messages.error(request, "Quantity must be at least 1.")
        return redirect('/products/list/')
    product = get_object_or_404(ProductModel, id=product_id)
    shop = get_object_or_404(ShopModel, id=shop_id)
    if shop.owner == request.user or product.shop.owner == request.user:
        messages.error(request, "You cannot buy from your own shop.")
        return redirect("/products/list/")
    
# 🔒 Enforce one-shop-only cart (consider only status=False = active cart)
    existing_shop_ids = list(
        CartModel.objects
        .filter(user=request.user, status=False)
        .values_list("shop_id", flat=True)
        .distinct()
    )
    if existing_shop_ids and shop.id not in existing_shop_ids:
        messages.error(
            request,
            "Your cart already has items from another shop. "
            "Please checkout or clear your cart before buying from a different shop."
        )
        return redirect("/products/list/")

    # (Optional but safe) Ensure product really belongs to this shop
    if getattr(product, "shop_id", None) and product.shop_id != shop.id:
        messages.error(request, "This product belongs to a different shop.")
        return redirect("/products/list/")

    total = product.price  * qty
    
    with transaction.atomic():
        line, created = CartModel.objects.get_or_create(
            user=request.user,
            shop=shop,
            product=product,
            status=False,
            defaults={"quantity": 0, "total": Decimal("0.00")},
        )
        CartModel.objects.filter(pk=line.pk).update(quantity=F("quantity") + qty)
        line.refresh_from_db(fields=["quantity"])
        CartModel.objects.filter(pk=line.pk).update(total=product.price * F("quantity"))
        line.refresh_from_db(fields=["total"])
    messages.success(request, "Added to cart.")
    return redirect("/products/list/")

def ShopCartUpdate(request,pk):
    cart = CartModel.objects.get(id=pk)
    product_id = request.POST.get("product_id")
    shop_id = request.POST.get("shop_id")
    if request.method == "POST":
        cart.product = get_object_or_404(ProductModel, id=product_id)
        cart.shop = get_object_or_404(ShopModel, id=shop_id)
        cart.quantity = int(request.POST.get('quantity', 1))
        cart.total = cart.product.price  * cart.quantity
        cart.user = request.user
        cart.status = False
        cart.save()
        messages.success(request, "Updated to cart.")
        return redirect('/shoppingcart/list/')

def ShopCartDelete(request,pk):
    cart = CartModel.objects.get(id=pk)
    if request.method == "POST":
        cart.delete()
        messages.success(request, "Deleted Successfully")
        return redirect('/shoppingcart/list/')
    
# order
@login_required(login_url="/login/")
def OrderList(request):
    orders_receive = (OrderModel.objects
                      .filter(shopkeeper=request.user)
                      .select_related("cart", "cart__product", "customer")
                      .order_by("-created_at"))

    orders_send = (OrderModel.objects
                   .filter(customer=request.user)
                   .select_related("cart", "cart__product", "shopkeeper")
                   .order_by("-created_at"))
    pending_receive_count = orders_receive.filter(purchase=False).count()

    return render(request, "orders_list.html", {
        "orders_receive": orders_receive,
        "orders_send": orders_send,
        "pending_receive_count": pending_receive_count,
    })


@login_required(login_url="/login/")
def OrderSend(request):
    # Grab all active cart lines for this customer
    carts = (CartModel.objects
             .filter(user=request.user, status=False)
             .select_related("shop", "shop__owner", "product"))
    if not carts.exists():
        messages.warning(request, "Your cart is empty.")
        return redirect("/products/list/")

    # Enforce single-shop cart
    shop_ids = list(carts.values_list("shop_id", flat=True).distinct())
    if len(shop_ids) != 1:
        messages.error(request, "Your cart contains items from multiple shops. Please keep items from one shop only.")
        return redirect("/shoppingcart/list/")

    with transaction.atomic():
        for c in carts:
            # Create an offering order per cart line
            OrderModel.objects.create(
                customer   = request.user,
                shopkeeper = c.shop.owner,
                cart       = c,               # links to the CartModel row (has qty/total/product)
                purchase   = False            # offering stage
            )

            # Reduce stock
            # ProductModel.objects.filter(pk=c.product_id).update(
            #     quantity=F("quantity") - c.quantity
            # )

            # Freeze cart line so it can't be edited anymore
            c.status = True
            c.save(update_fields=["status"])

    messages.success(request, "Order sent to the shop. They’ll review your offer.")
    return redirect("/products/list/")  # point to a page that shows sent/received orders

@login_required
def confirm_order(request, pk):
    order = get_object_or_404(OrderModel, pk=pk, shopkeeper=request.user)
    if order.purchase:
        messages.info(request, "Order already confirmed.")
    else:
        order.purchase = True
        order.save(update_fields=["purchase", "updated_at"])
        messages.success(request, "Order confirmed.")
    return redirect("orders_list")

@login_required
def order_mark_sold(request, pk):
    # Only the shopkeeper who owns this order can mark it sold
    order = get_object_or_404(OrderModel, pk=pk, shopkeeper=request.user)
    if order.purchase:
        messages.info(request, "Already confirmed.")
        return redirect("orders_list")
    
    qty = order.cart.quantity
    product = order.cart.product

    with transaction.atomic():
        # Lock the product row to avoid race conditions
        product_locked = ProductModel.objects.select_for_update().get(pk=product.pk)

        # Ensure enough stock (quantity field on ProductModel)
        if product_locked.quantity is None:
            messages.error(request, "This product does not track quantity.")
            return redirect("orders_list")

        if product_locked.quantity < qty:
            messages.error(
                request,
                f"Insufficient stock for {product_locked.productname}. "
                f"Have {product_locked.quantity}, need {qty}."
            )
            return redirect("orders_list")

        # Deduct using F() for safe in-DB arithmetic
        ProductModel.objects.filter(pk=product_locked.pk).update(
            quantity=F("quantity") - qty
        )

        order.purchase = True
        order.save(update_fields=["purchase"])
    messages.success(request, "Marked as sold.")
    return redirect("orders_list")


    






