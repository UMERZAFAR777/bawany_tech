from django.http import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from slider.models import Slider
from app.models import Main_Category,Category,Sub_Category
from product.models import Product,Section,Time,Wishlist
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
    time = Time.objects.first()
    if request.user.is_authenticated:
        wishlist_items = Wishlist.objects.filter(user=request.user)
        products = [item.product for item in wishlist_items]
    else:
        products = []

        
    data = {
        'slider':slider,
        'main_category':main_category,
        'top_deals':top_deals,
        'top_featured':top_featured,
        'top_selling':top_selling,
        'time':time,
        'products':products,


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




def contact(request):
    return render (request,'contact.html')

def about(request):
    return render (request,'about.html')











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
    if request.user.is_authenticated:
        wishlist_items = Wishlist.objects.filter(user=request.user)
        products = [item.product for item in wishlist_items]
    else:
        products = []

    data = {
        'products':products
    }
    return render(request, 'cart/cart_detail.html',data)





# def shop(request):
#     category = Category.objects.all()
#     all_products = Product.objects.filter(
#         section__name__in=["Top Deals Of The Day", "Top Featured Products", "Top Selling Products"]
#     ).order_by('-id')

#     min_price = Product.objects.aggregate(Min('original_price'))
#     max_price = Product.objects.aggregate(Max('original_price'))

   
#     search_query = request.GET.get('search_query', '') 
#     if search_query:
#         all_products = all_products.filter(product_name__icontains=search_query)

   
#     paginator = Paginator(all_products, 8)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)

#     if request.user.is_authenticated:
#         wishlist_items = Wishlist.objects.filter(user=request.user)
#         products = [item.product for item in wishlist_items]
#     else:
#         products = []
#     data = {
#         'category': category,
#         'all_products': page_obj,
#         'page_obj': page_obj,
#         'min_price': min_price,
#         'max_price': max_price,
#         'FilterPrice': Filter,
#         'search_query': search_query,
#         'products':products,
#     }

#     return render(request, 'shop.html', data)
def shop(request):
    category = Category.objects.all()
    all_products = Product.objects.filter(
        section__name__in=["Top Deals Of The Day", "Top Featured Products", "Top Selling Products"]
    ).order_by('-id')

    min_price = Product.objects.aggregate(Min('original_price'))
    max_price = Product.objects.aggregate(Max('original_price'))

    # Fetch the FilterPrice from the URL
    filter_price = request.GET.get('FilterPrice')
    
    # Apply price filter if FilterPrice exists and is not None
    if filter_price and filter_price != 'None':  # Check if the value is not 'None'
        filter_price = int(filter_price)
        all_products = all_products.filter(original_price__lte=filter_price)

    search_query = request.GET.get('search_query', '') 
    if search_query:
        all_products = all_products.filter(product_name__icontains=search_query)

    paginator = Paginator(all_products, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.user.is_authenticated:
        wishlist_items = Wishlist.objects.filter(user=request.user)
        products = [item.product for item in wishlist_items]
    else:
        products = []
    
    data = {
        'category': category,
        'all_products': page_obj,
        'page_obj': page_obj,
        'min_price': min_price,
        'max_price': max_price,
        'FilterPrice': filter_price,  # Passing the FilterPrice here
        'search_query': search_query,
        'products': products,
    }

    return render(request, 'shop.html', data)





def filter_data(request):
    categories = request.GET.getlist('category[]')
    brands = request.GET.getlist('brand[]')
    search_query = request.GET.get('q', '')

    all_products = Product.objects.filter(
        section__name__in=["Top Deals Of The Day", "Top Featured Products", "Top Selling Products"]
    )

    if categories:
        all_products = all_products.filter(category__id__in=categories)

    if brands:
        all_products = all_products.filter(brand__id__in=brands)

    if search_query:
        all_products = all_products.filter(product_name__icontains=search_query)

        

        

    paginator = Paginator(all_products, 8)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    html_content = render_to_string('ajax/shop.html', {'page_obj': page_obj})

    return JsonResponse({'data': html_content})



def wishlist_view(request):
    # Fetch all products in the user's wishlist
    if request.user.is_authenticated:
        wishlist_items = Wishlist.objects.filter(user=request.user)
        products = [item.product for item in wishlist_items]
    else:
        products = []
    
    return render(request, 'wishlist.html', {'products': products})




def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_item = Wishlist.objects.filter(user=request.user, product=product).first()

    if wishlist_item:
        wishlist_item.delete()
        return redirect('wishlist')  # Redirect back to the wishlist page after removal

    return redirect('wishlist')  # In case the item is not in the wishlist


def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)  # Get the product with the given ID
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)

    if not created:  # If the item was already in the wishlist, delete it (toggle behavior)
        wishlist_item.delete()
        return JsonResponse({"status": "removed"})
    
    return JsonResponse({"status": "added"})




@login_required
def clear_wishlist(request):
  
    Wishlist.objects.filter(user=request.user).delete()
    
  
    return redirect('wishlist')  



from buyer.models import Buyer

def checkout(request):
    if request.user.is_authenticated:
        wishlist_items = Wishlist.objects.filter(user=request.user)
        products = [item.product for item in wishlist_items]
    else:
        products = []

    data = {'products': products}

    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        address = request.POST.get("address")
        city = request.POST.get("city")
        postal_code = request.POST.get("postal_code")
        email = request.POST.get("email")
        phone = request.POST.get("phone")

   
        cart = request.session.get("cart", {})
        total_products = len(cart)
        product_names = "(---------NEXT_PRODUCT---------)".join([value["product_name"] for value in cart.values()])

       
        cart_total_amount = sum(int(value["original_price"]) * int(value["quantity"]) for value in cart.values())


        if cart_total_amount <= 2999:
            cart_total_amount += 200 

        try:
            buyer = Buyer.objects.create(
                first_name=first_name,
                last_name=last_name,
                address=address,
                city=city,
                postal_code=postal_code,
                email=email,
                phone=phone,
                total_products=total_products,
                product_names=product_names,
                total_amount=cart_total_amount  
            )
            buyer.save()

            messages.success(request, "Your order has been placed successfully!")

            # Clear Cart After Order
            del request.session["cart"]
            request.session.modified = True

            return redirect("order_success")
        except Exception as e:
            messages.error(request, "Something went wrong. Please try again.")
            print("Error:", e)
            return redirect("checkout")

    return render(request, "checkout.html", data)


def order_success(request):
    

    
    return render (request,'order_success.html')


