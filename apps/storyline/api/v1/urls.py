from django.urls import path
from .views import StoryListView

urlpatterns = [
    path('storyline/', StoryListView.as_view(), name='story-list'),
]
