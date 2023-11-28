from django.db import models
from datetime import timezone
from django.utils import *
from django.contrib.auth.models import * 
from conference.models import conference, ConferenceTopic, ConferenceTrack
# Create your models here.



class CustomUserManager(BaseUserManager):
     def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
     def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser,PermissionsMixin):
    groups = models.ManyToManyField(
        Group,
        verbose_name=('groups'),
        blank=True,
        related_name='customuser_set',  # Add a related_name
        related_query_name='user'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=('user permissions'),
        blank=True,
        related_name='customuser_set',  # Add a related_name
        related_query_name='user'
    )
    name = models.CharField(max_length=70)
    email = models.EmailField(unique=True)
    number = models.CharField(max_length=15)
    password = models.CharField(max_length=500)
    date = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_auth =models.BooleanField(default=False)
    is_reviewer = models.BooleanField(default=False)
    is_conference_admin =models.BooleanField(default=False)
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'number']
    def __str__(self):
        return self.email
    username = models.CharField(max_length=70, null=True, blank=True)
     

class Reviewer_data(AbstractBaseUser,PermissionsMixin):
    groups = models.ManyToManyField(
        Group,
        verbose_name=('groups'),
        blank=True,
        related_name='reviewerdata_set',  # Add a related_name
        related_query_name='user'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=('user permissions'),
        blank=True,
        related_name='reviewerdata_set',  # Add a related_name
        related_query_name='user'
    )
    reviewer_id = models.IntegerField(default=0)
    reviewer_name = models.CharField(max_length=70)
    highest_qualification = models.CharField(max_length=150)
    experience = models.CharField(max_length=150)
    designations = models.CharField(max_length=70)
    organization = models.CharField(max_length=80)
    email = models.EmailField(unique=True)
    reviewer_number = models.CharField(max_length=15)
    whats_app_number = models.CharField(max_length=15)
    password = models.CharField(max_length=250)
    date_reviewer = models.DateTimeField(default=timezone.now)
    photo_upload=models.FileField(upload_to='reviewer/profile-photos/')
    resume_upload=models.FileField(upload_to='reviewer/profile-resume/')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_ok = models.BooleanField(default=False)

    # objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    PASSWORD_FIELD = 'password'
    REQUIRED_FIELDS = ['reviewer_name', 'reviewer_number']
    def __str__(self):
        return self.email

class Author(models.Model):
    email = models.EmailField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    institution = models.CharField(max_length=255)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class paper(models.Model):
    #  id 20231001
     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None)
     title_paper = models.CharField(max_length=255)
    
     track_preference = models.ForeignKey(ConferenceTrack, on_delete=models.SET_NULL, null=True)
     main_topic = models.ForeignKey(ConferenceTopic, on_delete=models.SET_NULL, null=True)
    
     TYPE_CHOICES = [
        ('type1', 'Article'),
        ('type2', 'Presentation Orale'),
        # Add other types as needed
     ]
     contribution_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
     content_type = models.CharField(max_length=255)
     authors = models.ManyToManyField(Author)
     abstract = models.TextField()
     other_topics = models.ManyToManyField(ConferenceTopic, related_name='papers', blank=True)

    
     paper_upload=models.FileField(upload_to='papers/')
     start_date=models.DateTimeField(default=timezone.now)
    #  expiry_date=models.CharField(max_length=20)
     STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        )
     status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
     has_uploaded_paper = models.BooleanField(default=False)
     conference = models.ForeignKey(
        conference,
        on_delete=models.CASCADE,
        default=None,
        null=True,
        related_name='papers'
    )
     
     version = models.PositiveIntegerField(default=1)
     comment1 = models.CharField(max_length=1000,default="Not Available")
     comment2 = models.CharField(max_length=1000,default="Not Available")
     comment3 = models.CharField(max_length=1000,default="Not Available")
     reviewer_comments = models.JSONField(default=dict, blank=True)
     assigned_reviewers = models.ManyToManyField(Reviewer_data, related_name='assigned_papers')
     def assigned_reviewers_list(self):
        return ', '.join([str(reviewer) for reviewer in self.assigned_reviewers.all()])
        assigned_reviewers_list.short_description = 'Assigned Reviewers'
     
     def other_topics_list(self):
        return ', '.join([str(topic) for topic in self.other_topics.all()])
     
     def authors_list(self):
        return ', '.join([str(author) for author in self.authors.all()])

     def __str__(self):
          return self.title_paper

class resubmit_papers(models.Model):

    paper_id=models.IntegerField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None)
    title_paper=models.CharField(max_length=70)
    Auth_name=models.CharField(max_length=70)
    paper_description=models.CharField(max_length=500)
    paper_upload=models.FileField(upload_to='papers/')
    start_date=models.DateTimeField(default=timezone.now)
    #  expiry_date=models.CharField(max_length=20)
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    has_uploaded_paper = models.BooleanField(default=False)
    conference = models.ForeignKey(
        conference,
        on_delete=models.CASCADE,
        default=None,
        null=True,
        related_name='paper'
    )
    Auth_email = models.EmailField(default='example@example.com')
    Auth_affiliation = models.CharField(max_length=100, default='No affiliation')
    Auth_mobile = models.CharField(max_length=20, default='N/A')
    corresponding_auth_name = models.CharField(max_length=100, default='Unknown')
    corresponding_auth_email = models.EmailField(default='corresponding@example.com')
    corresponding_auth_affiliation = models.CharField(max_length=100, default='No affiliation')
    corresponding_auth_mobile = models.CharField(max_length=20, default='N/A')
    other_auth_name = models.CharField(max_length=100, default='Unknown')
    other_auth_email = models.CharField(max_length=150,default='other@example.com')
    other_auth_affiliation = models.CharField(max_length=100, default='No affiliation')
    other_auth_mobile = models.CharField(max_length=20, default='N/A')
    paper_keyword = models.CharField(max_length=100, default='No keywords')
    version = models.PositiveIntegerField(default=1)
    comment1 = models.CharField(max_length=1000,default="Not Available")
    comment2 = models.CharField(max_length=1000,default="Not Available")
    comment3 = models.CharField(max_length=1000,default="Not Available")
    reviewer_comments = models.JSONField(default=dict, blank=True)
    def comment_for_reviewer(self, reviewer):
        return self.comments.get(str(reviewer.id), "")
    assigned_reviewers = models.ManyToManyField(Reviewer_data, related_name='resubmit_papers')
    def assigned_reviewers_list(self):
        return ', '.join([str(reviewer) for reviewer in self.assigned_reviewers.all()])
        assigned_reviewers_list.short_description = 'Assigned Reviewers'
    

    def __str__(self):
        return self.title_paper