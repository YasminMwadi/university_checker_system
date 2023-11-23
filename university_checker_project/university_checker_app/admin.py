from django.contrib import admin
from .models import University, Tweets, FilteredTweets, ranking, Profile

# models registration
admin.site.register(University)
admin.site.register(Tweets)
admin.site.register(FilteredTweets)
admin.site.register(ranking)
admin.site.register(Profile)