from django.contrib import admin
from django.urls import path , include
from users import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    
    path('',views.index,name='index'),
    path('sing-up-review/',views.sing_up_reviewer,name='reviewer-sing-up'),
    path('sing-in/',views.sing_in_reviewer,name='reviewer-sing-in'),
    path('sing-out/',views.sing_out_reviewer,name='reviewer-sing-out'),
    path('dashboard/',views.dashboard_reviewer,name='reviewer-dashboard'),
    path('activate-reviewer/<str:uidb64>/<str:token>/',views.activate_reviewer,name="activate_reviewer"),

    path('profile/<int:reviewer_id>/',views.reviewer_profile,name="profile"),

    path('review-paper/<paper_id>/',views.paper_reviewer,name="paper_reviewer"),
    path('paper-reviewer-resubmit/<paper_id>/',views.paper_reviewer_resubmit,name="paper_reviewer_resubmit"),

    path('list-of-submitted-paper/',views.list_of_submitted_papers,name="list-of-submitted-paper"),
    path('list-of-resubmitted-paper/',views.list_of_resubmitted_papers,name="list-of-resubmitted-paper"),
    path('signup/',views.singup_view,name="singup"),
    path('singin/',views.singIn,name="singin"),
    path('success/', views.success_view, name='success'),
    path('success/logout/',views.logout_page,name="logout"),
    path('activate/<str:uidb64>/<str:token>/',views.activate,name="activate"),
    path('success/conference_detail/<int:conf_id>/submit/',views.submit_paper,name="submit"),
    path('success/conference_detail/resubmit/<int:paper_id>/',views.resubmit,name="resubmit"),
    path('success/conference_detail/resubmit-again/<int:re_paper_id>/',views.re_resubmit,name="re_resubmit"),
    path('success/list-of-Papers/<int:conf_id>/',views.list_of_paper,name="list_of_paper"),
    path('success/list-of-conference/',views.list_of_conference,name="list_of_conference"), 
    path('success/conference_detail/<int:conf_id>/', views.conference_detail, name='conference_detail'),
   



]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
