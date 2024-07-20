from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import CustomUser

class LoginFrom(AuthenticationForm):
    class Meta:
        model = CustomUser

