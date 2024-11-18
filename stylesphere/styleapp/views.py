from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
import os
from .models import Category,Clothes,Cart,Order,Userdetails
from django.contrib import messages
from django.contrib.auth.hashers import make_password

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
            if username.lower() == 'admin':
                login(request, user)
                return redirect('/admin/') 
            else:
                login(request, user)
                return redirect('index')  # Redirect to your homepage after login
        else:
            # If authentication fails, return an error message
            messages.error(request, "Invalid credentials. Please try again.")
            return render(request, 'Login.html')  # Ensure you have a 'loginpage.html' template
 # Redirect to login page if authentication fails

    # If it's a GET request, render the login page
    return render(request, 'Login.html')  # Ensure you have a 'loginpage.html' template


def forgot_password_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            request.session['reset_email'] = email  # Save email in session for reset
            return redirect('reset_password')
        except ObjectDoesNotExist:
            messages.error(request, "Email does not exist!")
    return render(request, 'forgot_password.html')


def reset_password_view(request):
    if request.method == "POST":
        email = request.session.get('reset_email')  # Retrieve email from session
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if len(new_password) < 8:
            messages.error(request, "Password must be at least 8 characters long.")
        if new_password != confirm_password:
            messages.error(request, "Passwords do not match!")
        else:
            try:
                user = User.objects.get(email=email)
                user.set_password(new_password)
                user.save()
                messages.success(request, "Password successfully updated!")
                return redirect('signin')
            except ObjectDoesNotExist:
                messages.error(request, "An error occurred. Please try again.")
    return render(request, 'reset_password.html')

def signup(request):
    if request.method == 'POST':
        # User fields
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # Additional fields for Userdetails
        address = request.POST['address']
        contact = request.POST['contact']
        profile = request.FILES.get('profile')
        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters long.")
            return redirect('signup')
        # Check password match
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')

        # Check if user already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'User with this email already exists.')
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists. Please choose another one.")
            return redirect('signup')

        # Create User
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )

        # Create Userdetails
        Userdetails.objects.create(
            user=user,
            address=address,
            phone=contact,
            image=profile
        )

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

def order_history(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user)
        return render(request, 'order_history.html', {'orders': orders})
    else:
        return redirect('login')  # Redirect to login if the user is not authenticated
    
@login_required(login_url='signin')
def create_order(request):
    if request.method == "POST":
        user = request.user
        cart_items = Cart.objects.filter(user=user)  # Retrieve cart items for the logged-in user

        if cart_items.exists():
            for item in cart_items:
                total_price = item.quantity * item.product.price if not item.total_price else item.total_price
                odr = Order(user=user, product=item.product, quantity=item.quantity, total=total_price)
                odr.save()
            cart_items.delete()

            messages.success(request, "Order placed successfully!")
            return render(request, "cart.html", {'order_placed': True})  # Render with success flag
        else:
            messages.error(request, "Your cart is empty!")
            return render(request, "cart.html", {'order_placed': False})  # Render with failure flag
    
    return redirect("cart_view")

@login_required(login_url='signin')
def user_account(request):
    current = request.user
    user_det = Userdetails.objects.get(user=current)
    return render(request, 'user_account.html', {'user': user_det})

@login_required
def edit_profile(request):
    user = request.user
    try:
        user_det = Userdetails.objects.get(user=user)
    except ObjectDoesNotExist:
        user_det = Userdetails(user=user)  # In case Userdetails does not exist for this user

    if request.method == 'POST':
        # Update basic user details (first name, last name, email)
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        
        # Handle profile image upload
        if request.FILES.get('prf_image'):
            # Delete the old image if it exists
            if user_det.image:
                # Get the full file path and delete it
                old_image_path = user_det.image.path
                if os.path.exists(old_image_path):
                    os.remove(old_image_path)
            
            # Save the new image
            user_det.image = request.FILES['prf_image']
        
        # Update address and phone number
        user_det.address = request.POST.get('address')
        user_det.phone = request.POST.get('phone')

        # Save user and user details
        user.save()
        user_det.save()

        # Success message
        messages.success(request, "Profile updated successfully!")
        return redirect('user_account')  # Redirect to the user account page

    # If GET request, render the profile page with current user details
    return render(request, 'edit_profile.html', {'user': user_det})

@login_required
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        if len(new_password) < 8:
            messages.error(request, "Password must be at least 8 characters long.")
        if not request.user.check_password(current_password):
            messages.error(request, "Current password is incorrect.")
        elif new_password != confirm_password:
            messages.error(request, "New passwords do not match.")
        else:
            request.user.set_password(new_password)
            request.user.save()
            messages.success(request, "Password changed successfully!")
            # Reauthenticate the user after password change
            user = authenticate(username=request.user.username, password=new_password)
            if user:
                login(request, user)
            return redirect('user_account')
    return render(request, 'change_password.html')

