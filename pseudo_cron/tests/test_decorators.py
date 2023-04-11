from django.test.testcases import SimpleTestCase

from pseudo_cron.decorators import cron_jobs, schedule_job


def my_test_func():
    ...


class TestDecorators(SimpleTestCase):

    def test_schedule_job(self):
        schedule_job(300)(my_test_func)
        self.assertEqual(len(cron_jobs), 1)
        job = cron_jobs[0]
        self.assertEqual(job.job_name, 'pseudo_cron.tests.test_decorators.my_test_func')
        self.assertEqual(job.func, my_test_func)
        self.assertEqual(job.frequency, 300)
        self.assertEqual(job.max_run_time, 10)
