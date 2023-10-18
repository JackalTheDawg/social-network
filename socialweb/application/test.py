# import unittest
#
# from django.test import TestCase, Client
# from application.forms import *
# from application.auth.auth import AuthenticateUser
# from django.http import HttpRequest
# from django.contrib.auth.models import AnonymousUser
# from django.contrib.sessions.backends.db import SessionStore
# from django.contrib.sites.models import Site
#
#
# class AuthTestCase(TestCase, Client):
#     testAuth = AuthenticateUser()
#
#     data = {'correct': {'email': 'test@test.com',
#                         'password': 'testpass'},
#             'uncorrect': {'email': 'uncorrect@test.com',
#                           'password': 'uncorpass'}
#             }
#
#
#     site = Site()
#
#     testRequest = HttpRequest()
#     testRequest.user = AnonymousUser()
#     testRequest.META['SERVER NAME'] = site.domain
#     testRequest.META['SERVER_PORT'] = 80
#
#     session = SessionStore()
#     session.create()
#
#     testRequest.session = session
#
#
#     def setUp(self):
#         CustomUser.objects.create_user(email=self.data['correct']['email'],
#                                        password=self.data['correct']['password'])
#
#     """Authorization existing user"""
#     def test_caseOne(self):
#         form = Sign_in_form(data=self.data['correct'])
#         if form.is_valid():
#             form_data = form.cleaned_data
#             response = self.testAuth.sign_in(self.testRequest, form_data)
#             self.assertTrue(response, 'successfuly authorizated')
#
#     """Authorization non-existent user"""
#     @unittest.expectedFailure
#     def test_caseTwo(self):
#         form = Sign_in_form(data=self.data['uncorrect'])
#         if form.is_valid():
#             form_data = form.cleaned_data
#             response = self.testAuth.sign_in(self.testRequest, form_data)
#             self.assertTrue(response, 'User doesnt exist')
#
#
