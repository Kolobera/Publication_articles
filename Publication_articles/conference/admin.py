from django.contrib import admin

# Register your models here.
from .models import *


class Conference_Admin(admin.ModelAdmin):
    list_display = ('id','conference_name','conference_user','conference_descriptions','conference_start_date','conference_end_date','has_uploaded_paper','conference_mode','conference_venue', 'tracks_list', 'topics_list')


admin.site.register(conference,Conference_Admin)

class ConferenceTrack_Admin(admin.ModelAdmin):
    list_display = ('id', 'track_name')

admin.site.register(ConferenceTrack, ConferenceTrack_Admin)

class ConferenceTopic_Admin(admin.ModelAdmin):
    list_display = ('id', 'topic_name')

admin.site.register(ConferenceTopic, ConferenceTopic_Admin)