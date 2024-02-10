from django.shortcuts import get_object_or_404, render, redirect
from .forms import TodoListForm
from .forms import TodoListForm
from .models import TodoList
# I got a lot of help from here 
#https://www.w3schools.com/django




#todo list view

def todo_list(request): # copilot
    if request.method == 'POST':
        form = TodoListForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('todo_list')
    else:
        form = TodoListForm()
    todos = TodoList.objects.all()
    return render(request, 'todo_list.html', {'todos': todos, 'form': form})

def delete_todo(request, todo_id): #copilot wrote this mostly
    todo = get_object_or_404(TodoList, id=todo_id)
    todo.delete()
    return redirect('todo_list')

#identicle to the delete_todo function but we just mark the todo as completed instead of deleting it. 
def mark_todo_completed(request, todo_id):
    todo = get_object_or_404(TodoList, id=todo_id)
    todo.completed = True
    todo.save()
    return redirect('todo_list')