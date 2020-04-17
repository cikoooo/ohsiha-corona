from django.db import models
from django.urls import reverse
from datetime import datetime

# Create your models here.

class Newspiece(models.Model):
    Date = models.DateTimeField(default=datetime.now, blank=True)
    Main = models.CharField(max_length=100)
    Support = models.TextField()

    def __str__(self):
        return self.Main
    
    def get_absolute_url(self):
        return reverse('news_edit', kwargs={'pk': self.pk})
