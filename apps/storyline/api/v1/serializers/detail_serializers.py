from rest_framework import serializers
from .serializers import StorySerializer, AdventureSerializer, QuestSerializer
from apps.storyline.models import Story, Adventure, Quest
from apps.assistants.models import QuestAssistant


class StoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = ('id', 'title', 'description', 'story_num')

class AdventureDetailSerializer(serializers.ModelSerializer):
    story = StorySerializer()

    class Meta:
        model = Adventure
        fields = ('id', 'title', 'description', 'adventure_num', 'story')

class QuestDetailSerializer(serializers.ModelSerializer):
    adventure = AdventureSerializer()
    assistant_id = serializers.SerializerMethodField()

    class Meta:
        model = Quest
        fields = ('id', 'title', 'description', 'quest_num', 'adventure', 'assistant_id')

    def get_assistant_id(self, obj):
        try:
            return QuestAssistant.objects.get(quest=obj).assistant.openai_assistant_id
        except QuestAssistant.DoesNotExist:
            return None