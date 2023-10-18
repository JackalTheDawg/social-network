from django import forms
from .models import *
from django.contrib.auth.hashers import make_password
import os


class Sign_in_form(forms.Form):
    widgets = {
            'email': forms.TextInput(attrs={'placeholder': 'Enter your email or number', 'class': 'formOne'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Enter your password', 'class': 'formOne'})
        }
    email = forms.CharField(widget=widgets['email'])
    password = forms.CharField(widget=widgets['password'])

    for fieldname in [email, password]:
        fieldname.label = ''
        fieldname.help_text = None

    fieldname = None


class Registration_form(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = (
                  'email',
                  'phone_number',
                  'name',
                  'surname',
                  'password',
                  'birthday',
                  'birthday_month',
                  'birthday_year',
                  'sex',
                  )
        widgets = {
            'email': forms.TextInput(attrs={'placeholder': 'Enter your email'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Enter your password', 'class': 'registration_password_field'}),
            'name': forms.TextInput(attrs={'placeholder': 'Enter your name'}),
            'surname': forms.TextInput(attrs={'placeholder': 'Enter your last name'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Enter your number'}),
            'sex': forms.RadioSelect(attrs={'class': 'choice-boxes'})
        }


    def __init__(self, *args, **kwargs):

        super(Registration_form, self).__init__(*args, **kwargs)

        for fieldname in ['email', 'password', 'name', 'surname', 'phone_number',
                          'sex', 'birthday', 'birthday_month', 'birthday_year']:
            self.fields[fieldname].label = ''


    """Customize save method with hashing password"""
    def save(self, commit=True, password=None):

        if self.errors:
            raise ValueError(
                "The %s could not be %s because the data didn't validate."
                % (
                    self.instance._meta.object_name,
                    "created" if self.instance._state.adding else "changed",
                )
            )
        if commit:
            """hashing password in registration form"""
            self.instance.password = make_password(self.instance.password)

            self.instance.save()
            self._save_m2m()
        else:
            self.save_m2m = self._save_m2m
        return self.instance


class PageBlogForm(forms.ModelForm):
    class Meta:
        model = BlogModel
        fields = ('post_text',
                  'post_content')

        widgets = {'post_text': forms.Textarea()}

class CommentsForm(forms.ModelForm):
    class Meta:
        model = BlogCommentsModel
        fields = ('text', 'content')
        widgets = {'text': forms.Textarea()}

class AddPhoto(forms.ModelForm):
    class Meta:
        model = PhotoGallery
        fields = ('img', 'description')

class AddVideo(forms.ModelForm):
    class Meta:
        model = Videos
        fields = ('file', 'description', 'title')

class MessageForm(forms.Form):
    message = forms.CharField()

class Change_profiles_info(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = (
            'email',
            'phone_number',
            'name',
            'surname',
            'birthday',
            'birthday_month',
            'birthday_year',
            'sex'
        )


    def __init__(self, *args, **kwargs):
        super(Change_profiles_info, self).__init__(*args, **kwargs)

        for fieldname in self.fields:
            self.fields[fieldname].required = False

class Change_picture(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('profile_picture',)