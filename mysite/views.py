from django.http import HttpResponse
from django.shortcuts import render,redirect
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















