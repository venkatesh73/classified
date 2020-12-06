from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from core.core_modules import *
from core.models import Category, SubCategory, ClassifiedsMedia, Classifieds
from core.forms.sign_up_form import SignUpForm
from core.forms.login_form import SignInForm
from core.forms.post_form import CreatePostForm
from django.contrib.auth.decorators import login_required
from django.conf import settings
import uuid
import os

def index(request):
    locations = get_locations()
    categories = get_categories()
    latest_products = get_latest_products()

    response = {
        "locations": locations,
        "categories": categories,
        "latest_products": latest_products
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
            login(request, user)
            return HttpResponseRedirect('/dashboard')

    return render(request, 'signin.html', {'form' : form})

def signout(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required(login_url='signin')
def dashboard(request):
    return render(request, 'dashboard.html', {})

def category(request):
    return render(request, 'category.html', {})

def classifieds(request, category_id = None, location = None):
    return render(request, 'classifieds.html', {})

@login_required(login_url="signin")
def post_classifieds(request):
    if request.method == "POST":
        form  = CreatePostForm(request.POST, request.FILES)
        print(request.FILES.getlist('classifieds_media'))
        if form.is_valid():
            post_details = form.save(commit=False)
            post_details.user_id = request.user.id
            post_details.save()
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
