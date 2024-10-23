from django.urls import path
from .views import StoryListView, AdventureDetailView, QuestDetailView

urlpatterns = [
    path('storyline/', StoryListView.as_view(), name='story-list'),
    path('adventure/<int:pk>/', AdventureDetailView.as_view(), name='adventure-detail'),
    path('quest/<int:pk>/', QuestDetailView.as_view(), name='quest-detail'),
]
