from django.test import TestCase

from ..forms import SignUpForm


class SignUpFormTests(TestCase):
    def test_forms_has_field(self):
        form = SignUpForm()
        expected = ['username', 'email', 'password1', 'password2']
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)