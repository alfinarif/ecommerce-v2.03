from django.forms import ModelForm

from account.models import User, Profile

from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2',)


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ('user',)
