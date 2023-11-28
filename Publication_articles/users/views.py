from django.shortcuts import render , HttpResponse , redirect
from Publication_articles import settings
from django.contrib.auth import authenticate, login , logout
from django.urls import reverse
from users.models import Reviewer_data
from users.models import CustomUser , paper , resubmit_papers, Author
from django.core.mail import send_mail
import smtplib
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import * 
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import *
from django.shortcuts import get_object_or_404
from conference.models import *
# Create your views here.


def index(request):
    return render(request,'reviewer/index.html')
    # return HttpResponse("Hello, Reviewer.")

def sing_up_reviewer(request):
    if request.method == "POST":
        full_name=request.POST.get('full-name')
        highest_qualification=request.POST.get('highest-qualification')
        experience=request.POST.get('experience')
        designations=request.POST.get('designations')
        organization=request.POST.get('organization')
        mobile_number=request.POST.get('mobile-number')
        whats_app_number=request.POST.get('whats-app-number')
        email_reviewer=request.POST.get('email_reviewer')
        password_reviewer=request.POST.get('password_reviewer')
        photo_upload = request.FILES.get('photo-upload')
        resume_upload = request.FILES.get('resume-upload')
        print(full_name)
        if Reviewer_data.objects.filter(email=email_reviewer).exists():
                context = {'error_message': 'This email is already registered.'}
                return render(request, 'reviewer/sing-up.html',context)
        if CustomUser.objects.filter(email=email_reviewer).exists():
                context = {'error_message': 'This email is already registered.'}
                return render(request, 'reviewer/sing-up.html',context)
        else:
             new_reviewer=Reviewer_data.objects.create(
                  reviewer_name=full_name,highest_qualification=highest_qualification,experience=experience,designations=designations,organization=organization,reviewer_number=mobile_number,email=email_reviewer,whats_app_number=whats_app_number,password=password_reviewer,photo_upload=photo_upload,resume_upload=resume_upload,
             )
             new_reviewer.save()
             reviewer=CustomUser.objects.create_user(
                  name=full_name,email=email_reviewer,number=mobile_number,password=password_reviewer
             )
             reviewer.is_active = False
             reviewer.is_reviewer = True
             reviewer.save()
             subject2= "Email Verification SDBC Conference"
             from_email =settings.EMAIL_HOST_USER
             to_list = [reviewer.email]
             current_site = get_current_site(request)
             uidb64 = urlsafe_base64_encode(force_bytes(reviewer.id))
             token = default_token_generator.make_token(reviewer)
             context1 = {
                'name': reviewer.name,
                'domain': current_site.domain,
                'uidb64': uidb64,
                'token': token,
                }
             messages2 = render_to_string('reviewer/email_confirmation.html', context1)
             try:
                send_mail(subject2, messages2, from_email, to_list, fail_silently=True)
                context = {'success_message': 'Your Account Create Successfully. Please Check Your Email and Verify It  :-) '}
                return render(request, 'reviewer/sing-up.html', context)
             except smtplib.SMTPException as e:
                print("SMTPException occurred:",e)
                context = {'error_message': 'Your Account Create Successfully. There is a problem to sending mail But You Can login  :-) '}
                return render(request, 'reviewer/sing-up.html', context)
    return render(request,'reviewer/sing-up.html')

def activate_reviewer(request, uidb64, token):
    try:
        uidb64 = force_str(urlsafe_base64_decode(uidb64))
        my_user = CustomUser.objects.get(id=uidb64)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        my_user = None
    if my_user is not None and default_token_generator.check_token(my_user,token):
        my_user.is_active = True
        my_user.save()
        login(request,my_user)
        return redirect('reviewer-dashboard')
    else:
   
        return render(request,'reviewer/activation-failed.html')

def sing_in_reviewer(request):
    if request.user.is_authenticated:
        pass
         #return redirect('reviewer-dashboard')
    if request.method == 'POST':
         if request.POST.get('user_role') == 'reviseur':
            email=request.POST.get('email')
            password=request.POST.get('password')
            print(email)
            print(password)
            user=authenticate(request,email=email,password=password)
            print(user)
            if user is not None:
                #   login(request, user)
                #   print(request.user.is_authenticated)
                #   print(user.reviewer_name)
                #   return redirect('reviewer-dashboard')
                login(request,user)
                return redirect('reviewer-dashboard')
            else:
                context={
                    'error_message': 'Invalid Email or Password.'
                }
                return render(request,'reviewer/sing-in.html',context)
         elif request.POST.get('user_role') == 'auteur':
            get_email=request.POST['email']
            get_password=request.POST["password"]
            # hashed_password = make_password(get_password)
            print("Email is",get_email)
            print("Password is ",get_password)
            # print("Hashed Password is --- ",hashed_password)
            user = authenticate(request,email=get_email,password=get_password)
            print("User singIn is----",user)
            if user is not None:
                login(request,user)
                return redirect('success')
            else:
                context = {'error_message': 'Invalid email or password'}
                return render(request, 'reviewer/sing-in.html', context)

    return render(request,'reviewer/sing-in.html')



def dashboard_reviewer(request):
    print(request.user.is_authenticated)
    if request.user.is_authenticated: 
        user=request.user
        fname=user.name
        if user.is_reviewer:
            try:
                reviewer=Reviewer_data.objects.get(email=user)
            except Exception as e:
                print(e)
                logout(request)
                return redirect('reviewer-sing-in')
            add_id_ok=user.id
            reviewer.reviewer_id=add_id_ok
            reviewer.save()
            if reviewer.is_ok:
                reviewer_instance = get_object_or_404(Reviewer_data, email=user.email)
                papers = paper.objects.filter(assigned_reviewers=reviewer_instance)
                fname=reviewer.reviewer_name
                reviewer=reviewer
                content ={
                'reviewer':reviewer,
                'papers':papers,
                }
                return render(request,'reviewer/dashboard.html',content)
            else:
                content ={
                    "user":user,
                    "fname":fname,
                    "message_error":"You Are Not Verify By Admin Wait or Contact With Admin"
                }
                return render(request,'reviewer/dashboard.html',content)
        else:
            print("User is ",fname,"Not Reviewer")
            logout(request)
            return redirect('reviewer-sing-in')
    else :
        return redirect('reviewer-sing-in')
    
def sing_out_reviewer(request):
    logout(request)
    return redirect('reviewer-sing-in')

def list_of_submitted_papers(request):
    if request.user.is_authenticated: 
        user=request.user
        fname=user.name
        if user.is_reviewer:
            add_id=Reviewer_data.objects.get(email=user)
            add_id_ok=user.id
            add_id.reviewer_id=add_id_ok
            add_id.save()
            if add_id.is_ok:
                reviewer_instance = get_object_or_404(Reviewer_data, email=user.email)
                papers = paper.objects.filter(assigned_reviewers=reviewer_instance)
                fname=add_id.reviewer_name
                content ={
                "add_id":add_id,
                "papers" : papers,
                }
                return render(request,'reviewer/submitted_paper.html',content)
            else:
                content ={
                    "user":user,
                    "fname":fname,
                    "message_error":"You Are Not Verify By Admin Wait or Contact With Admin"
                }
                return render(request,'reviewer/dashboard.html',content)
        else:
            print("User is ",fname,"Not Reviewer")
            logout(request)
            return redirect('reviewer-sing-in')
    else :
        return redirect('reviewer-sing-in')
    
def list_of_resubmitted_papers(request):
    if request.user.is_authenticated: 
        user=request.user
        fname=user.name
        if user.is_reviewer:
            add_id=Reviewer_data.objects.get(email=user)
            add_id_ok=user.id
            add_id.reviewer_id=add_id_ok
            add_id.save()
            if add_id.is_ok:
                reviewer_instance = get_object_or_404(Reviewer_data, email=user.email)
                papers = resubmit_papers.objects.filter(assigned_reviewers=reviewer_instance)
                fname=add_id.reviewer_name
                content ={
                "add_id":add_id,
                "papers" : papers,
                }
                return render(request,'reviewer/resubmitted_paper.html',content)
            else:
                content ={
                    "user":user,
                    "fname":fname,
                    "message_error":"You Are Not Verify By Admin Wait or Contact With Admin"
                }
                return render(request,'reviewer/dashboard.html',content)
        else:
            print("User is ",fname,"Not Reviewer")
            logout(request)
            return redirect('reviewer-sing-in')
    else :
        return redirect('reviewer-sing-in')
    
def paper_reviewer(request, paper_id):
    if request.user.is_authenticated and request.user.is_reviewer:
        try:
            paper_instance = paper.objects.get(id=paper_id)
        except paper.DoesNotExist:
            return HttpResponse("Unknown Paper Id") # Handle the case when paper doesn't exist

        if request.method == 'POST':
            comment = request.POST.get('comment')
            print("Review Submitted Comment : ",comment)
            paper_instance.reviewer_comments[request.user.id] = comment
            paper_instance.save()

        context = {
            "paper": paper_instance,
        }
        return render(request, 'reviewer/review_paper.html', context)

    else:
        return redirect('reviewer-sign-in')

def paper_reviewer_resubmit(request, paper_id):
    if request.user.is_authenticated and request.user.is_reviewer:
        try:
            paper_instance = resubmit_papers.objects.get(id=paper_id)
        except paper.DoesNotExist:
            return HttpResponse("Unknown Paper Id") # Handle the case when paper doesn't exist

        if request.method == 'POST':
            comment = request.POST.get('comment')
            print("Review ReSubmitted Comment : ",comment)
            paper_instance.reviewer_comments[request.user.id] = comment
            paper_instance.save()

        context = {
            "paper": paper_instance,
        }
        return render(request, 'reviewer/review_resubmit_paper.html', context)

    else:
        return redirect('reviewer-sign-in')

def reviewer_profile(request, reviewer_id):
    if request.user.is_authenticated and request.user.is_reviewer:
        reviewer_instance=Reviewer_data.objects.get(id=reviewer_id)   
        context={
            "reviewer" : reviewer_instance,
        }    
        return render(request,'reviewer/reviewer_profile.html',context)
    else:
        return redirect('reviewer-sign-in')

def singup_view(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        number = request.POST.get('number')
        password = request.POST.get('password')
        if CustomUser.objects.filter(email=email).exists():
                context = {'error_message': 'This email is already registered.'}
                return render(request, 'reviewer/singup.html',context)        
        else:
            my_user = CustomUser.objects.create_user(
                    name=name,
                    email=email,
                    number=number,
                    password=password,
                )
            my_user.is_active = False
            my_user.is_auth = True
            my_user.save()
            # welcome Email Function
            # subject = "WELCOME TO SDBC CONFERENCE"
            subject2= "Email Verification SDBC Conference"
            # messages = "Hello "+my_user.name+"  !!\n"+"Welcome to SDBC Conference \n"+"Your Account is under the Verification Process .\n"+"You Get A Another Mail & It Content the verification link. You Have to Click it. Then Your Account will Activated :-)  "
            from_email =settings.EMAIL_HOST_USER
            to_list = [my_user.email]
            # send_mail(subject, messages, from_email, to_list, fail_silently=True)
            # Confirmation Email
            current_site = get_current_site(request)
            uidb64 = urlsafe_base64_encode(force_bytes(my_user.id))
            token = default_token_generator.make_token(my_user)
            context1 = {
                'name': my_user.name,
                'domain': current_site.domain,
                'uidb64': uidb64,
                'token': token,
                }
            messages2 = render_to_string('singup/email_confirmation.html', context1)
            try:
                send_mail(subject2, messages2, from_email, to_list, fail_silently=True)
                context_success = {'success_message': 'Your Account Create Successfully. Please Check Your Email and Verify It  :-) '}
                return render(request, 'reviewer/sing-in.html', context_success)
            except smtplib.SMTPException as e:
                print("SMTPException occurred:",e)
                context_success = {'error_message': 'Your Account Create Successfully. There is a problem to sending mail But You Can login  :-) '}
                return render(request, 'singup/sing-in.html', context_success)
    else:
        return render(request, 'singup/singup.html')
def singIn(request):
    if request.user.is_authenticated and request.user.is_auth:
        return redirect('success')
    if request.method=="POST":
        get_email=request.POST['email']
        get_password=request.POST["password"]
        # hashed_password = make_password(get_password)
        print("Email is",get_email)
        print("Password is ",get_password)
        # print("Hashed Password is --- ",hashed_password)
        user = authenticate(request,email=get_email,password=get_password)
        print("User singIn is----",user)
        if user is not None:
            login(request,user)
            return redirect('success')
        else:
            context = {'error_message': 'Invalid email or password'}
            return render(request, 'reviewer/sing-in.html', context)
    else:
        return render(request, 'reviewer/sing-in.html')
def logout_page(request):
    logout(request)
    return redirect('/')
def success_view(request):
    print(request.user.is_authenticated)
    if request.user.is_authenticated and request.user.is_auth:
        user=request.user
        print("User is ",user.name)
        context={
            'conference':conference.objects.all(),
            'uname' : user.name,
        }
        return render(request, 'singup/dashboard.html',context)
    else:
        return redirect('reviewer-sing-in') 
def activate(request, uidb64, token):
    try:
        uidb64 = force_str(urlsafe_base64_decode(uidb64))
        my_user = CustomUser.objects.get(id=uidb64)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        my_user = None
    if my_user is not None and default_token_generator.check_token(my_user,token):
        my_user.is_active = True
        my_user.save()
        login(request,my_user)
        return redirect('success')
    else:
   
        return render(request,'singup/activation-failed.html')

def re_resubmit(request,re_paper_id):
    if request.user.is_authenticated and request.user.is_auth:
        user = request.user
        original_paper = get_object_or_404(resubmit_papers, id=re_paper_id)
        if request.method=="POST":
            paper_title=request.POST.get('title_paper')
            Auth_name=request.POST.get('Auth_name')
            paper_keyword=request.POST.get('paper_keyword')
            paper_description=request.POST.get('paper_description')
            pdf_upload = request.FILES.get('pdf_upload')
            print(original_paper)
            re_resubmit_paper=resubmit_papers(
                paper_id=original_paper.paper_id,
                user=original_paper.user,
                status='pending',
                paper_keyword=paper_keyword,
                conference=original_paper.conference,
                title_paper=paper_title,
                Auth_name=Auth_name,
                paper_description=paper_description,
                paper_upload=pdf_upload,
                Auth_affiliation=original_paper.Auth_affiliation,
                Auth_email=original_paper.Auth_email,
                Auth_mobile=original_paper.Auth_mobile,
                corresponding_auth_name=original_paper.corresponding_auth_name,
                corresponding_auth_email=original_paper.corresponding_auth_email,
                corresponding_auth_mobile=original_paper.corresponding_auth_mobile,
                corresponding_auth_affiliation=original_paper.corresponding_auth_affiliation,
                other_auth_mobile=original_paper.other_auth_mobile,
                other_auth_email=original_paper.other_auth_email,
                other_auth_name=original_paper.other_auth_name,
                other_auth_affiliation=original_paper.other_auth_affiliation,
                version=original_paper.version + 1

            )
            re_resubmit_paper.save()
            context = {
                'error_message': 'Successfully Upload Your Paper',
                "original_paper":get_object_or_404(resubmit_papers, id=re_paper_id),
                "fname":user.name,
                }
            return render(request, 'singup/resubmit.html',context)
            
        context={
            "original_paper":get_object_or_404(resubmit_papers, id=re_paper_id),
            "user":request.user,
            "fname":user.name,
        }
        return render(request,'singup/re_resubmit.html',context)

def resubmit(request,paper_id):
    if request.user.is_authenticated and request.user.is_auth:
        user = request.user
        original_paper = get_object_or_404(paper, id=paper_id)
        if request.method=="POST":
            original_paper.title_paper=request.POST.get('title_paper')
            original_paper.track_preference = get_object_or_404(ConferenceTrack, track_name=request.POST.get('track_preference'))
            original_paper. main_topic = get_object_or_404(ConferenceTopic, topic_name=request.POST.get('main_topic'))
            original_paper.contribution_type = request.POST.get('contribution_type')
            original_paper.content_type = request.POST.get('content_type')
            original_paper.abstract = request.POST.get('abstract')
            authors_data = []

        # Itérer sur les champs des auteurs jusqu'à ce qu'il n'y en ait plus
            i = 0
            while f'authors[{i}][0]' in request.POST:
                email = request.POST.get(f'authors[{i}][0]')
                name = request.POST.get(f'authors[{i}][1]')
                first_name = request.POST.get(f'authors[{i}][2]')
                institution = request.POST.get(f'authors[{i}][3]')
                country = request.POST.get(f'authors[{i}][4]')

                authors_data.append((email, name, first_name, institution, country))
                i += 1
            if 'pdf_upload' in request.FILES:
            # Si un nouveau fichier est téléchargé, le sauvegarder dans le modèle
                original_paper.pdf_upload = request.FILES['pdf_upload']

            for author_data in authors_data:
                email, name, first_name, institution, country = author_data

            # Vérifier si l'auteur existe déjà
                author, created = Author.objects.get_or_create(
                    email=email,
                    defaults={
                        'first_name': name,
                        'last_name': first_name,
                        'institution': institution,
                        'country': country,
                    }
                )
                if author not in original_paper.authors.all():
                    original_paper.authors.add(author)

            
            original_paper.save()
            context = {
                'error_message': 'Contribution Modifiée avec Succès',
                "original_paper":get_object_or_404(paper, id=paper_id),
                "fname":user.name,
                'tracks' : get_object_or_404(conference, id=int(original_paper.conference.id)).tracks.all(),
                'topics' : get_object_or_404(conference, id=int(original_paper.conference.id)).topics.all(),
                'all_authors': original_paper.authors.all()
                }
            return render(request, 'singup/resubmit.html',context)
        
        context={
            "original_paper":get_object_or_404(paper, id=paper_id),
            "user":request.user,
            "fname":user.name,
            'tracks' : get_object_or_404(conference, id=int(original_paper.conference.id)).tracks.all(),
            'topics' : get_object_or_404(conference, id=int(original_paper.conference.id)).topics.all(),
            'all_authors': original_paper.authors.all()
        }
        return render(request,'singup/resubmit.html',context)

def submit_paper(request,conf_id):
    if request.user.is_authenticated and request.user.is_auth:
        user = request.user
        conf_instance = get_object_or_404(conference, id=conf_id)
        if request.method=="POST":
            user=request.user
            title_paper=request.POST.get('title_paper')
            track_preference = get_object_or_404(ConferenceTrack, track_name=request.POST.get('track_preference'))
            main_topic = get_object_or_404(ConferenceTopic, topic_name=request.POST.get('main_topic'))
            contribution_type = request.POST.get('contribution_type')
            content_type = request.POST.get('content_type')
            abstract = request.POST.get('abstract')
            authors_data = []

        # Itérer sur les champs des auteurs jusqu'à ce qu'il n'y en ait plus
            i = 0
            while f'authors[{i}][0]' in request.POST:
                email = request.POST.get(f'authors[{i}][0]')
                name = request.POST.get(f'authors[{i}][1]')
                first_name = request.POST.get(f'authors[{i}][2]')
                institution = request.POST.get(f'authors[{i}][3]')
                country = request.POST.get(f'authors[{i}][4]')

                authors_data.append((email, name, first_name, institution, country))
                i += 1

            pdf_upload = request.FILES.get('pdf_upload')
            if authors_data != []:
            
                new_paper=paper.objects.create(
                    user=user,
                    title_paper=title_paper,
                    track_preference=track_preference,
                    main_topic=main_topic,
                    contribution_type=contribution_type,
                    content_type=content_type,
                    abstract=abstract,
                    paper_upload=pdf_upload,
                    status='pending',
                    conference=conf_instance,
                )
            
            for author_data in authors_data:
                email, name, first_name, institution, country = author_data

            # Vérifier si l'auteur existe déjà
                author, created = Author.objects.get_or_create(
                    email=email,
                    defaults={
                        'first_name': name,
                        'last_name': first_name,
                        'institution': institution,
                        'country': country,
                    }
                )
                new_paper.authors.add(author)

            # Ajouter l'auteur à la liste des auteurs de l'article
            
            conf_instance.has_uploaded_paper = True
            new_paper.save()
            send_mail(
            'Confirmation de Soumission',
            'Votre contribution a été soumise avec succès à la conférence et sera bientôt examinée.',
            settings.EMAIL_HOST_USER,
            [new_paper.authors.all()[0].email],  # Remplacez par le véritable champ email du principal auteur
            fail_silently=False,
        )
            context = {
                'error_message': 'Contribution soumise avec Succès',
                'v1':conf_instance.id,
                }
            return render(request, 'singup/first_upload.html',context)
        else:
            context ={
                'v1':conf_instance.id,
                'uname' : user.name,
                'conference' : get_object_or_404(conference, id=conf_id),
                'tracks' : get_object_or_404(conference, id=conf_id).tracks.all(),
                'topics' : get_object_or_404(conference, id=conf_id).topics.all(),
            }
            return render(request, 'singup/first_upload.html',context)
    else:
        return redirect('reviewer-sing-in')


def list_of_paper(request,conf_id):
    if request.user.is_authenticated and request.user.is_auth:
        user = request.user
        context={
            'papers_uploaded':paper.objects.filter(user=user,conference_id=conf_id),
            'reupload_paper':resubmit_papers.objects.filter(user=user,conference_id=conf_id),
        }
        return render(request, 'singup/list_of_paper.html',context)
    else:
        return render(request, 'reviewer/sing-in.html')



def list_of_conference(request):
    # conference = conference.objects.all()
    if request.user.is_authenticated and request.user.is_auth:
        conference = conference.objects.all()
        user = request.user
        print("He Check The Conference List",user.name)
        return render(request,"singup/list_of_conference.html",{'conference':conference})
    else:
        return render(request, 'reviewer/sing-in.html')



def conference_detail(request, conf_id):
    if request.user.is_authenticated and request.user.is_auth:
        conf_instance = get_object_or_404(conference, id=conf_id)
        user=request.user
        print(conf_instance.has_uploaded_paper)
        context={
            'conf_instance': conf_instance,
            'papers_uploaded' : paper.objects.filter(user=user, conference=conf_instance),
        }
        return render(request, 'singup/conference_detail.html', context)
    else:
        return render(request, 'reviewer/sing-in.html')

