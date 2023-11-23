from django.db import models
from django.contrib.auth.models import User

# the following will upload excel file containing a list of public universities in SA
class University(models.Model):
    university_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
# all tweets model
class Tweets(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    university_name = models.ForeignKey(University, on_delete=models.CASCADE)
    tweet_text = models.TextField()
    sentiment_score = models.CharField(max_length=100)
    created_at = models.DateTimeField()


    def __str__(self):
        return f"{self.university_name} - {self.sentiment_score}"
# clearn tweet model
class FilteredTweets(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    university_name = models.ForeignKey(University, on_delete=models.CASCADE)
    filtered_tweet = models.TextField()
    sentiment_score = models.CharField(max_length=100)
    created_at = models.DateTimeField()

    def __str__(self):
        return f"Filtered Tweet by {self.user.username} at {self.created_at} for {self.university_name}"

#ranking model   
class ranking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.ForeignKey(University, on_delete=models.CASCADE)
    positive = models.IntegerField()
    negative = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sentiment result for {self.name}: {self.positive}: {self.negative}"
    
def profile_image_path(instance, filename):
    # Use the user's ID as the filename
    return f'profile_pics/{instance.user.username}_profile.jpg'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=100, blank=True)
    role = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    profile_pic = models.ImageField(upload_to=profile_image_path, blank=True, null=True)

    def __str__(self):
        return self.user.username