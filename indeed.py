import requests
from bs4 import BeautifulSoup 
#https://www.crummy.com/software/BeautifulSoup/bs4/doc/
#soup method explation

# find_all : 찾은 내용의 모든 결과를 리스트로 반환
# find : 찾은 내용의 첫번째 결과를 반환
# 클래스의 특성을 가져올때는 []를 사용

LIMIT = 50
DETAIL_LINK = "https://kr.indeed.com/%EC%B1%84%EC%9A%A9%EB%B3%B4%EA%B8%B0?jk="

def extract_page(URL):
	try:
		result = requests.get(URL)
		soup = BeautifulSoup(result.text, 'html.parser')
		# indeed사이트 검색결과의 페이지 개수를 알기위해 class명이 pagination인 div를 찾는고,
		# anchor에서 'span'내에 있는 문자열을 찾아서 최대 page_number를 구한다
		pagination = soup.find("div", {"class":"pagination"})
		links = pagination.find_all("a")
		pages = []
		for link in links[:-1]:
			pages.append(int(link.find('span').string))
		max_page = pages[-1]
		return max_page
	except:
		print("NONE RESULT")
		return 0 

# 페이지별 요청 쿼리문
# 하나의공고에서 타이틀, 회사명 뽑기

def extract_job(html, word):
	title = html.find("h2", {"class":"title"}).find("a")["title"]
	company = html.find("span", {"class":"company"})
	location = html.find("div", {"class":"recJobLoc"})["data-rc-loc"]
	day = html.find("span", {"class":"date"}).string
	job_id = html["data-jk"].strip()
	link = f"{DETAIL_LINK}{job_id}"
	relative_skills = word

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
				'link':link,
				'relative_skills':relative_skills
				}

def extract_jobs(last_page, URL, word):
	jobs = []
	if last_page > 2:
    		last_page = 2;
	for page in range(last_page):
		result = requests.get(f"{URL}&start={page*LIMIT}")
		print(f"Scrapping indeed page{page} -> {result}")
		html = BeautifulSoup(result.text, 'html.parser')
		htmls = html.find_all("div", {"class":"jobsearch-SerpJobCard"})
		for html in htmls:
			job = extract_job(html, word)
			jobs.append(job)
	return jobs

def get_jobs(word):
	URL = f"https://kr.indeed.com/%EC%B7%A8%EC%97%85?q={word}& l=seoul&limit={LIMIT}"
	last_page = extract_page(URL)
	jobs = extract_jobs(last_page, URL, word)
	return jobs