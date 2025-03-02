from django.http import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from slider.models import Slider
from app.models import Main_Category
from product.models import Product,Section
def index(request):
    slider = Slider.objects.all().order_by('-id')
    main_category = Main_Category.objects.all()
    top_deals = Product.objects.filter(section__name="Top Deals Of The Day")
    top_featured = Product.objects.filter(section__name="Top Featured Products")
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







