from random import randint
from .events import *

class Job:
    job_id = 0
    def __init__(self, duration):
        self.duration = duration
        self.job_id = Job.job_id
        self.state = "undone"
        Job.job_id = Job.job_id + 1
        
        self.sub_time = None
        self.start_time = None
        self.stop_time = None
        
    def get_exec_time(self):
        return self.stop_time - self.start_time
    
    def get_wait_time(self):
        return self.start_time - self.sub_time
        
class Campaign:
    campaign_id = 0
    def __init__(self, nb_jobs, duration):
        self.nb_jobs = nb_jobs
        self.nb_remaining_jobs_to_execute = nb_jobs
        self.campaign_id = Campaign.campaign_id
        Campaign.campaign_id = Campaign.campaign_id + 1
        self.generate_jobs(duration)
    
    def generate_jobs(self, duration):
        self.jobs = {}
        for _ in range(self.nb_jobs):
            job = Job(duration)
            self.jobs[job.job_id] = job

class PrioRandom:
    def __init__(self, scheduler, time, event_list, duration=60):
        self.duration = duration
        self.scheduler = scheduler
        self.time = time
        self.event_list = event_list
        
    def submit(self):
        for _ in range(randint(1, 50)):
            new_job = Job(self.duration)
            self.event_list.insert(Event(self.time.get(), lambda job: self.scheduler.submit_job(job), new_job))
        next_prio_job = randint(100, 1000)
        self.event_list.insert(Event(self.time.get() + next_prio_job, self.submit))
        
class PrioStep:
    def __init__(self, scheduler, time, event_list, duration=2000, step=32, delay=2000):
        self.duration = duration
        self.scheduler = scheduler
        self.time = time
        self.event_list = event_list
        self.step = step
        self.delay = delay
        
    def submit(self):
        for _ in range(self.step):
            new_job = Job(self.duration)
            self.event_list.insert(Event(self.time.get() + self.delay, lambda job: self.scheduler.submit_job(job), new_job))
        
    
