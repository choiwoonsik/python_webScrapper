import requests
from bs4 import BeautifulSoup

PAGE = 1
URL = "https://stackoverflow.com/jobs?q=java"
DETAIL_LINK = "https://stackoverflow.com/jobs/"

def extract_page():
  try:
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, 'html.parser')
    pagination = soup.find('div', {"class":"s-pagination"})
    # max_page = (int)(pagination.find("a")['title'][-3:].strip())
    pages = pagination.find_all("a")
    last_page = pages[-2].get_text(strip=True)
    return int(last_page)
  except:
    print("STACK_OVER_FLOW_ERROR")
    return None

def extract_job(html):
  link_ID = html.find("a", {
        "class":"s-link"
        })['href'].split('/')[2]
  title = html.find("a").string
  company, location = html.find("h3", {
        "class":"fc-black-700"
        }).find_all(
          "span", recursive=False)
  company = company.get_text(strip=True)
  location = location.get_text(strip=True)
  relative_all = html.find("div", {
        "class":"ps-relative"})
  relative_skills = []
  relatives = relative_all.find_all("a", {"class":"post-tag"})
  for relative in relatives:
    relative_skills.append(relative.string)
  return {
    "title":title,
    "company":company,
    "location":location,
    "relative_skills":relative_skills,
    "detail_link":f"{DETAIL_LINK}{link_ID}"
  }

def extract_jobs(last_page):
  jobs = []
  if last_page > 20:
    last_page = 20
  for page in range(last_page):
    result = requests.get(f"{URL}&pg={page+1}")
    print(f"Scrapping stack page{page+1} -> {result}")
    html_page = BeautifulSoup(result.text, 'html.parser')
    htmls = html_page.find_all("div", {"class":"grid--cell fl1"})
    for html in htmls:
      job = extract_job(html)
      jobs.append(job)
  return jobs


def get_jobs():
  last_page = extract_page()
  jobs = extract_jobs(last_page)
  return jobs