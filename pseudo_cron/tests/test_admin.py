from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import RequestFactory

from pseudo_cron.admin import JobAdmin
from pseudo_cron.models import Job


class TestJobAdmin(TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.site = AdminSite()
        self.job = Job.objects.create(job_name='job_test', frequency=300, max_run_time=10)
        self.user = User.objects.create_superuser('johndoe')

    def test_changelist(self):
        admin = JobAdmin(Job, self.site)
        request = RequestFactory().get("/")
        request.user = self.user
        response = admin.changelist_view(request)
        self.assertEqual(response.status_code, 200)
        response.render()
        self.assertContains(response, 'job_test')

    def test_change_view(self):
        admin = JobAdmin(Job, self.site)
        request = RequestFactory().get("/")
        request.user = self.user
        response = admin.change_view(request, str(self.job.pk))
        self.assertEqual(response.status_code, 200)
        response.render()
        self.assertContains(response, 'job_test')
