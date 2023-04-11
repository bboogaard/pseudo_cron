from django.contrib import admin

from .models import Job


class JobAdmin(admin.ModelAdmin):

    fields = ('job_name', 'frequency', 'max_run_time', 'last_run_time', 'next_run_time', 'error')

    list_display = ('job_name', 'frequency', 'last_run_time', 'next_run_time', 'error')

    readonly_fields = ('job_name', 'frequency', 'max_run_time', 'last_run_time', 'next_run_time', 'error')


admin.site.register(Job, JobAdmin)
