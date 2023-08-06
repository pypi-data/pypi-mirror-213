from .events import *
from .jobs import *

class Scheduler:
    def __init__(self, resources, time, event_list):
        self.max_resources = resources
        self.current_time = 0
        self.running_jobs = {}
        self.waiting_jobs = []
        self.dict_has_been_executed = {}
        self.time = time
        self.event_list = event_list

    def get_nb_free_resources(self):
        return self.max_resources - len(self.running_jobs)
        
    def terminate_job(self, job_id):        
        self.dict_has_been_executed[job_id] = True
        self.running_jobs.pop(job_id)
        self.event_list.insert(Event(self.time.get(), self.schedule_jobs))
        
    def has_been_executed(self, job_id):
        return job_id in self.dict_has_been_executed and self.dict_has_been_executed[job_id]

    def submit_job(self, job):        
        self.waiting_jobs.append(job)
        self.dict_has_been_executed[job.job_id] = False
        self.event_list.insert(Event(self.time.get(), self.schedule_jobs))

    def schedule_jobs(self):
        nb_free_resources = self.get_nb_free_resources()
        i = 0
        initial_number_of_waiting_jobs = len(self.waiting_jobs)
        while i < initial_number_of_waiting_jobs and i < nb_free_resources:
            job = self.waiting_jobs.pop(0)
            job_id = job.job_id
            self.running_jobs[job_id] = job
            self.event_list.insert(Event(self.time.get() + job.duration, lambda j: self.terminate_job(j), job_id))
            i = i + 1     

    def log(self):
        return [self.time.get(), len(self.waiting_jobs), len(self.running_jobs)]
