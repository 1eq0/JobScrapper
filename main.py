import os
from flask import Flask,render_template,request,send_file
from so import get_so_jobs
from rm import get_rm_jobs
from we import get_we_jobs
from save import save_to_file

os.system('clear')

app = Flask("JobScrapper")

db={}

@app.route("/")
def home():
  return render_template("home.html")

@app.route("/search")
def search():
  term = request.args.get('term')
  if term:
    term = term.lower()
    fromDB = db.get(term)
    if fromDB:
      jobs = fromDB
    else:
      so_jobs = get_so_jobs(term)
      we_jobs = get_we_jobs(term)
      rm_jobs = get_rm_jobs(term)
      jobs = so_jobs + we_jobs + rm_jobs
      db[term] = jobs
  else:
    return redirect("/")
  return render_template("search.html",term = term, resultNum = len(jobs), jobs=jobs)

@app.route("/export")
def export():
  try:
    term = request.args.get('term')
    if not term:
      raise Exception()
    term = term.lower()
    jobs = db.get(term)
    if not jobs:
      raise Exception()
    save_to_file(jobs,term)
    return send_file(f"{term}.csv", mimetype="text/csv",attachment_filename=f"{term}.csv", as_attachment=True)
  except:
    return redirect("/")
  
    
app.run(host = "0.0.0.0")
