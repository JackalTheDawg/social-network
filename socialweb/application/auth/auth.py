from django.shortcuts import render, redirect
from django.contrib.auth import login
from application.auth import CustomAuthBackend
from application.models import *
from django.contrib import messages
from application.forms import *
from django.shortcuts import HttpResponse

class AuthenticateUser:

    def check_session(self, request):
        if request.user.id is not None:
            return request.user.id
        else:
            return None

    def sign_in(self, request, users_data):
        try:
            check_user = CustomAuthBackend()
            user = check_user.authenticate(email=users_data['email'],
                                           password=users_data['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return user.id
            else:
                return None
        except CustomUser.DoesNotExist:
            return None

    def sign_up(self, request, registration_data):
        try:
            email = CustomUser.objects.get(email=registration_data['email'])
            number = CustomUser.objects.get(phone_number=registration_data['phone_number'])
            if email.exists() or number.exists() is not False:
                return None
        except CustomUser.DoesNotExist:
            users_data = registration_data.cleaned_data
            registration_data.save()
            user_id = self.sign_in(request, users_data)
            return user_id