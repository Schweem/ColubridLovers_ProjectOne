from django.db import models
# docs powered by CoPilot

#todo list model
class Event(models.Model):
    """
    Represents an event.

    Attributes:
        title (str): The title of the event.
        description (str): The description of the event.
        completed (bool): Indicates whether the event is completed or not.
        date (datetime.date): The date of the event.
        time (datetime.time): The time of the event.
        created_at (datetime.datetime): The timestamp when the event was created.
    """
    title = models.CharField(max_length=100)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    date = models.DateField()
    time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)

class readingMaterial(models.Model):
    """
    Represents a piece of reading material.

    Attributes:
        title (str): The title of the reading material.
        author (str): The author of the reading material.
        type (str): The type or category of the reading material.
        link (str): The URL link to the reading material.
        read (bool): Indicates whether the reading material has been read or not.
    """

    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    link = models.URLField()
    read = models.BooleanField(default=False)

    def __str__(self):
        return self.title