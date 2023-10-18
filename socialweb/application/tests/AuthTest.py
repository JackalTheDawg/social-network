import unittest

from django.test import TestCase
from application.forms import *
from application.auth.auth import AuthenticateUser
from django.http import HttpRequest
from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sites.models import Site


class AuthTestCase(TestCase):
    testAuth = AuthenticateUser()

    data = {'correct': {'email': 'test@test.com',
                        'password': 'testpass'},
            'uncorrect': {'email': 'uncorrect@test.com',
                          'password': 'uncorpass'},
            'registration': {'email': 'new@user.com',
                             'password': 'test',
                             'phone_number': 7777777777,
                             'name': 'test',
                             'surname': 'test',
                             'sex': 'O',
                             'birthday': 17,
                             'birthday_month': 'August',
                             'birthday_year': 1960
                             }
            }


    site = Site()

    testRequest = HttpRequest()
    testRequest.user = AnonymousUser()
    testRequest.META['SERVER NAME'] = site.domain
    testRequest.META['SERVER_PORT'] = 80

    session = SessionStore()
    session.create()

    testRequest.session = session


    def setUp(self):
        CustomUser.objects.create_user(email=self.data['correct']['email'],
                                       password=self.data['correct']['password'])

    """Authorization existing user"""
    def test_caseOne(self):
        form = Sign_in_form(data=self.data['correct'])
        if form.is_valid():
            form_data = form.cleaned_data
            response = self.testAuth.sign_in(self.testRequest, form_data)
            user = CustomUser.objects.get(email=self.data['correct']['email'])
            self.assertEqual(response, user.id)
        else:
            self.assertEqual(form.is_valid(), True, msg=form.errors.as_data())

    """Authorization non-existent user"""
    # @unittest.expectedFailure
    def test_caseTwo(self):
        self.data['correct']
        form = Sign_in_form(data=self.data['uncorrect'])
        if form.is_valid():
            form_data = form.cleaned_data
            response = self.testAuth.sign_in(self.testRequest, form_data)
            self.assertFalse(response, 'User doesnt exist')
        else:
            self.assertEqual(form.is_valid(), True, msg=form.errors.as_data())

    @unittest.expectedFailure
    def test_caseThree(self):
        self.data['correct']['password'] = self.data['uncorrect']['password']
        form = Sign_in_form(data=self.data['correct'])
        if form.is_valid():
            form_data = form.cleaned_data
            response = self.testAuth.sign_in(self.testRequest, form_data)
            user = CustomUser.objects.get(email=self.data['correct']['email'])
            self.assertEqual(response, user.id)
        else:
            self.assertEqual(form.is_valid(), True, msg=form.errors.as_data())

    """Registration user"""
    def test_registrationCase(self):
        form = Registration_form(data=self.data['registration'])
        if form.is_valid():
            response = self.testAuth.sign_up(self.testRequest, form)
            newUserid = CustomUser.objects.get(email=self.data['registration']['email'])
            self.assertEqual(response, newUserid.id)
        else:
            self.assertEqual(form.is_valid(), True, msg=form.errors.as_data())


    """Registration with uncorrect data"""
    @unittest.expectedFailure
    def test_uncorrectRegistration(self):
        self.data['registration']['email'] = None
        form = Registration_form(data=self.data)
        if form.is_valid():
            self.assertEqual(form.is_valid(), False, msg=form.errors.as_data())
        else:
            self.assertEqual(form.is_valid(), True, msg=form.errors.as_data())


