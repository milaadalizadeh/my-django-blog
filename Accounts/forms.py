from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm


class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')                      #ba kwargs be views.py vasl shodim va user ro gereftim (badesh pak kardim)
        super(ProfileForm, self).__init__(*args, **kwargs)

        self.fields['username'].help_text = None  #agar mikhastim help texti neveshte beshe bayad dakhele "  " minevshtim

        if not user.is_superuser:
            self.fields['username'].disabled = True
            self.fields['email'].disabled = True
            self.fields['special_user'].disabled = True
            self.fields['is_author'].disabled = True


    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'special_user', 'is_author']





class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
