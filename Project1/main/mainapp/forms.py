from django import forms
from .models import readingMaterial

class ReadingMaterialForm(forms.ModelForm):
    class Meta:
        model = readingMaterial
        fields = ['title', 'author', 'type', 'link']