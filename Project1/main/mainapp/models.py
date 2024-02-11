from django.db import models

# Create your models here.
class readingMaterial(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    link = models.URLField()
    read = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title