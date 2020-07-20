from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import User


class UserCreationForm2(UserCreationForm):

    class Meta(UserCreationForm):
        model = User
        fields = ('email',)