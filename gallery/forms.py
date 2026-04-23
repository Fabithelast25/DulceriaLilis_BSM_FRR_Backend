from django import forms
from .models import GalleryImage

class ImageForm(forms.ModelForm):
    class Meta:
        model = GalleryImage
        fields = ['image']