from django.db import models
from django.contrib.auth.models import User

# the following will upload excel file containing a list of public universities in SA
class University(models.Model):
    university_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    # established_year = models.PositiveIntegerField()
    # Add other fields as needed

    def __str__(self):
        return self.name

class Tweets(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    university_name = models.ForeignKey(University, on_delete=models.CASCADE)
    tweet_text = models.TextField()
    sentiment_score = models.CharField(max_length=100)
    created_at = models.DateTimeField()


    def __str__(self):
        return f"{self.university_name} - {self.sentiment_score}"

    
class SentimentResultAnalysis(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    sentiment = models.TextField()  # You can adjust the field type as needed
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sentiment result for {self.university}: {self.sentiment}"