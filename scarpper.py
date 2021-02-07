from indeed import get_jobs as get_indeed_jobs
from stackoverflow import get_jobs as get_stack_jobs

def get_jobs(word):
  indeed_jobs = get_indeed_jobs(word)
  stack_jobs = get_stack_jobs(word)
  jobs = indeed_jobs + stack_jobs
  return jobs