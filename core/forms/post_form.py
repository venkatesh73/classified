from django import forms
from core.models import Classifieds, SubCategory, City, Category
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from django_summernote.fields import SummernoteTextFormField, SummernoteTextField
from django.core.exceptions import ValidationError 
from tempus_dominus.widgets import DatePicker
import datetime
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

class CreatePostForm(forms.ModelForm):
    title = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder' : 'Title'}))
    sub_category = forms.ModelChoiceField(queryset=SubCategory.objects.all().order_by('name'), widget=forms.Select(attrs={'class': 'form-control', 'placeholder' : 'Select Category'}))
    cities = forms.ModelMultipleChoiceField(queryset=City.objects.all().order_by('name'), widget=forms.SelectMultiple(attrs={'class': 'form-control', 'placeholder' : 'Select Cities'}))
    price = forms.CharField(required = False, max_length=25, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder' : 'Price'}))
    description = SummernoteTextFormField()
    price_on_call = forms.BooleanField(required = False, widget=forms.CheckboxInput(attrs={'class': 'custom-control-input'}))
    valid_till = forms.DateField(widget=DatePicker(options={
                'minDate': (datetime.date.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d'),
                'useCurrent': True,
                'collapse': False,
            }
        ))
    classifieds_media = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True, 'id' : 'tg-photogallery', 'class' : 'tg-fileinput'}))

    class Meta:
        model = Classifieds
        fields = [
            "title",
            "sub_category",
            "cities",
            "price",
            "price_on_call",
            "valid_till",
            "description",
            "classifieds_media"
        ]

    def clean_classifieds_media(self):
        files = self.files.getlist('classifieds_media')
        if len(files) < 3:
            raise forms.ValidationError('Upload minmum of 3 Media files and max to 5.')

        if len(files) > 5:
            raise forms.ValidationError('Upload minmum of 3 Media files and max to 5.')

        valid_sizes = True
        for media in files:
            if media.size > 500000:
                valid_sizes = False

        if not valid_sizes:
            raise forms.ValidationError('Uploaded file sizes should be less than or equal to 500KB.')

        return None