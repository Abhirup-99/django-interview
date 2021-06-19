from django.urls import path

from . import views

urlpatterns = [
    path("", views.indexView),
    path("create", views.submitFormView),
    path("view", views.readInterviewsView),
    path("update", views.views.updateInterview),
    path("*", views.indexView),
]
