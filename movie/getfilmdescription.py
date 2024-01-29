import asyncio
import time

import requests
from bs4 import BeautifulSoup
import re
import json
import aiohttp


async def getPageData(url):
    print('正在爬取：' + url)
    timestamp = int(round(time.time() * 1000))
    html = ''
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html = await response.text()

    print('爬取完成：' + url + '，耗时：' + str(int(round(time.time() * 1000)) - timestamp) + 'ms')
    soup = BeautifulSoup(html, 'html.parser')
    json_datas = pageProcess(soup)
    return json_datas


def getfilmdescription(film_Name):
    timestamp = int(round(time.time() * 1000))
    # 初次请求获取搜索页数 pages
    url = f'https://www.xigua29.com/search.php?page=1&searchword=={film_Name}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        ul_tag = soup.find('ul', class_='stui-page text-center clearfix')
        if ul_tag:
            hidden_xs_li_tags = ul_tag.find_all('li', class_='hidden-xs')
            pages = len(hidden_xs_li_tags)

            # 对每一页爬取内容，以数组->字典形式存入 list_json_datas
            list_json_datas = []
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            tasks = [
                loop.create_task(
                    getPageData(f'https://www.xigua29.com/search.php?page={i}&searchword=={film_Name}')
                )
                for i in range(1, pages + 1)
            ]
            loop.run_until_complete(asyncio.wait(tasks))
            for task in tasks:
                json_datas = task.result()
                list_json_datas.extend(json_datas)
            print('total time: ' + str(int(round(time.time() * 1000)) - timestamp) + 'ms')
            return list_json_datas
        else:
            return []
    else:
        print(f"请求失败，状态码: {response.status_code}")
        return []


def getplaym3u8(playpage_original_value):
    url = f'https://www.xigua29.com{playpage_original_value}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # 查找script 标签，并且文本内容包含 var now
        script_tags = soup.find_all('script', text=re.compile(r'var\s+now'))
        if script_tags:
            for script_tag in script_tags:
                m3u8_values = []
                # 使用正则表达式提取 now(m3u8) 的值
                match1 = re.search(r'var\s+now\s*=\s*"([^"]+)"', script_tag.string)
                match2 = re.search(r'var\s+next\s*=\s*"([^"]+)"', script_tag.string)
                if match1:
                    m3u8_value = match1.group(1)
                    m3u8_values.append(m3u8_value)
                else:
                    m3u8_values.append('')
                if match2:
                    m3u8_value = match2.group(1)
                    m3u8_values.append(m3u8_value)
                else:
                    m3u8_values.append('')
                return m3u8_values
        else:
            return None
    else:
        print(f"请求失败，状态码: {response.status_code}")
        return None


def pageProcess(soup):
    # 查找盒子内容
    ul_tag = soup.find('ul', class_='stui-vodlist__media col-pd clearfix')
    json_datas = []
    # 查找 ul 标签内所有 li 标签
    if ul_tag:
        li_tags = ul_tag.find_all('li')
        for li_tag in li_tags:
            json_data = []
            # 查找 li 标签内部的第一个 div 块
            thumb_div = li_tag.find('div', class_='thumb')
            # 获取 a 标签中的 data-original 属性值
            if thumb_div:
                a_tag = thumb_div.find('a')
                if a_tag and 'data-original' in a_tag.attrs:
                    data_original_value = a_tag['data-original']

            detail_div = li_tag.find('div', class_='detail')
            if detail_div:
                # 获取 h3 标签中的内容作为值，'title' 作为键
                h3_tag = detail_div.find('h3')
                title_value = h3_tag.text.strip() if h3_tag else ''
                # 获取较早出现的 p 标签中的内容作为值，'director' 作为键
                p_tags = detail_div.find_all('p')
                director_value = p_tags[0].text.strip() if p_tags else ''
                # 使用正则表达式提取以"导演："开头的部分
                match = re.search(r'导演：(.+)', director_value)
                # 提取结果，如果匹配成功，获取第一个捕获组的内容，否则为空字符串
                director_value = match.group(1) if match else ''
                # 获取第二个 p 标签中的所有 a 标签内的人名，用空格连接起来作为值，'actor' 作为键
                actor_value = ','.join([a.text.strip() for a in p_tags[1].find_all('a')]) if len(
                    p_tags[1].find_all('a')) > 1 else ''
                # 获取第3个 p 标签中的所有内容,使用列表索引逐项表示 'type'、'area'、'time' 作为键
                mix_value = ''.join([a.text.strip() for a in p_tags[2]]) if len(p_tags[2]) > 1 else ''
                # 使用正则表达式提取在"类型："和"地区："之间的内容
                match = re.search(r'类型：(.*?)地区：', mix_value)
                # 提取结果，如果匹配成功，获取第一个捕获组的内容，否则为空字符串
                type_value = match.group(1) if match else ''
                # 使用正则表达式提取在"地区："和"年份："之间的内容
                match = re.search(r'地区：(.*?)年份：', mix_value)
                # 提取结果，如果匹配成功，获取第一个捕获组的内容，否则为空字符串
                area_value = match.group(1) if match else ''
                # 使用正则表达式提取在"地区："之后的内容
                match = re.search(r'地区：(.+)', mix_value)
                # 提取结果，如果匹配成功，获取第一个捕获组的内容，否则为空字符串
                time_value = match.group(1) if match else ''
                # 获取第四个 p 标签内的第一个 a 标签，a标签的 href 属性为电影播放页面
                p_a_tag = p_tags[3].find('a')
                if p_a_tag and 'href' in p_a_tag.attrs:
                    playpage_original_value = p_a_tag['href']
                m3u8_values = getplaym3u8(playpage_original_value)
                json_data = {
                    'image': 'https://www.xigua29.com' + data_original_value,
                    'title': title_value,
                    'director': director_value,
                    'actor': actor_value,
                    'type': type_value,
                    'area': area_value,
                    'time': time_value,
                    'playpage': playpage_original_value,
                    'now': m3u8_values[0],
                    'next': m3u8_values[1]
                }
            json_datas.append(json_data)
        return json_datas
    else:
        # 没有资源,None用[]替代
        return []


def getLiNumber(url, headers):
    """
    获取剧集数量

    :param url:
    :param headers:
    :return:
    """
    try:
        url = 'https://www.xigua29.com' + url
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # 找到ul
        playlist_ul = soup.find('ul', class_='stui-content__playlist clearfix')
        if playlist_ul:
            # 统计数量li数量
            li_elements = playlist_ul.find_all('li')
            li_count = len(li_elements)
            return li_count
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None


def getSeriesMessage(url):  # 格式:url=/play/65110-0-0.html
    """
    获取剧集信息

    :param url:
    :return:
    """
    # 从url中获取集， 从0开始
    now_series = re.findall(r'-(\d+)\.html', url)[0]
    now_series = int(now_series)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    li_count = getLiNumber(url, headers)
    if li_count is None:
        print("没有剧集")
        return None
    json_data = []
    for i in range(li_count):
        # url_temp = str(url[:-6]) + str(i) + str(url[-5:])
        # m3u8_values = getplaym3u8(url_temp)
        json_temp = {
                'index': '第' + str(i + 1) + '集',
                'playpage': str(url[:-6]) + str(i) + str(url[-5:]),
                'selected': True if i == now_series else False
                # 'now': m3u8_values[0],
                # 'next': m3u8_values[1]
        }

        json_data.append(json_temp)
    return json_data


def parse_m3u8(m3u8_url):
    """
    解析m3u8文件，返回m3u8文件的内容
    :param m3u8_url: m3u8文件的url
    :return: m3u8文件的内容
    """
    m3u8_content = requests.get(m3u8_url).text
    if m3u8_content:
        return m3u8_content
    else:
        return None


if __name__ == '__main__':
    print(getSeriesMessage('/65110-0-0.html'))
    # parse_m3u8('https://v.gsuus.com/play/7ax76GBe/index.m3u8')
