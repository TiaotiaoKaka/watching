import json
import os.path
import re
import threading

from django.test import TestCase

# Create your tests here.


import requests
from bs4 import BeautifulSoup
import requests

proxies = {'https': 'http://127.0.0.1:4780'}


def search(kw, page=1):
    """
    搜索
    :return:
    """

    cookies = {
        'session': 'KVJ7dLPPv1QhQvEFjsMBQri21AOqzadDuywg2Omk',
        '_ga': 'GA1.1.214472288.1706841497',
        'locale': 'zh',
        'dom3ic8zudi28v8lr6fgphwffqoz0j6c': '9b330242-4867-40fd-837d-6248886be67a%3A3%3A1',
        'pp_idelay_a344ad3aa120e7b018b3813250fb1100': '1',
        '_ga_VZGC2QQBZ8': 'GS1.1.1706841497.1.1.1706843263.0.0.0',
        'x-token': '8758cf3b32ad1e1103db4b4616d7b804',
    }

    headers = {
        'authority': 'njav.tv',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'max-age=0',
        # 'cookie': 'session=KVJ7dLPPv1QhQvEFjsMBQri21AOqzadDuywg2Omk; _ga=GA1.1.214472288.1706841497; locale=zh; dom3ic8zudi28v8lr6fgphwffqoz0j6c=9b330242-4867-40fd-837d-6248886be67a%3A3%3A1; pp_idelay_a344ad3aa120e7b018b3813250fb1100=1; _ga_VZGC2QQBZ8=GS1.1.1706841497.1.1.1706843263.0.0.0; x-token=8758cf3b32ad1e1103db4b4616d7b804',
        'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    }

    search_list = []
    params = {
        'keyword': f'{kw}',
        'page': f'{page}',
    }

    response = requests.get('https://njav.tv/zh/search', params=params, cookies=cookies, headers=headers,
                            proxies=proxies)
    soup = BeautifulSoup(response.text, 'html.parser')
    tags = soup.find_all(class_='col-6 col-sm-4 col-lg-3')

    for tag in tags:
        item = tag.find("div", "thumb")
        favourite_tag = item.find("div", "favourite")
        vid = re.findall(r'(\d+),', favourite_tag['v-scope'])[0]
        img_tag = item.find('img')
        a_tag = item.find("a")
        image = img_tag.get('data-src')
        href = a_tag.get('href')
        title = a_tag.get('title')
        search_list.append({"image": image, "href": href, "title": title, "vid": vid})
    return search_list


def page_detail(**kwargs):
    """
    详情页
    :return:
    """
    url = f"https://njav.tv/zh/{kwargs.get('href')}"
    response = requests.get(url, proxies=proxies)
    soup = BeautifulSoup(response.text, 'html.parser')
    detail_tag = soup.find("div", class_="detail-item")
    type_value = detail_tag.find(class_="genre").text.replace("\n", "")
    iframe_src = soup.find("iframe").get("src")
    data = kwargs
    data.update({
        "type": type_value,
        "iframe_src": iframe_src
    })
    print(data)
    return data


def video_url(vid):
    cookies = {
        '_ga': 'GA1.1.214472288.1706841497',
        'dom3ic8zudi28v8lr6fgphwffqoz0j6c': '9b330242-4867-40fd-837d-6248886be67a%3A3%3A1',
        'locale': 'zh',
        'session': '3FqAkZDWAxG4jONNtHkqZ38enYCtXUqKGDEq3U5Z',
        'x-token': '0eac04957c4757886ce2d4fda4de6bf1',
        '_ga_VZGC2QQBZ8': 'GS1.1.1707040109.3.1.1707041469.0.0.0',
    }

    headers = {
        'authority': 'njav.tv',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        # 'cookie': '_ga=GA1.1.214472288.1706841497; dom3ic8zudi28v8lr6fgphwffqoz0j6c=9b330242-4867-40fd-837d-6248886be67a%3A3%3A1; locale=zh; session=3FqAkZDWAxG4jONNtHkqZ38enYCtXUqKGDEq3U5Z; x-token=0eac04957c4757886ce2d4fda4de6bf1; _ga_VZGC2QQBZ8=GS1.1.1707040109.3.1.1707041469.0.0.0',
        'referer': 'https://njav.tv/zh/v/hmn-476',
        'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    response = requests.get(f'https://njav.tv/zh/ajax/v/{vid}/videos', cookies=cookies, headers=headers,
                            proxies=proxies)
    return response.json()['data'][0]['url']


queryCache2 = {}
if os.path.exists(f'cache.json'):
    # 读取json文件
    with open(f'cache.json', 'r') as f:
        queryCache2 = json.loads(f.read())


def query2(kw, page=1):
    if queryCache2.get(f'{kw}_{page}'):
        return queryCache2.get(f'{kw}_{page}')
    seatch_list = search(kw, page)
    for item in seatch_list:
        play_url = video_url(item.get('vid'))
        # data = page_detail(**item)
        item['iframe_src'] = play_url
        # data_list.append(data)
    queryCache2[f'{kw}_{page}'] = seatch_list
    # 保存成json文件
    with open(f'cache.json', 'w') as f:
        f.write(json.dumps(queryCache2))
    return seatch_list

# if __name__ == '__main__':
#     data_list = []
#     seatch_list = search("高级")
#     tasks = []
#     for item in seatch_list:
#         play_url = video_url(item.get('vid'))
#         data = page_detail(**item)
#         data['iframe_src'] = play_url
#         data_list.append(data)
#     print(data_list)
