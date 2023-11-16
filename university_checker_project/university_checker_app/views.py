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
from .sentiment_analysis.university_tweet_clearning import clean_twitter_text, generate_word_cloud
import base64
import os
from collections import Counter
from django.db.models import Q

IMAGE_DIR = os.path.join('static', 'images/wordcloud_images')


# the following class will display list of universities

class UniversityListView(ListView):
    model = University 
    context_object_name = 'university_list' 
    template_name = 'project/new_project.html'


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
                return redirect('university_checker:overview', university=selected_university_name)

        else:
            custom_errors.append("Please select a university.")

    universities = University.objects.all()
    return render(request, 'project/new_project.html', {
        'university_list': universities,
        'success_message': success_message,
        'custom_errors': custom_errors,
    })
# project details code
def overview_view(request, university):
    if not request.user.is_authenticated:
        return redirect('index')
    else:
        if university is not None:
            university_obj = get_object_or_404(University, name=university)
            tweets = Tweets.objects.filter(user=request.user).values('tweet_text', 'created_at')

            if tweets:
                positive_text = ""
                negative_text = ""
                neutral_text = ""
                wordcloud_positive=""
                wordcloud_negative=""

                # Extract month from created_at and count occurrences
                positive_dates_counter = Counter()
                negative_dates_counter = Counter()
                custom_month_order = [
                    'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
                ]

                for tweet in tweets:
                    tweet_text = tweet['tweet_text']
                    created_at = tweet.get('created_at', None)

                    if not tweet_text:
                        continue

                    cleaned_text, sentiment = clean_twitter_text(tweet_text)

                    if sentiment.get("sentiment", "") == "Positive":
                        wordcloud_positive += cleaned_text + " "
                        positive_text +=cleaned_text + ";"

                    elif sentiment.get("sentiment", "") == "Negative":
                        wordcloud_negative += cleaned_text + " "
                        negative_text +=cleaned_text + ";"

                    elif sentiment.get("sentiment", "") == "Neutral":
                        neutral_text += cleaned_text + ";"
                    
                    # Count positive and negative sentiment per month code
                    sentiment_value = sentiment.get("sentiment", "")
                    created_at = tweet.get('created_at', None)

                    if sentiment_value == "Positive":
                        positive_dates_counter[created_at.strftime('%b')] += 1
                    elif sentiment_value == "Negative":
                        negative_dates_counter[created_at.strftime('%b')] += 1

                   # Extract unique months and their counts for positive sentiment
                   # Sort the items based on the index of the month in custom_month_order
                    if positive_dates_counter:
                        sorted_positive_dates = sorted(positive_dates_counter.items(), key=lambda x: custom_month_order.index(x[0]))
                        unique_months_positive, positive_counts = zip(*sorted_positive_dates)
                    else:
                        unique_months_positive, positive_counts = [], []

                    # Similar modification for negative_dates_counter
                    if negative_dates_counter:
                        sorted_negative_dates = sorted(negative_dates_counter.items(), key=lambda x: custom_month_order.index(x[0]))
                        unique_months_negative, negative_counts = zip(*sorted_negative_dates)
                    else:
                        unique_months_negative, negative_counts = [], []

                    # End count positive and negative sentiment per month code
                   
                    # Add data to filteredTweet table in database
                        # Check if the entry already exists in FilteredTweets table
                    existing_entry = FilteredTweets.objects.filter(
                        Q(user=request.user) &
                        Q(university_name=university_obj) &
                        Q(filtered_tweet=cleaned_text)
                    ).exists()

                    if not existing_entry:
                        # Create and save the filtered tweet
                        filtered_tweet = FilteredTweets(
                            user=request.user,
                            university_name=university_obj,
                            filtered_tweet=cleaned_text,
                            sentiment_score=sentiment.get('sentiment', None),
                            created_at=created_at
                        )
                        filtered_tweet.save()
                    # End dd data to filteredTweet table in database

                # Generate the WordCloud images
                if wordcloud_positive:
                    positive_wordcloud = generate_word_cloud(wordcloud_positive, "Positive Sentiment Word Cloud")
                    positive_wordcloud_path = os.path.join(IMAGE_DIR, f'{university}_positive_wordcloud.png')
                    with open(positive_wordcloud_path, 'wb') as f:
                        f.write(base64.b64decode(positive_wordcloud))

                if wordcloud_negative:
                    negative_wordcloud = generate_word_cloud(wordcloud_negative, "Negative Sentiment Word Cloud")
                    negative_wordcloud_path = os.path.join(IMAGE_DIR, f'{university}_negative_wordcloud.png')
                    with open(negative_wordcloud_path, 'wb') as f:
                        f.write(base64.b64decode(negative_wordcloud))
                 # Calculate sentiment counts
                # End generate the WordCloud images
                positive_count = len(positive_text.split(';'))
                negative_count = len(negative_text.split(';'))
                neutral_count = len(neutral_text.split(';')) 

                # Calculate sentiment counts
                total_count = len(positive_text.split(";")) + len(negative_text.split(';')) + len(neutral_text.split(';'))

                if total_count > 0:
                    positive_percentage = (positive_count / total_count) * 100
                    negative_percentage = (negative_count/ total_count) * 100
                    neutral_percentage = (neutral_count/ total_count) * 100
                else:
                    positive_percentage = negative_percentage = neutral_percentage = 0
                
                 # Check if the entry already exists in ranking table
                existing_entry1 = ranking.objects.filter(
                    Q(user=request.user) &
                    Q(name=university_obj) &
                    Q(positive=positive_count) &
                    Q(negative=negative_count)

                ).exists()

                if not existing_entry1:
                    # Create and save the project 
                    sentiment_project = ranking(
                        user=request.user,
                        name=university_obj,
                        positive=positive_count,
                        negative=negative_count,
                        created_at=created_at
                    )
                    sentiment_project.save()
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


def comparison_view(request, university):
    if not request.user.is_authenticated:
         return redirect('index')
    else:
        
        return render(request, 'project/comparison.html', {
            'university_name': university,
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
