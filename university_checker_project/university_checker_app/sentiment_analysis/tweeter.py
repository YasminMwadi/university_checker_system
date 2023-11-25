import tweepy
from textblob import TextBlob
from datetime import datetime
from django.utils import timezone

def project_sentiment_analysis(university_name, api_key, api_secret_key, access_token, access_token_secret):
    auth = tweepy.OAuthHandler(api_key, api_secret_key)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    # Step 1: Search for tweets with the university name
    search_results = tweepy.Cursor(api.search, q=university_name, count=10, lang="en").items()

    # Perform sentiment analysis and capture the results
    sentiment_results = []

    for tweet in search_results:
        tweet_id = tweet.id_str
        tweet_text = tweet.text
        tweet_date = timezone.make_aware(tweet.created_at)

        # Perform sentiment analysis using TextBlob
        analysis = TextBlob(tweet_text)
        sentiment_score = analysis.sentiment.polarity

        # Categorize sentiments
        if sentiment_score > 0:
            sentiment_category = "Positive"
        elif sentiment_score < 0:
            sentiment_category = "Negative"
        else:
            sentiment_category = "Neutral"

        sentiment_results.append({
            "tweet_id": tweet_id,
            "university_name": university_name,
            "tweet": tweet_text,
            "tweet_date": tweet_date,
            "sentiment": sentiment_category
        })

    return sentiment_results

if __name__ == "__main__":
    selected_university_name = "Tshwane university of technology"
    api_key = "e4PodYiTVLRPpvS4sZKf06FEK"
    api_secret_key = "0rAtVZDlJtH8poeswVaftyGU51hxCc7JWwaO8ecZdU1frSqBs5"
    access_token = "1615056030676750365-Exeqbj8TJb15CdlwplaO3FxO5X9ss4"
    access_token_secret = "VqPYqg3hRyKn2CRu3gNCqsulkC7SJ1dbpsDx4Yzy3FLqj"

    results = project_sentiment_analysis(
        selected_university_name, api_key, api_secret_key, access_token, access_token_secret
    )

    for result in results:
        print(result)
