from flask import Flask, render_template, request, redirect, send_file
from scarpper import get_jobs
from exporter import save_to_file

app = Flask("jobScrapper", template_folder='./templates', static_folder='./static')

db = {}

@app.route("/")
def home():
  return render_template('job_search.html')

@app.route("/report")
def report():
  word = request.args.get('input').strip()
  if word:
    word = word.lower()
    existing_db = db.get(word)
    if existing_db:
      jobs = existing_db
    else:
      jobs = get_jobs(word)
      db[word] = jobs;
  else:
    return redirect("/")
  return render_template(
    'report.html',
    resultsNumber=len(jobs),
    searchingBy=word,
    jobs=jobs)

@app.route("/export")
def export():
  try:
    word = request.args.get('word').strip()
    if not word:
      raise Exception()
    word = word.lower()
    jobs = db.get(word)
    if not jobs:
      raise Exception()
    save_to_file(jobs)
    return send_file("jobs.csv")
  except:
    return redirect("/")

app.run(host="127.0.0.1", port=3000)