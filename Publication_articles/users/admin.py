from django.contrib import admin

# Register your models here.
from .models import *
class PaperAdmin(admin.ModelAdmin):
    list_display=('id','user','title_paper','track_preference','main_topic','contribution_type','content_type','authors_list','abstract','other_topics_list','conference','paper_upload','start_date','status','reviewer_comments','comment1','comment2','comment3','assigned_reviewers_list')
    list_filter = ('status',)
    actions = ['make_change']
    def make_change(self, request, queryset):
        # L'action que vous voulez effectuer lorsqu'on choisit "Change" depuis l'interface d'administration
        for paper in queryset:
            paper.save()

    make_change.short_description = "Modifier les papiers sélectionnés"
admin.site.register(paper,PaperAdmin)

class Resubmit_papers_admin(admin.ModelAdmin):
    list_display=('id','paper_id','user','conference','title_paper','Auth_name','paper_description','paper_upload','start_date','status','version','assigned_reviewers_list','reviewer_comments')
    list_filter = ('status',)
admin.site.register(resubmit_papers,Resubmit_papers_admin)

class CustomUserAdmin_by(admin.ModelAdmin):
    list_display=('name','id','email','number','date','is_active','is_staff','is_conference_admin','is_reviewer','is_auth','password')

admin.site.register(CustomUser,CustomUserAdmin_by)

class Reviewer_admin(admin.ModelAdmin):
    list_display=('id','reviewer_name','reviewer_id','highest_qualification','experience','designations','organization','email','reviewer_number','whats_app_number','password','date_reviewer','photo_upload','resume_upload','is_active','is_ok','is_staff')

admin.site.register(Reviewer_data, Reviewer_admin)

class Author_admin(admin.ModelAdmin):
    list_display=('id','email','first_name','last_name','institution', 'country')

admin.site.register(Author, Author_admin)
