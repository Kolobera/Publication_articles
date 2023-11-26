"""Login URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include
from conference import views

urlpatterns = [
    path('',views.login_view,name="login"),
    path('login/',views.login_view,name="login"),
    path("dashboard/",views.dashboard,name="dashboard"),
    path('dashboard/list-of-paper/<int:conference__id>/',views.list_of_paper,name="list-of-paper"),
    path('dashboard/list-of-paper/update-paper-status/<int:selected_paper_id>/', views.update_paper_status, name='update_paper_status'),
    path('dashboard/list-of-paper/resubmit_paper_status/<int:selected_paper_id>/', views.resubmit_paper_status, name='resubmit_paper_status'),
    path('dashboard/create-conference/',views.create_conference,name="create_conference"),
    path('dashboard/list-of-conference/',views.list_of_conference,name="list-of-conference"),
    path('dashboard/list-of-reviewer/',views.list_of_reviewer,name="list-of-reviewer"),
    
    path('dashboard/profile/<int:reviewer_id>/',views.reviewers_profile,name="reviewer_profile"),

    path('dashboard/Assing-paper/',views.assign_paper,name="Assign_paper"),
    path('dashboard/Assing-paper/<int:reviewer_id>/',views.list_of_paper_sing,name="Assign_reviewer_paper"),
    path('dashboard/Assing-paper/resubmitted/<int:reviewer_id>/',views.list_of_paper_sing_re,name="Assign_reviewer_paper_re"),

    path('logout/',views.logout_Admin,name="logout_Admin"),
   
]
