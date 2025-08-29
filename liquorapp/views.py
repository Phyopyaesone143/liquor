from django.shortcuts import render, redirect
from liquorapp.models import *
from django.db.models import Q
from django.conf import settings
from django.contrib.auth import authenticate, login, logout 
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator 
from django.core.mail import send_mail



def Custom404Page(request):
    return render(request, '404page.html')

def About(request):
    return render(request, 'about.html')

def TermOfService(request):
    return render(request, 'term_of_services.html')

# Create your views here.
def Index(request):
    posts = ShopModel.objects.all().order_by('created_at')
    # posts = PostModel.objects.filter(active = True).order_by('-created_at') # for activate စစ်ပြီး ထုတ်ရန်
    paginator = Paginator(posts, 8) 
    page_number = request.GET.get('page') 
    page_obj = paginator.get_page(page_number) 
    context = {
        'posts': page_obj,
    }
    
    return render(request, 'index.html',context)



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



def ShopList(request):
    shops = ShopModel.objects.all().order_by('-created_at')
    context = {
        'shops':shops
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

    
def ProductList(request):
    products = ProductModel.objects.all().order_by('-created_at')
    context = {
        'products':products
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
def ShopCartList(request):
    carts = OrderModel.objects.all().order_by('-created_at')
    context = {
        'carts':carts
    }
    return render(request, "cart_list.html", context)

def ShopCartCreate(request):
    # if request.method == "GET":
    #    return render(request, "shop_create.html")
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