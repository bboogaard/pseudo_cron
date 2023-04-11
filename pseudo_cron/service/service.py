import logging
from typing import List

from django.utils.timezone import now

from .functools import exec_safe
from .models import Job
from ..decorators import cron_jobs
from ..utils import timestamp_to_datetime


logger = logging.getLogger(__name__)


class CronService:

    jobs: List[Job]

    def __init__(self):
        self.jobs = self.get_jobs()

    def run(self):
        current_time = now().timestamp()
        for job in self.get_jobs_to_run(current_time):
            self.job_execute(job)
            job.last_run = int(current_time)
            job.save()
            logger.info('Next run: {}'.format(timestamp_to_datetime(job.next_run)))

    @staticmethod
    def job_execute(job: Job):
        logger.info('Cron triggered for job {}'.format(job.job_name))
        try:
            exec_safe(job.func, job.max_run_time)
            job.error = ''
        except Exception as exc:
            job.error = str(exc)
            logger.error('Error executing job {}: {}'.format(job.job_name, str(exc)))

    def get_jobs_to_run(self, time: float):

        def _job_should_run(job: Job) -> bool:
            logger.info('Checking cron job {}'.format(job.job_name))
            return time >= job.next_run

        return list(filter(_job_should_run, self.jobs))

    @staticmethod
    def get_jobs():
        jobs = []
        for scheduled_job in cron_jobs:
            jobs.append(scheduled_job.load())
        return jobs
