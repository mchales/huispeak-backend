from rest_framework import serializers
from apps.storyline.models import Story, Adventure, Quest


class QuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quest
        fields = ('id', 'title', 'quest_num')


class AdventureSerializer(serializers.ModelSerializer):
    quests = serializers.SerializerMethodField()

    class Meta:
        model = Adventure
        fields = ('id', 'title', 'adventure_num', 'quests')

    def get_quests(self, obj):
        # Order quests by 'quest_num' and exclude any quest where include is false
        quests = obj.quests.filter(include=True).order_by('quest_num')
        return QuestSerializer(quests, many=True).data


class StorySerializer(serializers.ModelSerializer):
    adventures = serializers.SerializerMethodField()

    class Meta:
        model = Story
        fields = ('id', 'title', 'story_num','adventures')

    def get_adventures(self, obj):
        # Order adventures by 'adventure_num'
        adventures = obj.adventures.filter(include=True).order_by('adventure_num')
        return AdventureSerializer(adventures, many=True).data
