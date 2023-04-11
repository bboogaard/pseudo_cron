from dataclasses import dataclass, field, replace
from typing import Callable, Optional

from ..models import Job as DbJob


@dataclass
class Job:
    job_name: str
    func: Callable
    frequency: int
    max_run_time: int
    last_run: Optional[int] = field(default=0)
    error: Optional[str] = field(default='')

    @property
    def next_run(self):
        return self.last_run + self.frequency

    def load(self) -> 'Job':
        db_job, _ = DbJob.objects.update_or_create(job_name=self.job_name, defaults={
            'frequency': self.frequency,
            'max_run_time': self.max_run_time
        })
        return replace(self, last_run=db_job.last_run)

    def save(self):
        DbJob.objects.filter(job_name=self.job_name).update(last_run=self.last_run, error=self.error)
