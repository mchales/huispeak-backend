from django.urls import path
from .views import StoryListView, AdventureDetailView

urlpatterns = [
    path('storyline/', StoryListView.as_view(), name='story-list'),
    path('adventure/<int:pk>/', AdventureDetailView.as_view(), name='adventure-detail'),
]
