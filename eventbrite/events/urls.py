from django.urls import path
from . import views

app_name = 'groups'

urlpatterns = [
    path('', views.ListEvents.as_view(), name="all"),
    path("new/", views.CreateEvent.as_view(), name="create"),
    path("posts/in/<slug>/",views.SingleEvent.as_view(),name="single"),
    path("join/<slug>/",views.LikeEvent.as_view(),name="like"),
    path("leave/<slug>/",views.UnlikeEvent.as_view(),name="unlike"),
    path("myevents",views.UserEvents.as_view(),name="userevents"),
    path("likedevents/",views.LikedEvents.as_view(),name="likedevents"),
]
