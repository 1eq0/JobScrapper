import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}

def extract_job(html):
    title = html.find("h2",{"itemprop":"title"}).get_text(strip=True)
    company = html.find("h3",{"itemprop":"name"})
    company = company.get_text(strip=True)
    job_id = html['data-id']
    return {
        'title': title,
        'company': company,
        'apply_link': f"https://remoteok.io/l/{job_id}"
    }

def extract_jobs(url):
  jobs = []
  result = requests.get(f"{url}",headers=headers)
  soup = BeautifulSoup(result.text,"html.parser")
  results = soup("tr", {"class": "job"})
  i = 1
  for result in results:
    job = extract_job(result)
    print(f"scrap remoteok {i}")
    i+=1
    jobs.append(job)
  return jobs


def get_rm_jobs(term):
  url = f"https://remoteok.io/remote-dev+{term}-jobs"
  jobs = extract_jobs(url)
  return jobs
