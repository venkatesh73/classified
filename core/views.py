from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from core.core_modules import *
# from core.models import Category, SubCategory, ClassifiedsMedia, Classifieds
from core.forms.sign_up_form import SignUpForm
from core.forms.login_form import SignInForm
from core.forms.post_form import CreatePostForm
from django.contrib.auth.decorators import login_required
from django.conf import settings
import uuid
import os
from urllib.parse import parse_qs, urlparse

def index(request):
    locations = get_locations()
    categories = get_categories()
    latest_products = get_latest_products()
    sub_categories = sub_categoreis_post_count()
    
    response = {
        "locations": locations,
        "categories": categories,
        "latest_products": latest_products,
        'sub_categories' :  sub_categories.items()
    }

    return render(request, 'index.html', response)

def signup(request):
    form = SignUpForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=email, password=password)
            login(request, user)
            return HttpResponseRedirect('/')
    
    return render(request, 'signup.html', {'form' : form})

def signin(request):
    form = SignInForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/dashboard')
            else:
                return render(request, 'signin.html', {'form' : form})
    return render(request, 'signin.html', {'form' : form})

def signout(request):
    logout(request)
    return HttpResponseRedirect('/')

def reset_password(request):
    return render(request, 'forgot-password.html', {})

@login_required(login_url='signin')
def dashboard(request):
    return render(request, 'dashboard.html', {})

def classifieds(request):
    params = request.GET
    filters = models.Q(active=True)

    if 'city' in params:
        filters &= models.Q(
            cities__in=params['city'],
        )

    if 'category' in params:
        filters &= models.Q(
            sub_category=params['category'],
        )
        
    locations = get_locations()
    sub_categories = sub_categoreis_post_count()
    
    qs = Classifieds.objects.filter(filters).order_by('-id')

    for post in qs:
        media = ClassifiedsMedia.objects.filter(classifieds=post.id, type__icontains="image").first()
        setattr(post, "media", media)
    
    return render(request, 'classifieds.html', {
        'locations' : locations,
        'sub_categories' :  sub_categories.items(),
        'classifieds' : qs
    })

def post_info(request, id):
    post = Classifieds.objects.filter(id=id, active=True)[0]
    if post:
        media = ClassifiedsMedia.objects.filter(classifieds=post)
        setattr(post, 'media', media)
        print(post)
        return render(request, 'ads-details.html', {'post':  post})
    else:
        return render(request, '404.html', {})

@login_required(login_url="signin")
def post_classifieds(request):
    if request.method == "POST":
        form  = CreatePostForm(request.POST, request.FILES)
        if form.is_valid():
            post_details = form.save(commit=False)
            post_details.user_id = request.user.id
            post_details.save()
            form.save_m2m()
            files = request.FILES.getlist('classifieds_media')
            for media in files:
                file_path = handle_uploaded_file(media)
                ClassifiedsMedia.objects.create(
                    classifieds = post_details,
                    media_url = file_path,
                    type = media.content_type
                )
            return HttpResponseRedirect('/myads')    
    else:
        form  = CreatePostForm()

    return render(request, 'post_classifieds.html', {'form' : form})

def handle_uploaded_file(f):
    _filename, file_extension = f.name.split(".")
    file_path = settings.CLASSIFIEDS_MEDIA_ROOT
    file_name = 'classifieds_media/' + str(uuid.uuid4()) + '.' + file_extension
    with open(file_path + file_name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    
    return file_name

@login_required(login_url="signin")
def my_ads(request):
    user_classifieds = Classifieds.objects.filter(user=request.user.id)
    for post in user_classifieds:
        media = ClassifiedsMedia.objects.filter(classifieds=post.id, type__icontains="image").first()
        setattr(post, "media", media)

    return render(request, 'myads.html', {'myads' : user_classifieds})

def create_sub_category_fixtures():
    sub_categories = {
        "Commercial Equipment & Tools" : ["Industrial Ovens", "Manufacturing Equipment", "Manufacturing Materials", "Medical Equipment", "Printing Equipment", "Restaurant & Catering Equipment", "Safety Equipment", "Salon Equipment", "Stage Lighting & Effects", "Stationery", "Store Equipment"],
        "Electronics" : ["Accessories" ,"Laptops & Computers" ,"TV & DVD Equipment" ,"Audio & Music Equipment" ,"Computer Accessories" ,"Computer Hardware" ,"Computer Monitors" ,"Headphones" ,"Networking Products" ,"Photo & Video Cameras" ,"Printers & Scanners" ,"Security & Surveillance" ,"Software" ,"Video Games" ,"Video Game Consoles"],
        "Furniture & Appliances" : ["Furniture", "Garden", "Home Accessories", "Home Appliances", "Kitchen Appliances", "Kitchen & Dining"],
        "Property" : ["Houses & Apartments For Rent", "Houses & Apartments For Sale", "Land & Plots for Rent", "Land & Plots For Sale", "Commercial Property For Rent", "Commercial Property For Sale", "Event centres, Venues and Workstations", "Short Let"],
        "Repair & Construction" : ["Building Materials", "Doors", "Electrical Equipment", "Electrical Tools", "Hand Tools", "Measuring & Layout Tools", "Plumbing & Water Supply", "Solar Energy", "Windows", "Other Repair & Construction Items"],
        "Vehicles" : ["Cars", "Buses & Microbuses", "Heavy Equipment", "Motorcycles & Scooters", "Trucks & Trailers", "Vehicle Parts & Accessories", "Watercraft & Boats",]
    }

    schema = []
    pk = 0
    for obj in sub_categories:
        category = Category.objects.get(name=obj).id
        for sub_cat in sub_categories[obj]:
            pk = pk + 1
            sub_cat_schema = {
                "model": "core.sub_category",
                "pk": pk,
                "fields": {
                    "category": category,
                    "name": sub_cat,
                    "created_at": "2020-11-18 10:32:37",
                    "updated_at": "2020-11-18 10:32:37"
                }
            }
            schema.append(sub_cat_schema)
    
    with open("./core/fixtures/sub_category.json", "w") as fout:
        print(schema, file=fout)

    return True

