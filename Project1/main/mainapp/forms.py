from django import forms
from .models import TodoList
#written in large part by copilot
class TodoListForm(forms.ModelForm):
    title = forms.CharField(label='Title', max_length=100)
    description = forms.Textarea()
    class Meta:
        model = TodoList
        fields = ['title', 'description']
