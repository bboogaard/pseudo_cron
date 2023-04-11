from functools import partial
from unittest import mock

from django.test.testcases import TestCase
from django.utils.timezone import now

from pseudo_cron.models import Job as DbJob
from pseudo_cron.service.models import Job
from pseudo_cron.service.service import CronService
from pseudo_cron.tests.utils import MockProcess


class TestService(TestCase):

    frequency = 300

    job_name = 'job_test'

    max_run_time = 10

    def setUp(self):
        super().setUp()
        self.call_list = []

    def setup_jobs(self, last_run: int = 0):
        patcher = mock.patch(
            'pseudo_cron.service.service.CronService.get_jobs', partial(self.get_jobs, last_run=last_run)
        )
        patcher.start()
        self.addCleanup(patcher.stop)

    def setup_process(self, is_alive: bool = False):
        MockProcess._is_alive = is_alive
        patcher = mock.patch('multiprocessing.Process', MockProcess)
        patcher.start()
        self.addCleanup(patcher.stop)

    def get_jobs(self, last_run: int):
        job = Job(self.job_name, self.job_test, self.frequency, self.max_run_time, last_run=last_run)
        job.load()
        return [job]

    def test_run(self):
        self.setup_jobs()
        self.setup_process()
        service = CronService()
        service.run()
        self.assertJobRun()
        db_job = DbJob.objects.get(job_name='job_test')
        self.assertGreater(db_job.last_run, 0)

    def test_run_skip(self):
        self.setup_jobs(int(now().timestamp() - 60))
        self.setup_process()
        service = CronService()
        service.run()
        self.assertJobNotRun()

    def test_run_with_timeout(self):
        self.setup_jobs()
        self.setup_process(is_alive=True)
        service = CronService()
        service.run()
        self.assertJobRun()
        db_job = DbJob.objects.get(job_name='job_test')
        self.assertEqual(db_job.error, 'Job timed out')

    def job_test(self):
        self.call_list.append(1)

    def assertJobRun(self, count=1):
        self.assertEqual(sum(self.call_list), count)

    def assertJobNotRun(self):
        self.assertEqual(sum(self.call_list), 0)
