from django import forms
from django.forms.widgets import SelectDateWidget, TimeInput

from .models import Event
# I got a lot of use from this https://docs.djangoproject.com/en/5.0/ref/forms/widgets/
#https://www.geeksforgeeks.org/django-form-field-custom-widgets/
#https://cdf.9vo.lt/3.0/django.forms.widgets/SelectDateWidget.html

#written in large part by copilot
class EventForm(forms.ModelForm):
    title = forms.CharField(label='Title', max_length=100)
    description = forms.Textarea()
    #todo by should allow the user to select a date and time
    # Got help from here https://stackoverflow.com/questions/72627164/django-datetime-typeerror-fromisoformat-argument-must-be-str
    date = forms.DateField(widget=SelectDateWidget())
    time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    class Meta:                                                                     # and here https://docs.djangoproject.com/en/3.0/ref/forms/widgets/#selectdatewidget
        model = Event
        fields = ['title', 'description', 'date', 'time']

