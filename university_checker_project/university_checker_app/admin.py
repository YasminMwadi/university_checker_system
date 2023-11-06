from django.contrib import admin
from .models import University, Tweets, SentimentResultAnalysis

# Register your models here.
admin.site.register(University)
admin.site.register(Tweets)
admin.site.register(SentimentResultAnalysis)
