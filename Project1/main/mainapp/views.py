from calendar import monthrange
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.utils import timezone
from django.db.models import Q
from .forms import EventForm, ReadingMaterialForm, ReadingMaterialForm, classListForm
from .models import Event, readingMaterial, classList
from datetime import date, timedelta
from django.shortcuts import render
from datetime import date, timedelta
from calendar import monthcalendar
from datetime import timedelta


# I got a lot of help from here 
#https://www.w3schools.com/django
#and a lot of help from copilot

#todo list view
def todo_list(request): # copilot
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('todo_list')
    else:
        form = EventForm()
    # Get the current date and time
    now = timezone.now()

    # Filter the todos to only include (uncompleted events and events in the past) or (completed events and events in the future)
    todos = Event.objects.filter(
        Q(completed=False, date__lte=now.date()) | 
        Q(date__gte=now.date())
    ).order_by('date', 'time')
    return render(request, 'todo_list.html', {'todos': todos, 'form': form})

def delete_todo(request, todo_id): #copilot wrote this mostly
    todo = get_object_or_404(Event, id=todo_id)
    todo.delete()
    return redirect('todo_list')

#identicle to the delete_todo function but we just mark the todo as completed instead of deleting it. 
def mark_todo_completed(request, todo_id):
    todo = get_object_or_404(Event, id=todo_id)
    todo.completed = True
    todo.save()
    return redirect('todo_list')

def event_detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    return render(request, 'event_detail.html', {'event': event})
  
def home(request):
    return calendar(request, 'month')

def reading_material_view(request):
    form = ReadingMaterialForm()
    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        if form_type == 'add':
            form = ReadingMaterialForm(request.POST)
            if form.is_valid():
                form.save()
            else:
                form = ReadingMaterialForm()
        elif form_type == 'update':
            item_id = request.POST.get('item_id')
            item = readingMaterial.objects.get(id=item_id)
            item.read = 'read' in request.POST
            item.save()
        elif form_type == 'clear':
            readingMaterial.objects.filter(read=True).delete()

    reading_list = readingMaterial.objects.all()
    return render(request, 'readingList.html', {'form': form, 'reading_list': reading_list})

def pomodoro_timer(request):
    return render(request, 'timer.html')

def draw_view(request):
    return render(request, 'draw.html')


def calendar(request, period): # Written in large part by copilot
    today = date.today()

    if(request.method == 'POST'):
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('calendar', period=period)
    else:
        form = EventForm()

    if period == 'month':
        # Create a calendar for the current month
        cal = monthcalendar(today.year, today.month)
    elif period == 'week':
        # Create a calendar for the current week
        start_week = today - timedelta(days=today.weekday())  # Monday
        end_week = start_week + timedelta(days=6)  # Sunday
        cal = [list(range(start_week.day, end_week.day + 1))]
    elif period == 'day':
        # Create a calendar for the current day
        cal = [[today.day]]
    #calendar for a semester ahead 6 months
    elif period == 'semester':
        cal = monthcalendar(today.year, today.month)
        for i in range(5):
            today = today + timedelta(days=30)
            cal += monthcalendar(today.year, today.month)
    else:
        return HttpResponse('Invalid period')
    # Create the weeks list
    weeks = []
    for week in cal:
        week_days = []
        for day in week:
            if day == 0:  # day outside of the month
                week_days.append(None)
            else:
                # Fetch events from your database here
                events = Event.objects.filter(date=date(today.year, today.month, day))
                week_days.append({
                    'day': day,
                    'events': events
                })
        weeks.append(week_days)

    return render(request, 'calendar.html', {'weeks': weeks, 'form': form})




# Class List view
def class_list_view(request): #copilot
    if(request.method == 'POST'):
        form = classListForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('class_list')
    else:
        form = classListForm()
    
    current_classes = classList.objects.filter(currently_taking=True, completed=False)
    completed_classes = classList.objects.filter(completed=True, currently_taking = False)
    future_classes = classList.objects.filter(currently_taking=False, completed=False)
    
    return render(request, 'class_list.html', {'current_classes': current_classes, 'completed_classes': completed_classes, 'future_classes': future_classes, 'form': form})


def delete_class(request, class_id): #copilot
    class_to_delete = get_object_or_404(classList, id=class_id)
    class_to_delete.delete()
    return redirect('class_list')

def hours(request):
    return render(request, 'hours.html')