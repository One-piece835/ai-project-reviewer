from django.urls import path
from .views import review_project

urlpatterns = [
    path("review/", review_project, name="review-project"),
]