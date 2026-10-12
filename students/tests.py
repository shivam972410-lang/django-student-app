from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Student


class StudentPortalTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username='portal-user', password='Test-password-123!'
        )

    def setUp(self):
        self.student = Student.objects.create(
            name='Asha Patel', email='asha@example.com', course='Physics', age=20
        )

    def test_login_page_is_available_and_authenticates(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome back')
        response = self.client.post(reverse('login'), {
            'username': 'portal-user', 'password': 'Test-password-123!'
        })
        self.assertRedirects(response, reverse('home'))

    def test_admin_route_exists(self):
        response = self.client.get(reverse('admin:index'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/admin/login/', response.url)

    def test_student_pages_require_authentication(self):
        protected_urls = [
            reverse('home'), reverse('add_student'),
            reverse('edit_student', args=[self.student.pk]),
            reverse('delete_student', args=[self.student.pk]),
        ]
        for url in protected_urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertRedirects(response, f'{reverse("login")}?next={url}')

    def test_dashboard_lists_students_and_searches(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('home'), {'q': 'asha'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Asha Patel')
        self.assertEqual(response.context['total_students'], 1)

    def test_add_student_and_validate_unique_email(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('add_student'), {
            'name': 'Ravi Kumar', 'email': 'ravi@example.com', 'course': 'Math', 'age': 19,
        })
        self.assertRedirects(response, reverse('dashboard'))
        self.assertTrue(Student.objects.filter(email='ravi@example.com').exists())

        response = self.client.post(reverse('add_student'), {
            'name': 'Another Student', 'email': 'asha@example.com', 'course': 'Math', 'age': 19,
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'already exists')

    def test_edit_student(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('edit_student', args=[self.student.pk]), {
            'name': 'Asha P.', 'email': 'asha@example.com', 'course': 'Chemistry', 'age': 21,
        })
        self.assertRedirects(response, reverse('dashboard'))
        self.student.refresh_from_db()
        self.assertEqual(self.student.name, 'Asha P.')
        self.assertEqual(self.student.course, 'Chemistry')

    def test_delete_requires_confirmation_then_post(self):
        self.client.force_login(self.user)
        url = reverse('delete_student', args=[self.student.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Delete this student?')
        self.assertTrue(Student.objects.filter(pk=self.student.pk).exists())

        response = self.client.post(url)
        self.assertRedirects(response, reverse('dashboard'))
        self.assertFalse(Student.objects.filter(pk=self.student.pk).exists())

    def test_logout_is_post_only(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue('_auth_user_id' in self.client.session)
        response = self.client.post(reverse('logout'))
        self.assertRedirects(response, reverse('login'))
        self.assertNotIn('_auth_user_id', self.client.session)
