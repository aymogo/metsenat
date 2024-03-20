from django.urls import path
from sponsors import views


urlpatterns = [
    path("sponsor/", views.SponsorListView.as_view()),
    path("student/", views.StudentListView.as_view()),
    path("donation/", views.DonationListView.as_view()),
]
