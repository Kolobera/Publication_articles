from django.shortcuts import render , redirect ,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import *
from .models import *
from users.models import  CustomUser,CustomUserManager 
from django.contrib.auth import get_user_model 
from django.contrib.auth.decorators import login_required
from users.models import paper ,resubmit_papers
from django.contrib.auth import authenticate, login , logout 
from conference.models import conference
from users.models import Reviewer_data
from django.http import JsonResponse
# Create your views here ....


user=get_user_model
def login_view(request):
    if request.method == 'POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        user =authenticate(request,email=email,password=password)
        if user is not None :
            login(request,user)
            return redirect('dashboard')
        else:
            context = {'error_message': 'Invalid email or password'}
            return render(request, 'login/login.html', context)
            
    else:
            return render(request, 'login/login.html')


def logout_Admin(request):
    logout(request)
    return redirect('login')

def dashboard(request):
    print("He is Login As Admin",request.user)
    if request.user.is_authenticated and request.user.is_conference_admin :
        user = request.user
        fname = user.name
        return render(request,'login/dashboard.html',{'name':fname})
    else:
        return redirect('login')

def list_of_paper(request, conference__id):
    if request.user.is_authenticated and request.user.is_conference_admin:
        user = request.user
        conf=conference.objects.get(id=conference__id)
        conf.conference_user=user.email
        conf.save()
        reviewer_data_dict = {reviewer.id: reviewer for reviewer in Reviewer_data.objects.all()}
        context={
            'paper':paper.objects.filter(conference_id=conference__id),
            'reupload_paper':resubmit_papers.objects.filter(conference_id=conference__id),  
            'user':request.user,
            'reviewer_data_dict': reviewer_data_dict,
        }
        return render(request,'login/papers_list.html',context)
    else:
        return redirect('login')

def list_of_conference(request):
    if request.user.is_authenticated and request.user.is_conference_admin:
        user = request.user
        email=user.email
        print("He Check The Conference List",user.name)
        context={
            'conference':conference.objects.filter(conference_user=email)
        }
        return render(request,"login/conferences_list.html",context)
    else:
        return redirect('login')

def update_paper_status(request, selected_paper_id):
    if request.user.is_authenticated and request.user.is_conference_admin and request.method == 'POST':
        new_status = request.POST.get('status')
        papers = get_object_or_404(paper, id=selected_paper_id)
        papers.status = new_status
        papers.save()
        return redirect('list-of-conference')
    else:
        return redirect('login')
def resubmit_paper_status(request, selected_paper_id):
    if request.user.is_authenticated and request.user.is_conference_admin and request.method == 'POST':
        new_status = request.POST.get('status')
        print(new_status)
        resubmit_paper = get_object_or_404(resubmit_papers, id=selected_paper_id)
        resubmit_paper.status = new_status
        resubmit_paper.save()
        return redirect('list-of-conference')
    else:
        return redirect('login')

def create_conference(request):
    if request.user.is_authenticated and request.user.is_conference_admin:
        user = request.user
        fname = user.name
        conferences = conference.objects.all()
        if request.method == 'POST':
            
            conference_name = request.POST.get('conference_name')
            user = request.user
            conference_description = request.POST.get('conference_description')
            conference_end_date = request.POST.get('conference_end_date')
            conference_mode = request.POST.get('conference_mode')
            conference_venue = request.POST.get('Venue')
            New_Conference = conference.objects.create(
                conference_name=conference_name,conference_descriptions=conference_description,
                conference_end_date=conference_end_date,conference_mode=conference_mode,conference_venue=conference_venue, conference_user=user.email,
            )
            New_Conference.save()
            context_success = {
                "success_message":"Your Conference Created Successfully :-)",
                "conference":conference.objects.all(),
                "name":fname,
                "STATUS_CHOICES": conference.STATUS_CHOICES,
                }
            return render(request, 'login/create_conference.html', context_success)
        else:
            context={
                "conference":conference.objects.all(),
                "name":fname,
                "STATUS_CHOICES": conference.STATUS_CHOICES,
            }
            return render(request,'login/create_conference.html',context)
    else:
        return redirect('login')
    

# views.py
def list_of_reviewer(request):
    if request.user.is_authenticated and request.user.is_conference_admin:
        if request.method == 'POST':
            user_id = request.POST.get('user_id')
            is_ok = request.POST.get('is_ok') == 'true'  # Use lowercase 'true'

            try:
                reviewer = Reviewer_data.objects.get(reviewer_id=user_id)
                reviewer.is_ok = is_ok
                reviewer.save()
                return JsonResponse({'status': 'success'})
            except Reviewer_data.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Reviewer not found'})
        reviewer = Reviewer_data.objects.all()
        context ={
            'reviewer':reviewer,
        }
        return render(request,'login/list-of-reviewer.html',context)
    else:
        return redirect('login')

def reviewers_profile(request, reviewer_id):
    if request.user.is_authenticated and request.user.is_conference_admin:
        reviewer_instance=Reviewer_data.objects.get(id=reviewer_id)   
        context={
            "reviewer" : reviewer_instance,
        }    
        return render(request,'login/reviewer_profile.html',context)
    else:
        return redirect('login')

def assign_paper(request):
    if request.user.is_authenticated and request.user.is_conference_admin:
        reviewer = Reviewer_data.objects.all()
        context ={
            'reviewer':reviewer,
        }
        return render(request,'login/assing_reviewer_paper.html',context)
    else:
        return redirect('login')

def list_of_paper_sing_re(request, reviewer_id):
    if request.user.is_authenticated and request.user.is_conference_admin:
        # paper = paper.objects.filter(assigned__contains=[reviewer_id])
        reviewer = Reviewer_data.objects.get(reviewer_id=reviewer_id)
        if request.method=='POST':
            selected_paper_ids = request.POST.getlist('papers_to_assign')
            reviewer = Reviewer_data.objects.get(reviewer_id=reviewer_id)
            for paper_id in selected_paper_ids:
                papers1 = resubmit_papers.objects.get(id=paper_id)
                papers1.assigned_reviewers.add(reviewer)
                # papers1.assigned_reviewers_id = reviewer_id
                papers1.save()
            return redirect('Assign_paper')
        else:
            papers = paper.objects.all()
            resubmit_paper = resubmit_papers.objects.all()
            context = {
                'reviewer_id':reviewer_id,
                'reviewer': reviewer,
                'papers':papers,
                'resubmit_paper':resubmit_paper
            }
            return render(request, 'login/list_of_paper_sing.html', context)
    else:
        return redirect('login')
    
def list_of_paper_sing(request, reviewer_id):
    if request.user.is_authenticated and request.user.is_conference_admin:
        # paper = paper.objects.filter(assigned__contains=[reviewer_id])
        reviewer = Reviewer_data.objects.get(reviewer_id=reviewer_id)
        if request.method=='POST':
            selected_paper_ids = request.POST.getlist('papers_to_assign')
            reviewer = Reviewer_data.objects.get(reviewer_id=reviewer_id)
            for paper_id in selected_paper_ids:
                papers1 = paper.objects.get(id=paper_id)
                # papers1.assigned_reviewers_id = reviewer_id
                papers1.assigned_reviewers.add(reviewer)
                papers1.save()
            return redirect('Assign_paper')
        else:
            papers = paper.objects.all()
            resubmit_paper = resubmit_papers.objects.all()
            context = {
                'reviewer_id':reviewer_id,
                'reviewer': reviewer,
                'papers':papers,
                'resubmit_paper':resubmit_paper
            }
            return render(request, 'login/list_of_paper_sing.html', context)
    else:
        return redirect('login')