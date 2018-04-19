#######class for jobs in a state
###params: string of the state English name, list of all job titles; 
###list of all job lats, list of all job lons, list of all job types
###used by plot_job_by_state.py

class JobinState:
    def __init__(self, state, titles, lats, lons, jobtype):
        self.state = state
        self.titles = titles
        self.lats = lats
        self.lons = lons
        self.jobtype = jobtype
    def __str__(self):
        return 'there are {} jobs in {}'.format(len(self.titles), self.state)