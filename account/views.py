from django.contrib.auth import login, authenticate
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.views import LoginView as BaseLoginView, LogoutView as BaseLogoutView
from .forms import LoginFrom

class IndexView(TemplateView):
    template_name = "index.html"

class LoginView(BaseLoginView):
    form_class = LoginFrom
    template_name = "account/login.html"

class LogoutView(BaseLogoutView):
    template_name = "account/logout.html"

