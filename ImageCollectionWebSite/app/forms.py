from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from app.models import Image
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class BootstrapAuthenticationForm(AuthenticationForm):
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Nazwa użytkownika'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Hasło'}))

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = [
            'title',
            'description',
            'image',
            'canComment'
            ]
    def __init__(self, *args, **kwargs):
        super(ImageForm, self).__init__(*args, **kwargs)

        self.fields['title'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['style'] = 'resize: none;'
        self.fields['image'].widget.attrs['class'] = 'form-control'
        self.fields['canComment'].widget.attrs['class'] = 'form-control'


class BootstrapUserCreationForm(UserCreationForm):
    class Meta:
        model=User
        fields = ('username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(BootstrapUserCreationForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'