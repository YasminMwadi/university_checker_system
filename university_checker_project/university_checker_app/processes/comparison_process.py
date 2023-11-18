from ..sentiment_analysis.university_tweet_clearning import clean_twitter_text, generate_word_cloud
import base64
import os
from collections import Counter
from django.db.models import Q 
from ..models import FilteredTweets, ranking, Tweets

def get_comparison_data(user, university, selected_university_name):
    # Retrieve data for url_university
    tweets = Tweets.objects.filter(user=user, university_name__name=university).values('tweet_text', 'created_at')
    tweets1 = Tweets.objects.filter(user=user, university_name__name=selected_university_name).values('tweet_text', 'created_at')

    # Retrieve data for the original university
    positive_text, negative_text, unique_months_positive, unique_months_negative, positive_counts, negative_counts = compare_tweets(tweets, user, university)

    # Retrieve data for the selected university
    positive_text1, negative_text1, unique_months_positive1, unique_months_negative1, positive_counts1, negative_counts1 = compare_tweets(tweets1, user, selected_university_name)

    # Fetch all positive and negative entries for the url university
    url_university_data = ranking.objects.filter(user=user, name__name=university).first()

    # Print positive count for debugging
    print("positive count:")
    print(positive_counts)

    # Initialize variables for percentages
    url_positive_percentage = 0
    url_negative_percentage = 0
    select_positive_percentage = 0
    select_negative_percentage = 0

    if url_university_data:
        # Extract positive and negative values for the url university
        url_positive = url_university_data.positive
        url_negative = url_university_data.negative

        # Calculate percentages for the url university
        total_tweets = url_positive + url_negative
        url_positive_percentage = (url_positive / total_tweets) * 100
        url_negative_percentage = (url_negative / total_tweets) * 100

    # Similarly, repeat the above logic for the selected university
    selected_university_data = ranking.objects.filter(user=user, name__name=selected_university_name).first()

    if selected_university_data:
        # Extract positive and negative values for the selected university
        select_positive = selected_university_data.positive
        select_negative = selected_university_data.negative

        # Calculate percentages for the selected university
        total_tweets = select_positive + select_negative
        select_positive_percentage = (select_positive / total_tweets) * 100
        select_negative_percentage = (select_negative / total_tweets) * 100

    # Return the data as a dictionary
    return {
        'positive_counts': positive_counts,
        'positive_counts1': positive_counts1,
        'url_positive':url_positive,
        'url_negative': url_negative,
        'select_positive':select_positive,
        'select_negative':select_negative,
        'url_positive_percentage': url_positive_percentage,
        'url_negative_percentage': url_negative_percentage,
        'select_positive_percentage': select_positive_percentage,
        'select_negative_percentage': select_negative_percentage,
        'unique_months_positive': unique_months_positive,
        'unique_months_positive1': unique_months_positive1,
        'unique_months_negative': unique_months_negative,
        'unique_months_negative1': unique_months_negative1,
    }

# calculate positive and negative data for compared universities
def process_tweet(tweet, custom_month_order):
    tweet_text = tweet['tweet_text']
    created_at = tweet.get('created_at', None)

    if not tweet_text:
        return "", "", "", None, None, 0, 0, "", ""

    cleaned_text, sentiment = clean_twitter_text(tweet_text)

    if sentiment.get("sentiment", "") == "Positive":
        positive_text = cleaned_text + " "
        negative_text = ""
        wordcloud_positive = cleaned_text + ";"
        wordcloud_negative = ""
    elif sentiment.get("sentiment", "") == "Negative":
        positive_text = ""
        negative_text = cleaned_text + " "
        wordcloud_positive = ""
        wordcloud_negative = cleaned_text + ";"
    else:
        positive_text = ""
        negative_text = ""
        wordcloud_positive = ""
        wordcloud_negative = cleaned_text + ";"

    # Count positive and negative sentiment per month code
    sentiment_value = sentiment.get("sentiment", "")

    if sentiment_value == "Positive":
        month = created_at.strftime('%b')
        positive_count = 1
        negative_count = 0
    elif sentiment_value == "Negative":
        month = created_at.strftime('%b')
        positive_count = 0
        negative_count = 1
    else:
        month = None
        positive_count = 0
        negative_count = 0

    return positive_text, negative_text, wordcloud_positive, wordcloud_negative, month, positive_count, negative_count

def compare_tweets(tweets, request_user, university_obj):
    positive_text = ""
    negative_text = ""
    wordcloud_positive = ""
    wordcloud_negative = ""
    positive_dates_counter = Counter()
    negative_dates_counter = Counter()
    custom_month_order = [
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
    ]

    for tweet in tweets:
        (positive_t, negative_t, wordcloud_positive_t, wordcloud_negative_t, month_t, positive_count_t, negative_count_t) = process_tweet(tweet, custom_month_order)
        positive_text += positive_t
        negative_text += negative_t
        wordcloud_positive += wordcloud_positive_t
        wordcloud_negative += wordcloud_negative_t

        if month_t is not None:
            sentiment_dates_counter = positive_dates_counter if positive_count_t > 0 else negative_dates_counter
            sentiment_dates_counter[month_t] += 1

    sorted_positive_dates = sorted(positive_dates_counter.items(), key=lambda x: custom_month_order.index(x[0]))
    unique_months_positive, positive_counts = zip(*sorted_positive_dates)

    sorted_negative_dates = sorted(negative_dates_counter.items(), key=lambda x: custom_month_order.index(x[0]))
    unique_months_negative, negative_counts = zip(*sorted_negative_dates)

    return positive_text, negative_text, unique_months_positive, unique_months_negative, positive_counts, negative_counts

