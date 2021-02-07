import requests
from bs4 import BeautifulSoup

PAGE = 1
DETAIL_LINK = "https://stackoverflow.com/jobs/"

def extract_page(URL):
  try:
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, 'html.parser')
    pagination = soup.find('div', {"class":"s-pagination"})
    # max_page = (int)(pagination.find("a")['title'][-3:].strip())
    pages = pagination.find_all("a")
    last_page = pages[-2].get_text(strip=True)
    return int(last_page)
  except:
    print("NONE RESULT")
    return 0

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
  link = f"{DETAIL_LINK}{link_ID}"
  day = html.find('ul', {
        "class":"mt4 fs-caption fc-black-500 horizontal-list"
        }).find("span").string
  relative_all = html.find("div", {
        "class":"ps-relative"})
  relative_skills = ""
  relatives = relative_all.find_all("a", {"class":"post-tag"})
  for relative in relatives:
    relative_skills += relative.string
    if relative is not relatives[-1]:
      relative_skills+=", "
  return {
    'title':title,
    'company':company,
    'location':location,
    'day':day,
    'link':link,
    'relative_skills':relative_skills
  }

def extract_jobs(last_page, URL):
  jobs = []
  if last_page > 2:
    last_page = 2
  for page in range(last_page):
    result = requests.get(f"{URL}&pg={page+1}")
    print(f"Scrapping stack page{page+1} -> {result}")
    html_page = BeautifulSoup(result.text, 'html.parser')
    htmls = html_page.find_all("div", {"class":"grid--cell fl1"})
    for html in htmls:
      job = extract_job(html)
      jobs.append(job)
  return jobs


def get_jobs(word):
  URL = f"https://stackoverflow.com/jobs?q={word}"
  last_page = extract_page(URL)
  jobs = extract_jobs(last_page, URL)
  return jobs