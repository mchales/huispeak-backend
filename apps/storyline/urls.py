from django.urls import path, include

app_name = 'storyline'

urlpatterns = [
    path('v1/', include(('apps.storyline.api.v1.urls', 'v1'), namespace='v1')),
]