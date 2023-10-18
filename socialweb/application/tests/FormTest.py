import unittest

from django.test import TestCase
from application.forms import *


class TestForms(TestCase):
    data = {'sign_in': {'email': '',
                        'password': ''},
            'registration': {'email': '',
                             'password': '',
                             'phone_number': '',
                             'name': '',
                             'surname': '',
                             'sex': '',
                             'birthday': '',
                             'birthday_month': '',
                             'birthday_year': ''
                            }
                      }

    def test_one(self):
        form = Sign_in_form(data=self.data['sign_in'])
        self.assertEqual(form.is_valid(), False)

    def test_two(self):
        form = Registration_form(data=self.data['registration'])
        self.assertEqual(form.is_valid(), False)

    def test_three(self):
        self.data['sign_in']['email'] = 'some-email'
        self.data['sign_in']['password'] = 'some-pass'
        form = Sign_in_form(data=self.data['sign_in'])
        self.assertEqual(form.is_valid(), True)

    """Testing uncorret values for Registration form"""
    @unittest.expectedFailure
    def test_four(self):
        for keys in self.data['registration']:
            self.data['registration'][keys] = 'some-value'
        form = Registration_form(data=self.data['registration'])
        self.assertEqual(form.is_valid(), True, msg=form.errors.as_data())