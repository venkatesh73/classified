from core.models import *

def get_locations():
    locations = City.objects.filter(active=True ).order_by('name')
    return locations

def get_categories():
    categories = Category.objects.filter(active = True).order_by('name')
    return categories

def get_latest_products():
    products = Classifieds.objects.filter(active=True).order_by('-id')[:10]
    for post in products:
        media = ClassifiedsMedia.objects.filter(classifieds=post.id, type__icontains="image").first()
        setattr(post, "media", media)
    
    return products

def sub_categoreis_post_count():
    categories = get_categories()
    results = {}
    for cat in categories:
        sub_cat = SubCategory.objects.filter(active=True, category=cat.id).order_by('name')
        results[cat.name] = sub_cat
    
    return results