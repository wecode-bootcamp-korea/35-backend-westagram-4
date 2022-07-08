from django.urls import path
from users.views import UserView, SignInView

urlpatterns = [
    path('', UserView.as_view()),
    path('/login', SignInView.as_view())
]