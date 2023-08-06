from .events import *
from .jobs import *

class CiGri:
    def __init__(self, oar_server, controller, time, event_list, sleep_time = 5):
        self.sleep_time = sleep_time
        self.campaigns = {}
        self.oar_server = oar_server
        self.job_ids_of_latest_submission = []
        self.controller = controller
        self.time = time
        self.event_list = event_list
        self.data = []

    def submit_campaign_to_cigri(self, campaign):
        self.campaigns[campaign.campaign_id] = campaign

    def get_jobs_to_submit_to_oar(self, campaign_id, n):
        n = int(n)
        jobs_to_submit = [j for j in filter(lambda j: j.state == "undone", self.campaigns[campaign_id].jobs.values())]
        if n < len(jobs_to_submit):
            return jobs_to_submit[0:n]
        return jobs_to_submit

    def submit_jobs_to_oar(self, jobs_to_submit):
        for j in jobs_to_submit:
            self.job_ids_of_latest_submission.append(j.job_id)
            j.state = "executing"
            self.event_list.insert(Event(self.time.get(), lambda job: self.oar_server.submit_job(job), j))

    def update_data_campaign(self, campaign_id):
        c = self.campaigns[campaign_id]
        for job in c.jobs.values():
            if self.oar_server.has_been_executed(job.job_id):
                job.state = "done"
        c.nb_remaining_jobs_to_execute = sum(map(lambda x: 1, filter(lambda job: job.state != "done", c.jobs.values())))
        self.job_ids_of_latest_submission = []

    def get_sum_nb_jobs_remaining(self):
        return sum(map(lambda c : c.nb_remaining_jobs_to_execute, iter(self.campaigns.values())))
    
    def cigri_action(self):
        oar_data = self.oar_server.log()
        
        self.controller.update_submission_size(oar_data)
        n = self.controller.get_submission_size()

        for i in self.campaigns.keys():
            self.update_data_campaign(i)
        try:
            min_remaining_campaign_id = min(map(lambda c: c.campaign_id, filter(lambda c: c.nb_remaining_jobs_to_execute > 0 ,self.campaigns.values())))
        except:
            self.event_list.insert(Event(-1, lambda x: x))
            return
        
        jobs = self.get_jobs_to_submit_to_oar(min_remaining_campaign_id, n)
        self.submit_jobs_to_oar(jobs)


        oar_data.append(n)
        self.data.append(oar_data)
        self.event_list.insert(Event(self.time.get() + self.sleep_time, lambda : self.cigri_action()))
        
