from django.urls import include, path

from . import views

app_name = "main"

urlpatterns = [
    path("profile/", views.Profile.as_view()),
    path("devices/", views.DeviceView.as_view()),
    path("rate_element/", views.RateVideoElement.as_view()),
    path("element_types/", views.ElementsList.as_view()),
    path("videos/", views.VideoList.as_view()),
    path("videos/add/", views.AddVideo.as_view()),
    path("videos/<video_id>/", views.VideoView.as_view()),
    path("send_notification/", views.SendNotification.as_view()),
]
