from rest_framework import generics
from apps.storyline.models import Story, Adventure
from apps.storyline.api.v1.serializers.serializers import StorySerializer
from apps.storyline.api.v1.serializers.detail_serializers import AdventureDetailSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


@permission_classes([IsAuthenticated])
class StoryListView(generics.ListAPIView):
    queryset = Story.objects.filter(include=True).order_by('story_num')
    serializer_class = StorySerializer

    def list(self, request, *args, **kwargs):
        
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
    
        return Response({"stories": serializer.data})


@permission_classes([IsAuthenticated])
class AdventureDetailView(generics.RetrieveAPIView):
    queryset = Adventure.objects.filter(include=True)
    serializer_class = AdventureDetailSerializer
    lookup_field = 'pk'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({"adventure": serializer.data})