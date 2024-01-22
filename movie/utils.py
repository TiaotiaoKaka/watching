import datetime

import requests


def header_generator(indexx, key=None):
    header = f"""#EXTM3U
#EXT-X-VERSION:3
#EXT-X-TARGETDURATION:10
#EXT-X-ALLOW-CACHE:YES
#EXT-X-MEDIA-SEQUENCE:{int(indexx)}
#EXT-X-PLAYLIST-TYPE:EVENT
"""
    if key:
        # header += """EXT-X-KEY:METHOD=AES-128,URI=\"https://v.gsuus.com/play/7ax76GBe/enc.key\""""
        header += key
    return header


def convert_to_live_m3u8(m3u8_text):
    ts_files = m3u8_text.split('\n')
    key = None
    ts_list = []

    # 写入每个TS文件，并添加EXTINF标签
    EXTINF = ''
    offsetTime = 0
    for i, ts_file in enumerate(ts_files):

        if not ts_file or ts_file.startswith('#'):  # 跳过空行和注释行
            if "#EXTINF" in ts_file:
                EXTINF = ts_file
            elif "#EXT-X-KEY" in ts_file:
                key = ts_file
                continue
            continue
        # 生成时间戳
        duration = EXTINF.split(':')[1].split(',')[0]
        offsetTime += int(duration.split('.')[0])
        timestamp = datetime.datetime.now() + datetime.timedelta(seconds=offsetTime)
        ts_list.append([EXTINF, ts_file, timestamp])
        EXTINF = ''
    content_list = []
    # 三片一组
    for i in range(0, len(ts_list), 3):
        content = header_generator(i / 3, key)
        for j in range(3):
            if i + j >= len(ts_list):
                break
            content += "\n" + ts_list[i + j][0] + "\n" + ts_list[i + j][1]
        content_list.append(content)
    return content_list


def get_m3u8_content(url):
    headers = {
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9',
        # 'origin': 'https://www.xigua29.com',
        # 'referer': 'https://www.xigua29.com/',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }

    response = requests.get(url, headers=headers)
    text = response.text
    # 去除url后缀
    root_url = url[:url.rfind('/') + 1]
    if 'enc.key' in text:
        # 正则匹配.key文件
        text = text.replace('enc.key', root_url + 'enc.key')
    return text


if __name__ == '__main__':
    content = get_m3u8_content('https://v.gsuus.com/play/QdJrnO2d/index.m3u8')
    convert_to_live_m3u8(content)
