import csv

def save_to_file(jobs):
  file = open("jobs.csv", mode="w") #open
  writer = csv.writer(file) # writer
  writer.writerow(
    ["title", "company", "location", "day", "link", "relative_skills"])
  for job in jobs:
    #dict에서 값만 가져오는데 타입을 배열로 가져온다
    writer.writerow(list(job.values()))
  return