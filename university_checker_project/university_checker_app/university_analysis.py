import csv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from textblob import TextBlob
from datetime import datetime
from django.utils import timezone

def project_sentiment_analysis(university_name):
    api_key = "AIzaSyC-HbektWdhghBqPGOZnI6UvQiOBgP_D0Y"
    youtube = build("youtube", "v3", developerKey=api_key)

    hashtag = university_name  # Set the hashtag to the university name

    # Step 1: Search for videos with the university name
    search_response = youtube.search().list(
        q=hashtag,
        type="video",
        part="id",
        maxResults=10
    ).execute()

    # Perform sentiment analysis and capture the results
    sentiment_results = []

    for item in search_response["items"]:
        video_id = item["id"]["videoId"]
        try:
            next_page_token = None
            while True:
                comments_response = youtube.commentThreads().list(
                    part="snippet",
                    videoId=video_id,
                    maxResults=100,
                    pageToken=next_page_token
                ).execute()

                for comment_item in comments_response["items"]:
                    comment_id = comment_item["id"]
                    comment_text = comment_item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
                    comment_date_str = comment_item["snippet"]["topLevelComment"]["snippet"]["publishedAt"]
                    comment_date = timezone.make_aware(datetime.strptime(comment_date_str, "%Y-%m-%dT%H:%M:%SZ"))
                    
                    # Perform sentiment analysis using TextBlob
                    analysis = TextBlob(comment_text)
                    sentiment = analysis.sentiment
                    sentiment_score = sentiment.polarity

                    # Categorize sentiments
                    if sentiment_score > 0:
                        sentiment_category = "Positive"
                    elif sentiment_score < 0:
                        sentiment_category = "Negative"
                    else:
                        sentiment_category = "Neutral"

                    sentiment_results.append({
                        "comment_id": comment_id,
                        "university_name": university_name,
                        "comment": comment_text,
                        "comment_date": comment_date,
                        "sentiment": sentiment_category
                    })

                next_page_token = comments_response.get("nextPageToken")
                if not next_page_token:
                    break

        except HttpError as e:
            if "commentsDisabled" in str(e):
                print(f"Comments are disabled for video {video_id}. Skipping...")
            else:
                print(f"Error processing video {video_id}: {str(e)}")

    return sentiment_results

if __name__ == "__main__":
    selected_university_name = "Tshwane university of technology"  # Replace with your university name
    results = perform_sentiment_analysis(selected_university_name)

    for result in results:
        print(result)
