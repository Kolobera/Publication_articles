from django.db import models

# Create your models here.
from django.db import models
from django.forms import DateTimeField
from django.utils import timezone


class conference(models.Model):
     conference_name = models.CharField(max_length=80)
     conference_descriptions = models.CharField(max_length=600)

     conference_start_date = models.DateTimeField(default=timezone.now)
     conference_end_date = models.DateField()
     conference_venue=models.CharField(max_length=250,default="online",null=True)
     STATUS_CHOICES = (
        ('online', 'Online'),
        ('offline', 'Offline'),
        ('hybrid', 'Hybrid'),
        )
     conference_mode= models.CharField(max_length=20, choices=STATUS_CHOICES, default='online')

     conference_user = models.CharField(default="Not present",max_length=150)
     
     has_uploaded_paper = models.BooleanField(default=False)
     tracks = models.ManyToManyField('ConferenceTrack', related_name='conferences', blank=True)

     topics = models.ManyToManyField('ConferenceTopic', related_name='conferences', blank=True)

     def tracks_list(self):
        return ', '.join([str(track) for track in self.tracks.all()])

     def topics_list(self):
        return ', '.join([str(topic) for topic in self.topics.all()])
        
     
     def __str__(self):
          return self.conference_name
     
class ConferenceTrack(models.Model):
    track_name = models.CharField(max_length=100)

    def __str__(self):
        return self.track_name


class ConferenceTopic(models.Model):
    topic_name = models.CharField(max_length=100)

    def __str__(self):
        return self.topic_name