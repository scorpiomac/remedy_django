from django.urls import path

from .views import RemedyLoginView, RemedyLogoutView

urlpatterns = [
    path("login/", RemedyLoginView.as_view(), name="login"),
    path("logout/", RemedyLogoutView.as_view(), name="logout"),
]
