import re
import requests
from bs4 import BeautifulSoup
from piu_series_comparator import *
#title, bpm, category, gametype, levels_list, level_history_list, step_artist_list, version_list, version_detail_list

class SongData:
    def __init__(self, title, composers, bpm, category, gametype, length):
        self.title = title
        self.composers = composers
        self.bpm = bpm
        self.category = category
        self.gametype = gametype
        self.version = "N/A"
        self.version_detail = "N/A"
        self.length = length
        self.chartInfo = []

    def set_version(self, version, version_detail):
        self.version = version
        self.version_detail = version_detail

    def set_chartInfo(self, level_list, level_history_list, step_artist_list, version_list, version_detail_list, tags_list):
        for i in range(len(level_list)):
            chartInfo = ChartInfo(level_list[i], level_history_list[i], step_artist_list[i], version_list[i], version_detail_list[i], tags_list[i])
            self.chartInfo.append(chartInfo)

    def set_length(self, length):
        self.length = length

    def find_init_version(version, version_detail):

        return version, version_detail

    def append_chartInfo(self, chartInfo):
        self.chartInfo.append(chartInfo)

    def chartInfo_to_string(self):
        str = ""
        for i in range(self.length):
            str += (str(self.chartInfo[i]))
        return str
    
    def __str__(self):
        return f'title: {self.title}, composer: {self.composers}, bpm: {self.bpm}, \
        category: {self.category}, gametype: {self.gametype}, \
        version: {self.version}, version_detail: {self.version_detail}\nstep info:\n{self.chartInfo_to_string()}\n'

    def __repr__(self):
        return f'title: {self.title}, composer: {self.composers}, bpm: {self.bpm}, \
        category: {self.category}, gametype: {self.gametype}, \
        version: {self.version}, version_detail: {self.version_detail}\nstep info:\n{self.chartInfo_to_string()}\n'

    def modify_chartInfo(self, index, chartInfo):
        pass

    def delete_chartInfo(self, index):
        pass
    

class ChartInfo:
    def __init__(self, level, level_history, step_artist, version, version_detail, tags):
        self.level = level
        self.level_history = level_history
        self.step_artist = step_artist
        self.version = version
        self.version_detail = version_detail
        self.tags = tags

    def __str__(self):
        return f'level: {self.level}, level_history: {self.level_history}, step_artist: {self.step_artist}, version: {self.version}, version_detail: {self.version_detail}, tags: {self.tags}'

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

def delete_tabs_and_newlines(text):
    return text.replace("\t", "").replace("\n", "").strip()

#title/step_artist/levels/bpm/category/gametype 추출
def get_title(soup):
    title = soup.find('title').prettify()
    ans = title.replace("\t", "").replace("\n", "")
    print("## " + ans[17:-19] + " ##")
    return ans[17:-19]

def get_step_artist(soup):
    step_artist = r'"label bg-primary">(.*?)</span>'
    step_artist_list = re.findall(step_artist, str(soup))
    print(f'step_artist_list: {step_artist_list}')
    print(f'len(step_artist_list): {len(step_artist_list)}')
    return step_artist_list

#need FIX
def get_levels(soup):
    levels = r'Levels/(.*?).png"'
    soup_partial = soup.find('div', class_='list-group-item')
    levels_list = re.findall(levels, str(soup_partial))
    ans = level_format_list(levels_list)
    print(f'levels_list: {ans}')
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
    return ans

def get_bpm(soup):

    span_text = soup.find('span', {'class': 'badge bg-info'}).text
    bpm = ''.join(filter(str.isdigit, span_text))
    print('bpm:', bpm)
    return bpm

def get_category(soup):
    category = soup.find('span', {'class': 'badge bg-success pull-right'}).text
    category = delete_tabs_and_newlines(category)
    print(f'category: {category}')
    return category

def get_gametype(soup):
    gametype = soup.find('span', {'class': 'badge bg-inverse pull-right'}).text
    gametype = delete_tabs_and_newlines(gametype)
    print(f'gametype: {gametype}')
    return gametype

def get_composer(soup):
    pattern = re.compile('chart-item-container--\d+') #chart-item-container--1
    target_div2 = soup.find('div', class_='media', id=pattern).find('div', class_='media-body').find_all('span', class_ = "label bg-primary")
    for i in range(len(target_div2)):
        target_div2[i] = target_div2[i].text.strip()
    return target_div2

def level_format(str):
    parts = str.split("Levels/")
    substring_after_levels = parts[1] if len(parts) > 1 else None
    substring_after_levels = extract_before_slash(substring_after_levels)
    if str[-8:-6] == "sp":
        level = "??"
    else:
        level = str[-6:-4]
    return f'{substring_after_levels}{level}'

def parse_version_and_detail(str):
    parts = str.split(" - ")
    if len(parts) != 2:
        return "ERROR", "ERROR"
    else:
        return parts[0].strip(), parts[1].strip()

def parse_stepLV_artist_version_tag(sample):
    
    img_elements = sample.find_all('img')

    level = level_format(img_elements[0]['src'])
    #print(level)
    level_history = []
    step_artist_list = []

    for item in img_elements[1:]:
        level_history.append(level_format(item['src']))
    #print(level_history)

    step_artist_list = sample.find_all('span', {'class': 'label bg-primary'})
    for index in range(len(step_artist_list)):
        step_artist_list[index] = step_artist_list[index].text.strip()
    version, version_detail = parse_version_and_detail(sample.find('span', {'class': 'label bg-info'}).text.strip())
    #print(step_artist_list, version, version_detail)
    
    tags = sample.find_all('span', {'class': 'label bg-inverse'})
    for i in range(len(tags)):
        tags[i] = tags[i].text.strip()

    return level, level_history, step_artist_list, version, version_detail, tags

#metadata 추출 - 위 function들을 하나로 합침
def extract_metadata_legacy(soup):
    title = get_title(soup)
    step_artist_list = get_step_artist(soup)
    levels_list = get_levels(soup)
    bpm = get_bpm(soup)
    category = get_category(soup)
    gametype = get_gametype(soup)
    return title, step_artist_list, levels_list, bpm, category, gametype


def extract_metadata(soup):
    print("New Gangsta")

    title, composers, bpm, category, gametype = extract_songdata(soup)

    data = SongData(title, composers, bpm, category, gametype, 0)

    print("Fine Here")
    levels_list, level_history_list, step_artist_list, version_list, version_detail_list, tags_list = extract_chartdata(soup)

    init_version, init_version_detail = find_earliest_version(version_list, version_detail_list) 
    data.set_version(init_version, init_version_detail)
    print("Fine THere")
    
    length = len(levels_list)
    data.set_length(length)  
    data.set_chartInfo(levels_list, level_history_list, step_artist_list, version_list, version_detail_list, tags_list)
    print("Fine Everywhere")
    
    return data

def extract_songdata(soup):
    title = get_title(soup)
    composers = get_composer(soup)
    bpm = get_bpm(soup)
    category = get_category(soup)
    gametype = get_gametype(soup)   
    return title, composers, bpm, category, gametype 

def extract_chartdata(soup):
    levels_list, level_history_list, step_artist_list, version_list, version_detail_list, tags_list = [], [], [], [], [], []
    chart_div = soup.find('div', class_='col-lg-6').find('section', class_='panel').find('div', class_='list-group').find_all('div', class_="media")
    for item in chart_div:
        level, level_history, step_artists, version, version_detail, tags = parse_stepLV_artist_version_tag(item)
        levels_list.append(level)
        level_history_list.append(level_history)
        step_artist_list.append(step_artists)
        version_list.append(version)
        version_detail_list.append(version_detail)
        tags_list.append(tags)
    return levels_list, level_history_list, step_artist_list, version_list, version_detail_list, tags_list