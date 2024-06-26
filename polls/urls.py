from django.urls import path

from . import views

app_name = "polls"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:pk>/report/", views.ReportView.as_view(), name="report"),
    path("<int:pk>/submitted/", views.SubmitView.as_view(), name="submitted"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
    path("<int:question_id>/submitReport/", views.submitReport, name="submitReport"),

]