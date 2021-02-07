from indeed import get_jobs as get_indeed_jobs
from stackoverflow import get_jobs as get_stack_jobs

for i in range(10):
  print("start")

# indeed
indeed_jobs = get_indeed_jobs()
# stackoverflow
stack_jobs = get_stack_jobs()
jobs = indeed_jobs + stack_jobs
for i in jobs:
  print(f"{i}\n")