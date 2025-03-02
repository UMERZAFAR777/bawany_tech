from django.http import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from slider.models import Slider
from app.models import Main_Category
from product.models import Product,Section
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib import messages





def index(request):
    slider = Slider.objects.all().order_by('-id')
    main_category = Main_Category.objects.all()
    top_deals = Product.objects.filter(section__name="Top Deals Of The Day")
    top_featured = Product.objects.filter(section__name="Top Featured Products").order_by('-id')
    top_selling = Product.objects.filter(section__name="Top Selling Products")
    data = {
        'slider':slider,
        'main_category':main_category,
        'top_deals':top_deals,
        'top_featured':top_featured,
        'top_selling':top_selling,


    }
    return render (request,'index.html',data)


def product_detail(request,slug):
    product = Product.objects.filter(slug = slug)

    if product.exists():
        product = Product.objects.get(slug = slug)
    else:
        return redirect ('error404')    
    return render (request,'product/product_detail.html',{'product':product})




def error404(request):

    return render (request,'error/error404.html')


def account(request):
    
        
    return render (request,'account/my_account.html')

def login_user(request):
    if request.method == 'POST':
        user_input = request.POST.get('user_input') 
        password = request.POST.get('password')

      
        user = None
        if '@' in user_input: 
            try:
                user_obj = User.objects.get(email=user_input)  
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None
        else:
            user = authenticate(request, username=user_input, password=password) 

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, "Incorrect email/username or password, please try again!")
            return redirect('account')  

def logout_user(request):
    logout(request,)
    messages.success(request, "Logout Successfully")
    return redirect('account')  

   

def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

       
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken...!')
            return redirect('account')  

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already taken...!')
            return redirect('account')  

        
        user = User.objects.create_user(username=username, email=email, password=password)

        messages.success(request, 'Registered Successfully! Please login.')

        return redirect('account') 
    return render(request, 'account/my_account.html')


