from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
import os
from .models import Category,Clothes,Cart

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        current = request.user.id
        user_det = User.objects.get(id=current)
        products = Clothes.objects.all()  # Fetch all products from the database
        return render(request, 'index.html',{'products':products,'User':user_det})
    else:
        products = Clothes.objects.all()  # Fetch all products from the database
        return render(request, 'index.html',{'products':products})
        

def categorypage(request):
    if request.user.is_authenticated:
        current = request.user.id
        user_det = User.objects.get(id=current)
        cate = Category.objects.all()
        return render(request,"category.html",{'category':cate,'User':user_det})
    else:
        cate = Category.objects.all()
        return render(request,"category.html",{'category':cate})
def categoryviewpage(request,a):
    if request.user.is_authenticated:
        current = request.user.id
        user_det = User.objects.get(id=current)
        cate = Category.objects.get(id=a)
        cloth = Clothes.objects.filter(category_id = a)
        return render(request,"categoryview.html",{'category':cate,'User':user_det,'cloths':cloth})
    else:
        cate = Category.objects.get(id=a)
        cloth = Clothes.objects.filter(category_id = a)
        return render(request,"categoryview.html",{'category':cate,'cloths':cloth})

def viewmorepage(request,a):
    if request.user.is_authenticated:
        current = request.user.id
        user_det = User.objects.get(id=current)
        cloth = Clothes.objects.get(id=a)
        return render(request,"viewmore.html",{'User':user_det,'cloths':cloth})
    else:
        cloth = Clothes.objects.get(id=a)
        return render(request,"viewmore.html",{'cloths':cloth})

@login_required(login_url = 'signin')
def cart_view(request):
    if request.user.is_authenticated:
        current = request.user.id
        user_det = User.objects.get(id = current)
        cart_items = Cart.objects.filter(user_id = current)
        each_price=sum(p.total_price for p in cart_items)
        total_price= each_price 
        return render(request, 'cart.html', {'User':user_det,'cart_items':cart_items,'total':total_price})
    
@login_required(login_url = 'signin')
def add_to_cart(request, id):
    if request.method == 'POST':
        current = request.user.id 
        user1 = User.objects.get(id=current)  
        prod = Clothes.objects.get(id=id) 
        
        qty = int(request.POST.get("quantity", 1)) 
        
        existing_cart_item = Cart.objects.filter(user=user1, product=prod).first()
        
        if existing_cart_item:
            
            existing_cart_item.quantity += qty
            existing_cart_item.total_price = existing_cart_item.quantity * prod.price
            existing_cart_item.save()  
            prod.stock -= qty
            prod.save()
        else:
            
            prod.stock -= qty 
            prod.save() 
            total = qty * prod.price 
            cr = Cart(user=user1, product=prod, quantity=qty, total_price=total)
            cr.save() 
        return redirect('cart_view')
 
@login_required(login_url = 'signin')
def delete_cart(request,a):
    c=Cart.objects.get(id=a)
    pd=Clothes.objects.get(id=c.product.pk)
    pd.stock = pd.stock + c.quantity
    pd.save()
    c.delete()
    return redirect('cart_view')

# Signin view for user authentication
def signin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # If authentication is successful, log the user in and redirect
            login(request, user)
            return redirect('index')  # Redirect to your homepage after login
        else:
            # If authentication fails, return an error message
            messages.error(request, "Invalid credentials. Please try again.")
            return render(request, 'Login.html')  # Ensure you have a 'loginpage.html' template
 # Redirect to login page if authentication fails

    # If it's a GET request, render the login page
    return render(request, 'Login.html')  # Ensure you have a 'loginpage.html' template


def signup(request):
    if request.method == 'POST':
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(email=email).exists():
            messages.error(request, 'User with this email already exists.')
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists. Please choose another one.")
            return redirect('signup')

        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )
        user.save()
        messages.success(request, 'Registration successful! You can now log in.')
        return redirect('signin')

    return render(request, 'Register.html') 

def about(request):
    if request.user.is_authenticated:
        current = request.user.id
        user_det = User.objects.get(id = current)
        return render(request, 'about.html',{'User':user_det})
    else:
        return render(request, 'about.html')

@login_required(login_url = signin)
def logout_user(request):
    auth.logout(request)
    return redirect('index')
