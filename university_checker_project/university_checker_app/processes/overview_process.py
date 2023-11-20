from ..sentiment_analysis.university_tweet_clearning import clean_twitter_text, generate_word_cloud
import base64
import os
from django.shortcuts import render, redirect, get_object_or_404
from collections import Counter
from django.db.models import Q 
from ..models import FilteredTweets, ranking
from django.http import Http404

IMAGE_DIR = os.path.join('static', 'images/wordcloud_images')

# save Ranking

def save_ranking_project(request_user, university_obj, positive_count, negative_count):
    try:
        # Try to get the existing ranking entry
        ranking_entry = ranking.objects.get(user=request_user, name=university_obj)

        # If the entry exists, update the values
        # ranking_entry.positive = positive_count
        # ranking_entry.negative = negative_count
        # ranking_entry.save()
        print(ranking_entry)

    except ranking.DoesNotExist:
        # If the entry does not exist, create and save a new one
        sentiment_project = ranking(
            user=request_user,
            name=university_obj,
            positive=positive_count,
            negative=negative_count
        )
        sentiment_project.save()

    except Http404:
        # Handle the 404 exception (optional, can be used for logging)
        print(f"No ranking entry found for user {request_user} and university {university_obj}")


# save FilteredTweets
def save_filtered_tweet(request_user, university_obj, cleaned_text, sentiment, created_at):
    try:
        # Try to get the existing filtered tweet entry
        existing_entry = FilteredTweets.objects.get(user=request_user, university_name=university_obj)
        # print (existing_entry)
        # If the entry exists, update the values
        existing_entry.filtered_tweet = cleaned_text
        existing_entry.sentiment_score = sentiment.get('sentiment', None)
        existing_entry.created_at = created_at
        existing_entry.save()

    except FilteredTweets.DoesNotExist:
        # If the entry does not exist, create and save a new one
        filtered_tweet = FilteredTweets(
            user=request_user,
            university_name=university_obj,
            filtered_tweet=cleaned_text,
            sentiment_score=sentiment.get('sentiment', None),
            created_at=created_at
        )
        filtered_tweet.save()

    except Http404:
        # Handle the 404 exception (optional, can be used for logging)
        print(f"No FilteredTweets entry found for user {request_user} and university {university_obj}")

#sentiment analysis and chart displays code
def process_tweets(tweets, request_user, university_obj):
    positive_text = ""
    negative_text = ""
    neutral_text = ""
    wordcloud_positive = ""
    wordcloud_negative = ""

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
            positive_text += cleaned_text + ";"

        elif sentiment.get("sentiment", "") == "Negative":
            wordcloud_negative += cleaned_text + " "
            negative_text += cleaned_text + ";"

        elif sentiment.get("sentiment", "") == "Neutral":
            neutral_text += cleaned_text + ";"

        # Count positive and negative sentiment per month code
        sentiment_value = sentiment.get("sentiment", "")

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

    # Call the save_filtered_tweet function
    save_filtered_tweet(request_user, university_obj, cleaned_text, sentiment, created_at)

    return positive_text, negative_text, neutral_text, unique_months_positive, unique_months_negative, positive_counts, negative_counts, wordcloud_positive, wordcloud_negative

# generate wordcloud images for positive and negative sentiment

def generate_wordcloud_images(wordcloud_positive, wordcloud_negative, university):
    positive_wordcloud_path = None
    negative_wordcloud_path = None

    if wordcloud_positive:
        positive_wordcloud = generate_word_cloud(wordcloud_positive, f"{university} Positive Sentiment Word Cloud")
        positive_wordcloud_path = os.path.join(IMAGE_DIR, f'{university}_positive_wordcloud.png')
        with open(positive_wordcloud_path, 'wb') as f:
            f.write(base64.b64decode(positive_wordcloud))

    if wordcloud_negative:
        negative_wordcloud = generate_word_cloud(wordcloud_negative, f"{university} Negative Sentiment Word Cloud")
        negative_wordcloud_path = os.path.join(IMAGE_DIR, f'{university}_negative_wordcloud.png')
        with open(negative_wordcloud_path, 'wb') as f:
            f.write(base64.b64decode(negative_wordcloud))

    return positive_wordcloud_path, negative_wordcloud_path

 # Calculate sentiment counts
def calculate_sentiment_counts(positive_text, negative_text, neutral_text):
    positive_count = len(positive_text.split(';'))
    negative_count = len(negative_text.split(';'))
    neutral_count = len(neutral_text.split(';'))

   
    total_count = positive_count + negative_count + neutral_count

    if total_count > 0:
        positive_percentage = (positive_count / total_count) * 100
        negative_percentage = (negative_count / total_count) * 100
        neutral_percentage = (neutral_count / total_count) * 100
    else:
        positive_percentage = negative_percentage = neutral_percentage = 0

    return positive_count, negative_count, neutral_count, positive_percentage, negative_percentage, neutral_percentage
