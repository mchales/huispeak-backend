from rest_framework import generics
from apps.storyline.models import Story
from .serializers import StorySerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


# @permission_classes([IsAuthenticated])
class StoryListView(generics.ListAPIView):
    queryset = Story.objects.filter(include=True).order_by('story_num')
    serializer_class = StorySerializer

    def list(self, request, *args, **kwargs):
        
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
    
        return Response({"stories": serializer.data})
