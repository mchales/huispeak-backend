from rest_framework import serializers
from apps.storyline.models import Story, Adventure, Quest

class StoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = ('id', 'title', 'description', 'story_num')

class AdventureDetailSerializer(serializers.ModelSerializer):
    story = StoryDetailSerializer()

    class Meta:
        model = Adventure
        fields = ('id', 'title', 'description', 'adventure_num', 'story')