from django.http import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from slider.models import Slider
from app.models import Main_Category,Category,Sub_Category
from product.models import Product,Section
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Max, Min
# @login_required(login_url = '/login/')


def index(request):
    slider = Slider.objects.all().order_by('-id')
    main_category = Main_Category.objects.all()
    top_deals = Product.objects.filter(section__name="Top Deals Of The Day").order_by('-id')
    top_featured = Product.objects.filter(section__name="Top Featured Products").order_by('-id')
    top_selling = Product.objects.filter(section__name="Top Selling Products").order_by('-id')
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
            return redirect('login')  

def logout_user(request):
    logout(request,)
    messages.success(request, "Logout Successfully")
    return redirect('login')  

   

def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

       
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken...!')
            return redirect('login')  

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already taken...!')
            return redirect('login')  

        
        user = User.objects.create_user(username=username, email=email, password=password)

        messages.success(request, 'Registered Successfully! Please login.')

        return redirect('login') 
   

# def shop(request):
#     category = Category.objects.all()
#     all_products = Product.objects.filter(
#     section__name__in=["Top Deals Of The Day", "Top Featured Products", "Top Selling Products"]
#     ).order_by('-id')

#     paginator = Paginator(all_products, 8) 

#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)


#     min_price = Product.objects.all().aggregate(Min('original_price'))
#     max_price = Product.objects.all().aggregate(Max('original_price'))
#     FilterPrice = request.GET.get('FilterPrice')
#     if FilterPrice:
#         Int_FilterPrice = int(FilterPrice)
#         all_products = Product.objects.filter(original_price__lte = Int_FilterPrice)
#     else:
#         all_products = Product.objects.all()


#     data = {
#         'category':category,
#         'all_products':all_products,
#         'all_products':page_obj,
#         'page_obj':page_obj,
#         'min_price':min_price,
#         'max_price':max_price,
#         'FilterPrice':FilterPrice,
#     }

#     return render (request,'shop.html',data)


def shop(request):
    category = Category.objects.all()
    all_products = Product.objects.filter(
        section__name__in=["Top Deals Of The Day", "Top Featured Products", "Top Selling Products"]
    ).order_by('-id')

    min_price = Product.objects.aggregate(Min('original_price'))
    max_price = Product.objects.aggregate(Max('original_price'))

    # Get filter price from request
    FilterPrice = request.GET.get('FilterPrice')

    # Apply filter if price is provided
    if FilterPrice:
        try:
            Int_FilterPrice = int(FilterPrice)
            all_products = all_products.filter(original_price__lte=Int_FilterPrice)  # ✅ Apply filter on existing query
        except ValueError:
            pass  # If invalid input, ignore filter

    # Apply pagination AFTER filtering
    paginator = Paginator(all_products, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    data = {
        'category': category,
        'all_products': page_obj,  # ✅ Pass paginated objects
        'page_obj': page_obj,
        'min_price': min_price,
        'max_price': max_price,
        'FilterPrice': FilterPrice,
    }

    return render(request, 'shop.html', data)


def contact(request):
    return render (request,'contact.html')

def about(request):
    return render (request,'about.html')







from django.core.paginator import Paginator

def filter_data(request):
    categories = request.GET.getlist('category[]')
    brands = request.GET.getlist('brand[]')

    all_products = Product.objects.filter(
        section__name__in=["Top Deals Of The Day", "Top Featured Products", "Top Selling Products"]
    )

    if categories:
        all_products = all_products.filter(category__id__in=categories)

    if brands:
        all_products = all_products.filter(brand__id__in=brands)

    # Pagination (Jab products filter ho jayein)
    paginator = Paginator(all_products, 8)  # 10 products per page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    # Render the product HTML template
    html_content = render_to_string('ajax/shop.html', {'page_obj': page_obj})

    return JsonResponse({'data': html_content})




def wishlist(request):
    return render (request,'wishlist.html')


def cart(request):
    return render (request,'cart.html')


from django.contrib.auth.decorators import login_required
from cart.cart import Cart


@login_required(login_url="/accounts/login/")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)

    # Check if the product is in the cart and its quantity is greater than 1
    if str(product.id) in cart.cart and cart.cart[str(product.id)]["quantity"] > 1:
        cart.decrement(product=product)

    return redirect("cart_detail")



@login_required(login_url="/accounts/login/")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def cart_detail(request):
    return render(request, 'cart/cart_detail.html')


