from django.urls import path, include

app_name = 'assistants'

urlpatterns = [
    path('v1/', include(('apps.assistants.api.v1.urls', 'v1'), namespace='v1')),
]