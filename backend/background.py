import atexit
from apscheduler.schedulers.background import BackgroundScheduler

class BackgroundSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.scheduler = BackgroundScheduler(job_defaults={'max_instances': 20})
            atexit.register(cls._instance.shutdown)
        return cls._instance

    def start(self):
        self.scheduler.start()

    def shutdown(self):
        self.scheduler.shutdown()

    def add_job(self, *args, **kwargs):
        job = self.scheduler.add_job(*args, **kwargs)
        return job

    def get_jobs(self):
        return self.scheduler.get_jobs()

    def pause_job(self, job_id):
        self.scheduler.pause_job(job_id)

    def resume_job(self, job_id):
        self.scheduler.resume_job(job_id)

    def reschedule_job(self, job_id, trigger):
        self.scheduler.reschedule_job(job_id, trigger)

    def remove_job(self, job_id):
        self.scheduler.remove_job(job_id)
