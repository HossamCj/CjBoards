from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class LoginRequiredPasswordChangeTests(TestCase):
    def test_redirection(self):
        url = reverse('password_change')
        login_url = reverse('login')
        response = self.client.get(url)
        self.assertRedirects(response, f'{login_url}?next={url}')


class PasswordChangeTestCase(TestCase):
    def setUp(self, data={}):
        self.user = User.objects.create_user(username='naima', email='naima@gmail.com', password='old_password')
        self.url = reverse('password_change')
        self.client.login(username='naima', password='old_password')
        self.response = self.client.post(self.url, data)


class SuccessfulPasswordChangeTests(PasswordChangeTestCase):
    def setUp(self):
        super().setUp({
            'old_password': 'old_password',
            'new_password1': 'new_password',
            'new_password2': 'new_password'
        })

    def test_redirection(self):
        '''
            A valid form submission should redirect the user
        '''
        self.assertRedirects(self.response, reverse('password_change_done'))

    def test_password_changed(self):
        '''
            refresh the user instance from the database to the new
            password hash updated by the change password view.
        '''
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('new_password'))

    def test_authentication(self):
        '''
            Create a new request to and arbitrary page.
            The resulting response should now have and 'user' to its context, after successful sign up
        '''
        response = self.client.get(reverse('home'))
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)


class invalidPasswordChangeTests(PasswordChangeTestCase):
    def test_statud_code(self):
        '''
        An invalid form submission should return the same page
        '''
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    def test_didnt_change_password(self):
        '''
        Refresh the user instance from the database to make sure
        we have the lates data
        '''
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('old_password'))
