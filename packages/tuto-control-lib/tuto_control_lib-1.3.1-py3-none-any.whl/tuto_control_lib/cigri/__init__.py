from .cigri import CiGri
from .oar import Scheduler
from .jobs import Campaign, PrioRandom, PrioStep
from .events import Time, SortedList, Event, event_loop

import numpy as np
import matplotlib.pyplot as plt
from math import sqrt

def plot_cigri(data):
    df = np.array(data)
    n = len(df)
    fig, axs = plt.subplots(3, 1)
    axs[0].step(df[0:n,0],df[0:n,1], linewidth=0.5)
    axs[0].set_title('Waiting Jobs')
    axs[1].step(df[0:n,0],df[0:n,2], 'tab:orange', linewidth=0.5)
    axs[1].set_title('Running Jobs')
    axs[2].step(df[0:n,0],df[0:n,3], 'tab:green', linewidth=0.5)
    axs[2].set_title('Submission Size')
    for ax in axs.flat:
        ax.label_outer()
        
def _get_95_confidence_interval(array):
    mean = np.mean(array)
    sd = np.std(array)
    n = len(array)
    ci = 2 * sd / sqrt(n - 1)
    
    return (mean, ci)
        
def stats_cigri(data):
    df = np.array(data)
    (mean_wait, ci_wait) = _get_95_confidence_interval(df[0:len(df), 1])
    (mean_run, ci_run) = _get_95_confidence_interval(df[0:len(df), 2])

    print(f"Waiting jobs: {mean_wait} +/- {ci_wait} (95%)")
    print(f"Running jobs: {mean_run} +/- {ci_run} (95%)")

def main_loop(ctrl, nb_resources=100, number_cigri_jobs=5000, cigri_job_duration=120, prio=None):
    time = Time()
    event_list = SortedList()
    oar_server = Scheduler(nb_resources, time, event_list)
    cigri = CiGri(oar_server, ctrl, time, event_list, 30)
    
    c1 = Campaign(number_cigri_jobs, cigri_job_duration)
    cigri.submit_campaign_to_cigri(c1)
        
    event_list.insert(Event(0, cigri.cigri_action))

    if prio:
        prio_instance = prio(oar_server, time, event_list)
        event_list.insert(Event(0, prio_instance.submit))
    
    event_loop(event_list, time)

    return cigri.data