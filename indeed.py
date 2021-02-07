import requests
from bs4 import BeautifulSoup #https://www.crummy.com/software/BeautifulSoup/bs4/doc/
#soup method explation

LIMIT = 50
URL = f"https://kr.indeed.com/%EC%B7%A8%EC%97%85?q=java& l=seoul&limit={LIMIT}"
DETAIL_LINK = "https://kr.indeed.com/%EC%B1%84%EC%9A%A9%EB%B3%B4%EA%B8%B0?jk="

def extract_page():
  try:
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, 'html.parser')
    # indeed사이트 검색결과의 페이지 개수를 알기위해 class명이 pagination인 div를 찾는고, anchor에서 'span'내에 있는 문자열을 찾아서 최대 page_number를 구한다
    pagination = soup.find("div", {"class":"pagination"})
    links = pagination.find_all("a")
    pages = []
    for link in links[:-1]:
      pages.append(int(link.find('span').string))
    max_page = pages[-1]
    return max_page
  except:
    print("INDEED_ERROR")
    return None

# 페이지별 요청 쿼리문

# 아래와 같은 하나의공고에서 타이틀, 회사명 뽑기
# <div class="jobsearch-SerpJobCard unifiedRow row result clickcard" id="p_b5b88516a299bbb2" data-jk="b5b88516a299bbb2" data-tn-component="organicJob">

# <h2 class="title">
# <a target="_blank" id="jl_b5b88516a299bbb2" href="/rc/clk?jk=b5b88516a299bbb2&amp;fccid=7009e9adee12ff99&amp;vjs=3" onmousedown="return rclk(this,jobmap[0],0);" onclick="setRefineByCookie([]); return rclk(this,jobmap[0],true,0);" rel="noopener nofollow" title="(주)신세계아이앤씨 경력사원 상시" class="jobtitle turnstileLink " data-tn-element="jobTitle">
# (주)신세계아이앤씨 경력사원 상시</a>

# </h2>
# ...(생략)
# </div>

def extract_job(html):
  # 클래스의 특성을 가져올때는 []를 사용
  title = html.find("h2", {"class":"title"}).find("a")["title"]
  company = html.find("span", {"class":"company"})
  location = html.find("div", {"class":"recJobLoc"})["data-rc-loc"]
  day = html.find("span", {"class":"date"}).string
  job_id = html["data-jk"].strip()
  link = f"{DETAIL_LINK}{job_id}"

  company_anchor = company.find("a")
  if company_anchor is not None:
    company = (str(company_anchor.string))
  else:
    company = (str(company.string))
  company = company.strip()
  return {
        'title':title,
        'company':company,
        'location':location,
        'day':day,
        'link':link
        }

def extract_jobs(last_page):
  jobs = []
  for page in range(last_page):
    result = requests.get(f"{URL}&start={page*LIMIT}")
    print(f"Scrapping indeed page{page} -> {result}")
    html = BeautifulSoup(result.text, 'html.parser')
    htmls = html.find_all("div", {"class":"jobsearch-SerpJobCard"})
    for html in htmls:
      job = extract_job(html)
      jobs.append(job)
  return jobs

# find_all : 찾은 내용의 모든 결과를 리스트로 반환
# find : 찾은 내용의 첫번째 결과를 반환

def get_jobs():
  last_page = extract_page()
  jobs = extract_jobs(last_page)
  return jobs