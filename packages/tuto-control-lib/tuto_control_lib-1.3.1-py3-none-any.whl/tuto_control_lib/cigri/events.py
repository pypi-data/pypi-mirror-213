class Time:
    def __init__(self):
        self.current_time = 0
        
    def inc(self, inc):
        self.current_time += inc
        
    def get(self):
        return self.current_time
    
    def set(self, time):
        self.current_time = time
        
class Event:
    def __init__(self, timestamp, action, job_id = -1):
        self.timestamp = timestamp
        self.action = action
        self.job_id = job_id
        
    def get_timestamp(self):
        return self.timestamp
    
    def exec_action(self):
        if self.job_id != -1:
            self.action(self.job_id)
        else:
            self.action()
            
    def __str__(self):
        return str(self.timestamp)
    
    def __repr__(self):
        return str(self.timestamp)

class SortedList:
    def __init__(self):
        self.list = []
        
    def insert(self, e):
        length = len(self.list)
        ts = e.get_timestamp()
        i = 0
        while i < length and self.list[i].get_timestamp() < ts:
            i = i + 1
        to_insert = e
        while i < length:
            stored = self.list[i]
            self.list[i] = to_insert
            to_insert = stored
            i = i + 1
        self.list.append(to_insert)
        assert(len(self.list) == length + 1)
        
    def pop(self):
        return self.list.pop(0)
        
def event_loop(event_list, time):
    max_time = time.get()
    while len(event_list.list) > 0:
        event = event_list.pop()
        if event.timestamp == -1:
            return
        max_time = max(max_time, event.timestamp)
        time.set(max_time)
        
        event.exec_action()
 
    