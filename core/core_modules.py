from core.models import Category, City, Classifieds

def get_locations():
    locations = City.objects.filter(active=True ).order_by('name')
    return locations

def get_categories():
    categories = Category.objects.filter(active = True).order_by('name')
    return categories

def get_latest_products():
    return {}