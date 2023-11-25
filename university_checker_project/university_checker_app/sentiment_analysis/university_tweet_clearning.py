import matplotlib
matplotlib.use('Agg')
from university_checker_app.models import FilteredTweets
import re
import emoji
from textblob import TextBlob
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import os


os.environ['MPLBACKEND'] = 'Agg'

def generate_word_cloud(text, title):
    # Create a WordCloud object with desired parameters
    wordcloud = WordCloud(
        width=800,              # Width of the word cloud image
        height=400,             # Height of the word cloud image
        background_color='white',  # Background color of the word cloud
        colormap='coolwarm'     # Colormap for color scheme
    ).generate(text)

    # Creating a matplotlib figure for displaying the word cloud
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")  # Remove axis labels
    plt.title(title)  # Set the title for the word cloud

    # Save the word cloud as an image in memory
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()

    # Convert the word cloud to base64-encoded data
    wordcloud_base64 = base64.b64encode(buffer.getvalue()).decode()

    return wordcloud_base64


def clean_twitter_text(tweet_text):
    # Remove URLs
    tweet_text = re.sub(r"http\S+|www\S+|https\S+", '', tweet_text, flags=re.MULTILINE)

    # Remove mentions (e.g., @username)
    tweet_text = re.sub(r'@[\w_]+', '', tweet_text)

    # Remove hashtags (e.g., #example)
    tweet_text = re.sub(r'#', '', tweet_text)

    # Remove special characters and punctuation
    tweet_text = re.sub(r'[^\w\s]', '', tweet_text)

    # Remove extra whitespace
    tweet_text = ' '.join(tweet_text.split())

    # Convert emojis to understandable words
    tweet_text = emoji.demojize(tweet_text)

    # Remove colons from emojis and underscores from words
    tweet_text = tweet_text.replace(":", " ").replace("_", " ")

    # Convert text to lowercase
    tweet_text = tweet_text.lower()

    # Calculate sentiment
    sentiment_results = sentiment_score(tweet_text)

    #Assigning tweet_text to variable cleaned_text
    cleaned_text = tweet_text

    return cleaned_text, sentiment_results



def sentiment_score(tweet_text):
    # Perform sentiment analysis using TextBlob
    analysis = TextBlob(tweet_text)
    sentiment = analysis.sentiment
    sentiment_score = sentiment.polarity

    # Initialize variables for sentiment categories
    sentiment_category = None

    # Categorize sentiments
    if sentiment_score > 0:
        sentiment_category = "Positive"
    elif sentiment_score < 0:
        sentiment_category = "Negative"
    else:
        sentiment_category = "Neutral"

    # Create a list with the sentiment results
    sentiment_results = {
        "sentiment": sentiment_category,
    }

    return sentiment_results

