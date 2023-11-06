from django.shortcuts import render, redirect
from django.views.generic  import View, TemplateView, ListView, DetailView
from .models import University, Tweets
from .forms import RegistrationForm, CustomPasswordResetForm, UploadFileForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView
import pandas as pd
from .sentiment_analysis.university_tweet_fetching import project_sentiment_analysis
import subprocess
import sys
import os


# the following class will display list of universities

class UniversityListView(ListView):
    model = University 
    context_object_name = 'university_list' 
    template_name = 'project/new_project.html'

# the following function will upload list of university from excel file to db
def upload_excel(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data['file']
            if file.name.endswith('.xlsx'):
                df = pd.read_excel(file, engine='openpyxl')
                for index, row in df.iterrows():
                    university = University(  # Use the model name 'University'
                        name=row['Name'],
                        location=row['Location'],
                        # Add other fields as needed
                    )
                    university.save()
                messages.success(request, 'Data uploaded successfully!')
                return redirect('index')  # Redirect to the index page
            else:
                messages.error(request, 'Please upload an Excel file.')
        else:
            messages.error(request, 'Form is not valid. Please check the uploaded file.')
    else:
        form = UploadFileForm()

    return render(request, 'upload/excel_upload.html', {'form': form})



class CustomPasswordResetView(PasswordResetView):
    template_name = 'credentials/password_reset.html'  
    form_class = CustomPasswordResetForm

def registration_view(request):
    field_to_focus = None # Initialize the field_to_focus
    success_message = None # Initialize the success_message
    if request.user.is_authenticated:
         return redirect('university_checker:dashboard')
    else:
        if request.method == "POST":
            registration_form = RegistrationForm(request.POST)
            # Check if the form is valid and not empty
            if registration_form.is_valid():
                if not (
                    registration_form.cleaned_data['username'] and
                    registration_form.cleaned_data['first_name'] and
                    registration_form.cleaned_data['email'] and
                    registration_form.cleaned_data['password'] and
                    registration_form.cleaned_data['verify_pwd']
                ):
                    error_messages = ["Some fields are empty. Please fill out all the required fields."]
                    return render(request, 'registration.html', {
                        'registration_form': registration_form,
                        'custom_errors': error_messages,
                    })
                else:
                    user = registration_form.save(commit=False)
                    user.set_password(registration_form.cleaned_data['password'])
                    user.save()
                    success_message = 'Registration successful.'
            else:
                error_messages = [message for field, message in registration_form.errors.items()]
                if 'username' in registration_form.errors:
                    field_to_focus = 'id_username'
                elif 'first_name' in registration_form.errors:
                    field_to_focus = 'id_name'
                elif 'email' in registration_form.errors:
                    field_to_focus = 'id_email'
                elif 'password' in registration_form.errors:
                    field_to_focus = 'id_password'
                else:
                    field_to_focus = 'id_confirm'
                
                return render(request, 'registration.html', {
                    'registration_form': registration_form,
                    'custom_errors': error_messages,
                    'field_to_focus': field_to_focus,
                })
                                                            
        else:
            registration_form = RegistrationForm()

        return render(request, 'registration.html', {
            'registration_form': registration_form,
            'success_message': success_message,
        })


def index(request):
    if request.user.is_authenticated:
        return redirect('university_checker:dashboard')
    else:
        field_to_focus = None
        success_message = None
        error_messages = []

        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            remember_me = request.POST.get('remember_me')  # Get the 'Remember Me' checkbox value

            if not username:
                error_messages.append('Username is required.')
                field_to_focus = 'username'  # Set the field to focus on to 'username'
            elif not password:
                error_messages.append('Password is required.')
                field_to_focus = 'password'  # Set the field to focus on to 'password'
            else:
                user = authenticate(request, username=username, password=password)
                if user:
                    if user.is_active:
                        login(request, user)

                        # Set session expiration based on the 'Remember Me' checkbox
                        if not remember_me:
                            # Session expires when the user closes the browser
                            request.session.set_expiry(0)

                        success_message = 'Login successful.'
                    else:
                        error_messages.append('Account does not exist.')
                else:
                    error_messages.append('Invalid login details supplied.')
                    field_to_focus = 'username'  # Set the field to focus on to 'username'

        return render(request, 'index.html', {
            'custom_errors': error_messages,
            'success_message': success_message,
            'field_to_focus': field_to_focus,
        })

@login_required
def user_logout(request):
    logout(request)
    return  HttpResponseRedirect(reverse('index'))


def forgot_password_view(request):
    return render(request, 'forgot_password.html')

def dashboard_view(request):
    if not request.user.is_authenticated: #check if the user is not logged in then he will be redirected to login page
         return redirect('index')
    else:
        return render(request, 'index/dashboard.html')

@login_required
def project_view(request):
    if not request.user.is_authenticated:
        return redirect('index')

    success_message = None
    custom_errors = []

    if request.method == 'POST':
        selected_university_name = request.POST.get('university')
        if selected_university_name:
            # Check if the university has already been selected by the logged-in user
            if Tweets.objects.filter(user=request.user, university_name__name=selected_university_name).exists():
                custom_errors.append("University has already been selected by you.")
            else:
                print(f"Executing sentiment analysis for university: {selected_university_name}")
                # Use the project_sentiment_analysis class to perform sentiment analysis
                results = project_sentiment_analysis(selected_university_name)

                # Save the sentiment results and comments to the database
                university = University.objects.get(name=selected_university_name)

                for sentiment in results:
                    comment_text = sentiment['comment']
                    comment_date = sentiment['comment_date']
                    sentiment_score = sentiment['sentiment']

                    # Create and save the tweet, associating it with the logged-in user
                    tweet = Tweets(
                        user=request.user,
                        university_name=university,
                        tweet_text=comment_text,
                        sentiment_score=sentiment_score,
                        created_at=comment_date
                    )
                    tweet.save()

                # Optionally, you can also save the sentiment data in a separate model if needed

                success_message = 'Sentiment analysis completed successfully.'
        else:
            custom_errors.append("Please select a university.")

    universities = University.objects.all()
    return render(request, 'project/new_project.html', {
        'university_list': universities,
        'success_message': success_message,
        'custom_errors': custom_errors,
    })


# the following will display sentiment of university
def overview_view(request):
     if not request.user.is_authenticated:
        return redirect('index')
     else:
         return render(request, 'project/overview.html')


def comparison_view(request):
    if not request.user.is_authenticated:
         return redirect('index')
    else:
        return render(request, 'project/comparison.html')

def ranking_view(request):
    if not request.user.is_authenticated:
         return redirect('index')
    else:
        return render(request, 'project/ranking.html')

def profile_view(request):
    if not request.user.is_authenticated:
         return redirect('index')
    else:
        return render(request, 'settings/profile.html')

def change_password_view(request):
    if not request.user.is_authenticated:
         return redirect('index')
    else:
        return render(request, 'settings/change_password.html')

def user_management_view(request):
    if not request.user.is_authenticated:
         return redirect('index')
    else:
        return render(request, 'settings/user_management.html')
