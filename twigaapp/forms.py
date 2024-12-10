from django import forms
from twigaapp.models import Bookings, ImageModels
from django.core.exceptions import ValidationError


class BookingForm(forms.ModelForm):
    class Meta:
        model = Bookings
        fields = '__all__'


class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = ImageModels
        fields = ['image', 'title', 'description']

    def clean_title(self):
        title = self.cleaned_data.get('title')
        max_title_length = 100
        if len(title) > max_title_length:
            raise ValidationError(f"Title cannot be more than {max_title_length} characters.")
        return title

    def clean_description(self):
        description = self.cleaned_data.get('description')
        max_description_length = 500
        if description and len(description) > max_description_length:
            raise ValidationError(f"Description cannot be more than {max_description_length} characters.")
        return description

