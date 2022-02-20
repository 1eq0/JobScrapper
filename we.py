import requests
from bs4 import BeautifulSoup

def extract_job(html):
    title = html.find("span",{"class":"title"}).get_text(strip=True)
    company = html.find("span", {
        "class": "company"
    })
    company = company.get_text(strip=True)
    job_link = html.find("a",recursive=False)['href']
    return {
        'title': title,
        'company': company,
        'apply_link': f"https://weworkremotely.com{job_link}"
    }


def extract_jobs(url):
  jobs = []
  result = requests.get(f"{url}")
  soup = BeautifulSoup(result.text,"html.parser")
  results = soup("li", {"class": "feature"})
  i = 1
  for result in results:
    job = extract_job(result)
    print(f"scrap weworkremotely {i}")
    i+=1
    jobs.append(job)
  return jobs


def get_we_jobs(term):
  url = f"https://weworkremotely.com/remote-jobs/search?term={term}"
  jobs = extract_jobs(url)
  return jobs
