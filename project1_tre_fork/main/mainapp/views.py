from calendar import monthrange
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.utils import timezone
from django.db.models import Q
from .forms import EventForm, ReadingMaterialForm, ReadingMaterialForm, classListForm
from .models import Event, readingMaterial, classList, KudosCounter
from datetime import date, timedelta
from django.shortcuts import render
from datetime import date, timedelta, datetime
from calendar import monthcalendar, monthrange
from datetime import timedelta
import calendar
import os
import random
from django.conf import settings
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
import os
import random
from django.conf import settings
from datetime import timezone as dt_timezone


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

    # Tre: Get or create the KudosCounter object
    kudos_counter, created = KudosCounter.objects.get_or_create()
    if created:
        # If the object was created, initialize its count
        kudos_counter.count = 0
        kudos_counter.save()

    return render(request, 'todo_list.html', {'todos': todos, 'form': form, 'kudos_counter': kudos_counter}) # Tre: added kudos counter val to return 

def delete_todo(request, todo_id): #copilot wrote this mostly
    todo = get_object_or_404(Event, id=todo_id)
    todo.delete()
    return redirect('todo_list')

#identicle to the delete_todo function but we just mark the todo as completed instead of deleting it. 
def mark_todo_completed(request, todo_id):
    todo = get_object_or_404(Event, id=todo_id)

    # Tre - adding kudos whenever item newly marked completed
    if todo.completed == False: # this way you can't just remark it
        kudos_counter = KudosCounter.objects.first()
        kudos_counter.count += 1 # incrementing by 1 for now
        kudos_counter.save()

    todo.completed = True # Tre: moved this down here

    todo.save()
    return redirect('todo_list')

def event_detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    return render(request, 'event_detail.html', {'event': event})
  
def home(request):
    return calendar_view(request, 'month')

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


#Safari -- Copilot wrote this -- Super simple
#View function to display our timer page
def pomodoro_timer(request):
    return render(request, 'timer.html')

#Safari -- Copilot wrote this 
#View function to display our draw page
def draw_view(request):
    return render(request, 'draw.html')

def add_months(source_date, months):
    month = source_date.month - 1 + months
    year = source_date.year + month // 12
    month = month % 12 + 1
    return date(year, month, 1)

def calendar_view(request, period):
    today = date.today()

    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('calendar', period=period)  # Adjust the redirect as needed
    else:
        form = EventForm()

    months_with_weeks = {}
    # if the persiod is a wee
    if period == 'week':
        start_week = today - timedelta(days=today.weekday()) # Get the first day of the week
        week_name = f"Week of {start_week.strftime('%B %d, %Y')}" # Generate the week's name
        week_days = []  # This will hold the days of the week
        for i in range(7): # Generate the data for each day in the week
            day_date = start_week + timedelta(days=i)   # Get the date of the day
            events = Event.objects.filter(date=day_date) # Get the events for the day
            # Append each day's data directly into the week_days list
            week_days.append({'day': day_date.day, 'events': events}) 
        # Now, week_days is a single list representing one week, as expected by the template
        months_with_weeks[week_name] = [week_days]  # Wrap week_days in a list to match the expected structure

    # Handle month and semester views
    elif period in ['month', 'semester']:
        months_to_generate = 1 if period == 'month' else 6
        start_month = today.replace(day=1)
        # Generate the data for each month
        for i in range(months_to_generate):
            month_date = add_months(start_month, i)
            month_name = calendar.month_name[month_date.month] + " " + str(month_date.year)
            month_days = monthcalendar(month_date.year, month_date.month)
            weeks = []
            # Move on to each individual week
            for week in month_days:
                week_days = []
                # Move on to each day in the week
                for day in week:
                    if day != 0: # If it's a day in the current month
                        day_date = date(month_date.year, month_date.month, day)
                        events = Event.objects.filter(date=day_date)
                        day_info = {'day': day, 'events': events}
                    else:
                        day_info = None
                    week_days.append(day_info) # Append the day's data to the week
                weeks.append(week_days)
            months_with_weeks[month_name] = weeks

    return render(request, 'calendar.html', {'months_with_weeks': months_with_weeks, 'form': form})

#Safari -- Copilot helped write this one as well

# Tre -- code for generating iCal files from calendar:
def generate_ical(events):
    """
    Generate iCal data from a list of events.
    """
    ical_data = "BEGIN:VCALENDAR\n"
    ical_data += "VERSION:2.0\n"
    ical_data += "CALSCALE:GREGORIAN\n"
    ical_data += "X-WR-CALNAME:NCFTaskNinja\n"
    ical_data += "X-WR-TIMEZONE:America/New_York\n"

    for event in events:
        ical_data += "BEGIN:VEVENT\n"
        ical_data += f"UID:{event.id}@ncftaskninja.com\n"  # Unique identifier for the event
        ical_data += f"SUMMARY:{event.title}\n"
        ical_data += f"DESCRIPTION:{event.description}\n"
        event_time = datetime.combine(event.date, event.time) + timedelta(hours=5) # love a ductape solution to timezone shenanigans
        start_datetime = event_time.strftime('%Y%m%dT%H%M%S') # sorry for the long line
        ical_data += f"DTSTART:{start_datetime}Z\n"
        ical_data += f"DTEND:{start_datetime}Z\n" # not sure why google datetimes end in Zs for their icals
        ical_data += "END:VEVENT\n"
    ical_data += "END:VCALENDAR\n"
    return ical_data

def generate_ical_view(request):
    """
    View to generate and serve the iCal file.
    """
    if request.method == 'POST':
        # Fetch all events (you might want to filter them based on the displayed ones)
        events = Event.objects.all()
        ical_data = generate_ical(events)
        response = HttpResponse(ical_data, content_type='text/calendar')
        response['Content-Disposition'] = 'attachment; filename="calendar.ics"'
        return response
    else:
        return HttpResponseBadRequest()

# View function for displaying memes
def memes(request):
    images_dir = os.path.join(settings.BASE_DIR, 'mainapp', 'static', 'images') # Tre: adding settings.BASE_DIR made it work on my branch
    image_files = os.listdir(images_dir)
    random_image = random.choice(image_files)
    context = {
        'random_image': random_image
    }
    return render(request, 'memes.html', context)


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