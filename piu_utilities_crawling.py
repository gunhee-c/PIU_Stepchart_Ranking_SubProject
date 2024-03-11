import re
import requests
from bs4 import BeautifulSoup


#Request Soup 형성
def extractSoupfromURL(url):
    request = requests.get(url)
    soup = BeautifulSoup(request.text, 'html.parser')
    return request, soup

#해당 URL이 유효한지 판별
def check_valid_url(soup):
    if soup.find('div', {'class': "panel-heading bg bg-info"}):
        return True
    return False

#URL이 유효했는지 로그 남김
def printLog(log, url, isURLValid):
    if isURLValid:
        print(f'{url} is valid')
        log.append(f'{url} is valid')
    else:
        print(f'{url} is invalid')
        log.append(f'{url} is invalid')

#title/step_artist/levels/bpm/category/gametype 추출
def get_title(soup):
    title = soup.find('title').prettify()
    ans = title.replace("\t", "").replace("\n", "")
    return ans[17:-19]

def get_step_artist(soup):
    step_artist = r'bg-primary">(.*?)</span>'
    step_artist_list = re.findall(step_artist, str(soup))
    return step_artist_list

#need FIX
def get_levels(soup):
    levels = r'Levels/(.*?).png"'
    soup_partial = soup.find('div', class_='list-group-item')
    levels_list = re.findall(levels, str(soup_partial))
    ans = level_format_list(levels_list)
    return ans

def extract_before_slash(s):
    # Split the string by '/' and take the first element
    return s.split('/')[0]

def level_format(str):
    type = extract_before_slash(str)
    level = str[-2:]
    return f'{type}{level}'

def level_format_list(levels):
    ans = []
    for i in levels:
        new_item = level_format(i)
        ans.append(new_item)
    print(ans)
    return ans

def get_bpm(soup):
    span_text = soup.find('span', {'class': 'badge bg-info'}).text
    bpm = ''.join(filter(str.isdigit, span_text))
    return bpm

def get_category(soup):
    category = soup.find('span', {'class': 'badge bg-success pull-right'}).text
    return category

def get_gametype(soup):
    gametype = soup.find('span', {'class': 'badge bg-inverse pull-right'}).text
    return gametype

#metadata 추출 - 위 function들을 하나로 합침
def extract_metadata(soup):
    title = get_title(soup)
    step_artist_list = get_step_artist(soup)
    levels_list = get_levels(soup)
    bpm = get_bpm(soup)
    category = get_category(soup)
    gametype = get_gametype(soup)
    return title, step_artist_list, levels_list, bpm, category, gametype
    