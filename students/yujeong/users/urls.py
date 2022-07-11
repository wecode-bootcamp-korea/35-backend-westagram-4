from django.urls import URLPattern, path
from users.views import SignUpView

urlpatterns = [
    path('/signup', SignUpView.as_view()),
]