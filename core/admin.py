from django.contrib import admin
from core.models import Category, SubCategory, City, Classifieds, ClassifiedsInterest

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')

class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('category', 'name')

class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')

class ClassifiedsAdmin(admin.ModelAdmin):
    list_display = ('title', 'sub_category', 'user')

class ClassifiedsInterestAdmin(admin.ModelAdmin):
    list_display = ('classifieds', 'user')

admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Classifieds, ClassifiedsAdmin)
admin.site.register(ClassifiedsInterest, ClassifiedsInterestAdmin)

