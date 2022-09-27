from django_cron import CronJobBase, Schedule
import requests

class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 5 # every 1 minutes
    RETRY_AFTER_FAILURE_MINS = 1
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS, retry_after_failure_mins=RETRY_AFTER_FAILURE_MINS)
    code = 'crm_conn.my_cron_job'    # a unique code

    def do(self):
        print('cron radi...')