from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic  import View, TemplateView, ListView, DetailView
from .models import University, Tweets, FilteredTweets, ranking
from .forms import RegistrationForm, CustomPasswordResetForm, UploadFileForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView
import pandas as pd
from .sentiment_analysis.university_tweet_fetching import project_sentiment_analysis
import os
import matplotlib.pyplot as plt
from .processes.process import html_to_pdf 
from .processes.comparison_process import compare_tweets, get_comparison_data
from .processes.overview_process import process_tweets, generate_wordcloud_images, calculate_sentiment_counts, save_ranking_project

IMAGE_DIR = os.path.join('static', 'images/wordcloud_images')   

# delete project code

def delete_project(request, project_id):
    project = get_object_or_404(ranking, id=project_id)

    # Check if the user has the permission to delete the project
    if request.user == project.user:
        # Store the project details before deleting
        university_id = project.name.university_id

        # Delete related data in FilteredTweets and Tweets tables using both university_name and user
        FilteredTweets.objects.filter(university_name=university_id, user=request.user).delete()
        Tweets.objects.filter(university_name=university_id, user=request.user).delete()

        # Delete the project in the ranking table using both id and user
        ranking.objects.filter(id=project_id, user=request.user).delete()

        # Add success message
        messages.success(request, f'Project {project.name.name} deleted successfully.')
        return JsonResponse({'success': True, 'message': 'Project deleted successfully.'})
    else:
        # Add error message
        messages.error(request, 'Something went wrong. Try again later.')
        return JsonResponse({'success': False, 'message': 'Something went wrong. Try again later.'})
   
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

# reset password view
class CustomPasswordResetView(PasswordResetView):
    template_name = 'credentials/password_reset.html'  
    form_class = CustomPasswordResetForm

# user registration code
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
#login code
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
#logout code
@login_required
def user_logout(request):
    logout(request)
    return  HttpResponseRedirect(reverse('index'))
#forget passowrd code
def forgot_password_view(request):
    return render(request, 'forgot_password.html')
#dashboard code
def dashboard_view(request):
    if not request.user.is_authenticated: #check if the user is not logged in then he will be redirected to login page
         return redirect('index')
    else:
        projects = ranking.objects.filter(user=request.user)
        return render(request, 'index/dashboard.html', {'projects': projects})
#create project code
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
                # Use the project_sentiment_analysis class to perform sentiment analysis
                results = project_sentiment_analysis(selected_university_name)

                # Save the sentiment results and comments to the database
                university = University.objects.get(name=selected_university_name)

                for sentiment in results:
                    comment_text = sentiment['comment']
                    comment_date = sentiment['comment_date']
                    sentiment_score = sentiment['sentiment']

                    # Create and save the tweet
                    tweet = Tweets(
                        user=request.user,
                        university_name=university,
                        tweet_text=comment_text,
                        sentiment_score=sentiment_score,
                        created_at=comment_date
                    )
                    tweet.save()

                success_message = 'Sentiment analysis completed successfully.'
                return redirect('university_checker:overview', university=selected_university_name)

        else:
            custom_errors.append("Please select a university.")

    universities = University.objects.all()
    return render(request, 'project/new_project.html', {
        'university_list': universities,
        'success_message': success_message,
        'custom_errors': custom_errors,
    })

#this will generate pdf for overview
class Overview_generatePdf(View):
    def get(self, request, *args, **kwargs):
        pdf_displayed = True 
        # You need to fetch the data needed for your PDF
        university = self.kwargs['university']
        if university is not None:
            university_obj = get_object_or_404(University, name=university)
            tweets = Tweets.objects.filter(user=request.user).values('tweet_text', 'created_at')

            if tweets:
                positive_text, negative_text, neutral_text, unique_months_positive, unique_months_negative, positive_counts, negative_counts, wordcloud_positive, wordcloud_negative = process_tweets(tweets, request.user, university_obj)
                
                positive_count, negative_count, neutral_count, positive_percentage, negative_percentage, neutral_percentage = calculate_sentiment_counts(positive_text, negative_text, neutral_text)
         
        context_data = self.get_context_data(university, positive_count, negative_count, neutral_count, 
                         positive_percentage, negative_percentage, neutral_percentage, pdf_displayed)

        # getting the template and rendering the template with context data
        pdf = html_to_pdf('project/overview.html', context_data)
        # returning the response
        return HttpResponse(pdf, content_type='application/pdf')
    def get_context_data(self, university, positive_count, negative_count, neutral_count, 
                         positive_percentage, negative_percentage, neutral_percentage, pdf_displayed ):
        return {
            'university_name': university,
            'positive_count': positive_count,
            'negative_count': negative_count,
            'neutral_count': neutral_count,
            'positive_percentage': positive_percentage,
            'negative_percentage': negative_percentage,
            'neutral_percentage': neutral_percentage,
            'pdf_displayed': pdf_displayed,
        }    

# project details 
def overview_view(request, university):
    if not request.user.is_authenticated:
        return redirect('index')
    else:
        if university is not None:
            university_obj = get_object_or_404(University, name=university)
            tweets = Tweets.objects.filter(user=request.user).values('tweet_text', 'created_at')

            if tweets:
                positive_text, negative_text, neutral_text, unique_months_positive, unique_months_negative, positive_counts, negative_counts, wordcloud_positive, wordcloud_negative = process_tweets(tweets, request.user, university_obj)
                positive_wordcloud_path, negative_wordcloud_path = generate_wordcloud_images(wordcloud_positive, wordcloud_negative, university)
                # Call the function to calculate sentiment counts
                positive_count, negative_count, neutral_count, positive_percentage, negative_percentage, neutral_percentage = calculate_sentiment_counts(positive_text, negative_text, neutral_text)
                # Check if the entry already exists in ranking table
                save_ranking_project(request.user, university_obj, positive_count, negative_count)
                 # university_link = extract_university_name(request)
                return render(request, 'project/overview.html', {
                    'university_name': university,
                    'positive_count': positive_count,
                    'negative_count': negative_count,
                    'neutral_count': neutral_count,
                    'positive_percentage': positive_percentage,
                    'negative_percentage': negative_percentage,
                    'neutral_percentage': neutral_percentage,
                    'unique_months_positive': unique_months_positive,
                    'unique_months_negative': unique_months_negative,
                    'positive_counts': positive_counts,
                    'negative_counts': negative_counts,
                    'positive_wordcloud_path': positive_wordcloud_path if wordcloud_positive else None,
                    'negative_wordcloud_path': negative_wordcloud_path if wordcloud_negative else None,
                })
            else:
                return render(request, 'project/overview.html', {
                    'error_message': f'No data found for {university}.',
                })
        else:
            university_obj = get_object_or_404(University, name=university)

# end project details

#this will generate pdf for comparison
class Comparison_generatePdf(View):
    def get(self, request, *args, **kwargs):
        url_positive = 0
        url_negative = 0
        select_positive = 0
        select_negative = 0
        url_positive_percentage = 0  # Default value
        url_negative_percentage = 0  # Default value
        select_positive_percentage = 0  # Default value
        select_negative_percentage = 0  # Default value
        pdf_displayed = True 
        # You need to fetch the data needed for your PDF
        university = self.kwargs['university']
        select_university = self.kwargs['selected_university']
        if university is not None and select_university is not None:
           # Call the function to get comparison data
            comparison_data = get_comparison_data(request.user, university, select_university)
             # Access the data as needed
            
            url_positive=comparison_data['url_positive']
            url_negative = comparison_data['url_negative']
            select_positive= comparison_data['select_positive']
            select_negative = comparison_data['select_negative']
            url_positive_percentage = comparison_data['url_positive_percentage']
            url_negative_percentage = comparison_data['url_negative_percentage']
            select_positive_percentage = comparison_data['select_positive_percentage']
            select_negative_percentage = comparison_data['select_negative_percentage']

        context_data = self.get_context_data(university, select_university, url_positive, url_negative, 
                         select_positive, select_negative, url_positive_percentage,url_negative_percentage,
                          select_positive_percentage, select_negative_percentage, pdf_displayed)

        # getting the template and rendering the template with context data
        pdf = html_to_pdf('project/comparison.html', context_data)
        # returning the response
        return HttpResponse(pdf, content_type='application/pdf')
    def get_context_data(self, university, select_university, url_positive, url_negative, 
                         select_positive, select_negative, url_positive_percentage,url_negative_percentage,
                          select_positive_percentage, select_negative_percentage, pdf_displayed):
        return {
            'university_name': university,
            'select_university': select_university,
            'url_positive': url_positive,
            'url_negative': url_negative,
            'select_positive': select_positive,
            'select_negative': select_negative,
            'url_positive_percentage': url_positive_percentage,
            'url_negative_percentage': url_negative_percentage,
            'select_positive_percentage': select_positive_percentage,
            'select_negative_percentage': select_negative_percentage,
            'pdf_displayed': pdf_displayed,
        } 
    # this will compare 2 universities
def comparison_view(request, university):
    if not request.user.is_authenticated:
        return redirect('index')

    success_message = None
    custom_errors = []
    selected_university_name = ''

    # Initialize other variables with default values
    url_positive = 0
    url_negative = 0
    select_positive = 0
    select_negative = 0
    positive_counts = []
    positive_counts1 = []
    unique_months_positive = []
    unique_months_positive1 = []
    unique_months_negative = []
    unique_months_negative1 = []
    url_positive_percentage = 0  # Default value
    url_negative_percentage = 0  # Default value
    select_positive_percentage = 0  # Default value
    select_negative_percentage = 0  # Default value

    if request.method == 'POST':
        selected_university_name = request.POST.get('university')
        if selected_university_name:
            # Check if the university has already been selected by the logged-in user
            if selected_university_name == university:
                custom_errors.append("University has already been selected by you. Select another project")
            else:
                # Call the function to get comparison data
                comparison_data = get_comparison_data(request.user, university, selected_university_name)

                # Access the data as needed
                positive_counts = comparison_data['positive_counts']
                positive_counts1 = comparison_data['positive_counts1']
                
                url_positive=comparison_data['url_positive']
                url_negative = comparison_data['url_negative']
                select_positive= comparison_data['select_positive']
                select_negative = comparison_data['select_negative']
                url_positive_percentage = comparison_data['url_positive_percentage']
                url_negative_percentage = comparison_data['url_negative_percentage']
                select_positive_percentage = comparison_data['select_positive_percentage']
                select_negative_percentage = comparison_data['select_negative_percentage']
                unique_months_positive = comparison_data['unique_months_positive']
                unique_months_positive1 = comparison_data['unique_months_positive1']
                unique_months_negative = comparison_data['unique_months_negative']
                unique_months_negative1 = comparison_data['unique_months_negative1']

                success_message = 'University Selected.'

        else:
            custom_errors.append("Please select a university.")

    projects = ranking.objects.filter(user=request.user)

    return render(request, 'project/comparison.html', {
        'project_list': projects,
        'selected_university_name': selected_university_name,
        'success_message': success_message,
        'url_positive': url_positive,
        'url_negative': url_negative,
        'select_positive': select_positive,
        'select_negative': select_negative,
        'url_positive_percentage': url_positive_percentage,
        'url_negative_percentage': url_negative_percentage,
        'select_positive_percentage': select_positive_percentage,
        'select_negative_percentage': select_negative_percentage,
        'positive_counts': positive_counts,
        'positive_counts1': positive_counts1,
        'unique_months_positive': unique_months_positive,
        'unique_months_positive1': unique_months_positive1,
        'custom_errors': custom_errors,
        'unique_months_negative': unique_months_negative,
        'unique_months_negative1': unique_months_negative1,
    })


def ranking_view(request, university):
    if not request.user.is_authenticated:
         return redirect('index')
    else:
        return render(request, 'project/ranking.html',  {
            'university_name': university,
        })

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
