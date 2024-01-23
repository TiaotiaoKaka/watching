from django.test import TestCase

# Create your tests here.


import requests
headers = {
        'authority': 'missav.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'max-age=0',
        'if-modified-since': 'Tue, 23 Jan 2024 02:46:11 GMT',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }
proxies = {'https': 'http://127.0.0.1:4780'}
def search():
    """
    搜索
    :return:
    """
    params = {
        'frontend_timestamp': '1705988044',
        'frontend_sign': '24e2daf9138b9c3d2bdeaf2f9f9f3299e6b6c247',
    }

    json_data = {
        'searchQuery': '巨乳,小只,无码',
        'count': 24,
        'scenario': 'search',
        'returnProperties': True,
        'includedProperties': [
            'title_zh',
            'duration',
            'has_chinese_subtitle',
            'is_uncensored_leak',
            'dm',
        ],
        'cascadeCreate': True,
    }
    # 获取系统代理

    response = requests.post(
        'https://client-rapi-missav.recombee.com/missav-default/search/users/16cf8e23-4f94-4616-9d3c-1faa1aa8fab5/items/',
        params=params,
        headers=headers,
        json=json_data,
        proxies=proxies
    )
    return response.json()


def page():
    import requests

    cookies = {
        'user_uuid': '16cf8e23-4f94-4616-9d3c-1faa1aa8fab5',
        '_ga': 'GA1.1.1923847188.1675859058',
        'dom3ic8zudi28v8lr6fgphwffqoz0j6c': '9b330242-4867-40fd-837d-6248886be67a%3A3%3A1',
        'cf_clearance': 'taGNzXBbm0f.Lzdky96gnCRo4Y37Fh2pEGp5MXrcYVE-1705987977-1-AdUtKyqf94aWZRt/iXbJKfj+cN42q6JGhFHwcHh1qcp5ApxFvauyEJvfvfdqhk7F/UUTOm7/QRVcxlfLhpYdgLU=',
        'sb_main_62bdca270715b3b43fbac98597c038f1': '1',
        'search_history': '[%22%25E5%25B7%25A8%25E4%25B9%25B3%252C%25E5%25B0%258F%25E5%258F%25AA%252C%25E6%2597%25A0%25E7%25A0%2581%22%2C%22spay230%22%2C%22spay300%22%2C%22spay%22%2C%22spra%22]',
        'sb_page_62bdca270715b3b43fbac98597c038f1': '2',
        'sb_count_62bdca270715b3b43fbac98597c038f1': '2',
        'sb_onpage_62bdca270715b3b43fbac98597c038f1': '1',
        'XSRF-TOKEN': 'eyJpdiI6IlZXa0RHL2hBam0zMUdzMkJ3ZG0rRFE9PSIsInZhbHVlIjoialV0V3FPOVFRTGtMaFF0c0hhWTBsM2Fwb2pvbmVRdUE4TU1hV3E4b1RHOG04cXpwcXpBSnE5VEU0eXVTV1k0dWQ1cTVOWEdVRmRjem9qc01PUjl0MExsRXJYU29HeEF2ZU5XVUQ2Mjk2ejJEVjBuYml2cTF1N0ZBRWI1MVR2VnUiLCJtYWMiOiIxMjYyNGNmMTVmZWRlOTllMDU5OTMyYjRiMDUyNGUzNzA2MmIwMDU2M2I1Y2FiMjgzY2NlY2I5NTNkMTU1YzYzIiwidGFnIjoiIn0%3D',
        'missav_session': 'eyJpdiI6Ik5sRjVYazlXVFh1WnJ1R045UitYYXc9PSIsInZhbHVlIjoiZ0NFbGNuUHZQajNvL1ZsRjZWYU8xa0ZScHEzZzlYK2V0RXR5QkN2amt2Zklza2pYNUExNWNHZi9xT2xWRHc3eXBNa05UclhRdmF4V25QQkxaZmtXRGcyZEFMa0RLQkhUYXJIMWRzd3pLeDNzaHFXTk1QMnp5M0dzTENJSEdjdFkiLCJtYWMiOiIzZDMzMDBiOGY0YjhlZGZjMWM3NGY1OGY5YTkxN2ZiYmQzZjE4NzA2OTBjYjFiODhhMTc1NWI2MGFkY2RmNmU4IiwidGFnIjoiIn0%3D',
        'JAqUW5LRfMTVDbEcZGKMUjAVv0PDOs4CxhkLJKPT': 'eyJpdiI6ImxIUzRKWlpLTEYrZkRid0tSNFZFYnc9PSIsInZhbHVlIjoieW9XdEpJZDRxbnRZc2VSZXY1R1VBRU0yTHRDaWNkUyswcGVWRE4vY1VTODNUblo4djNaRnVieUszVitZN3VXZGNzT2lkWXA2c29xcnNXMCtYN0o1Y2lWOW1OUFRkQlFicTRYYUFURzQ3Nm1uOWdYYWQwRVozWk5yY2hTVUJRcm5USGdoL3JNYUdBbFZBK2FwZVZxWHVPME4xNHVJaFNOL0RxSVZDckdpTnRUMlVlb3lLL3pmQWlpdmRDdEZkdVpVTnNjN05wMDdiL2dBeEVQQ2N5cEVPeUNBSWR2RXdpT0RndVZwUmhlTWdzT1lmOU4xSTRMRC9QVFpyK0RWcEZjVXVtblo3Q2NrK2xQSFFuclkrMG1LRVFwYUFES2lBVTk4d3A3K3Q4VWQ2b3U0TkhwRU9meTlXVWhMbm56OWtWRTQwSUErTk5MYndKRVo4VkcrUGtyei9UQmpraEl1U3NzcFRRRWFaUjA2YjAyVzVHaHdORXJ3Vk1oMVhKUzk4NUM2bU9rWmNJcDB2bVNtMnNDV25OY0ZtQT09IiwibWFjIjoiZThhY2ZkMWI4NDZhNjFjOTBiM2I4NDAzYTAyYzM2OTFmNWVmNzA2M2U3MTA2YzlmOTg4Y2I2MmQ3ZTc5ZGUzNiIsInRhZyI6IiJ9',
        '_ga_Z3V6T9VBM6': 'GS1.1.1705987979.8.1.1705988838.0.0.0',
    }

    headers = {
        'authority': 'missav.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'max-age=0',
        # 'cookie': 'user_uuid=16cf8e23-4f94-4616-9d3c-1faa1aa8fab5; _ga=GA1.1.1923847188.1675859058; dom3ic8zudi28v8lr6fgphwffqoz0j6c=9b330242-4867-40fd-837d-6248886be67a%3A3%3A1; cf_clearance=taGNzXBbm0f.Lzdky96gnCRo4Y37Fh2pEGp5MXrcYVE-1705987977-1-AdUtKyqf94aWZRt/iXbJKfj+cN42q6JGhFHwcHh1qcp5ApxFvauyEJvfvfdqhk7F/UUTOm7/QRVcxlfLhpYdgLU=; sb_main_62bdca270715b3b43fbac98597c038f1=1; search_history=[%22%25E5%25B7%25A8%25E4%25B9%25B3%252C%25E5%25B0%258F%25E5%258F%25AA%252C%25E6%2597%25A0%25E7%25A0%2581%22%2C%22spay230%22%2C%22spay300%22%2C%22spay%22%2C%22spra%22]; sb_page_62bdca270715b3b43fbac98597c038f1=2; sb_count_62bdca270715b3b43fbac98597c038f1=2; sb_onpage_62bdca270715b3b43fbac98597c038f1=1; XSRF-TOKEN=eyJpdiI6IlZXa0RHL2hBam0zMUdzMkJ3ZG0rRFE9PSIsInZhbHVlIjoialV0V3FPOVFRTGtMaFF0c0hhWTBsM2Fwb2pvbmVRdUE4TU1hV3E4b1RHOG04cXpwcXpBSnE5VEU0eXVTV1k0dWQ1cTVOWEdVRmRjem9qc01PUjl0MExsRXJYU29HeEF2ZU5XVUQ2Mjk2ejJEVjBuYml2cTF1N0ZBRWI1MVR2VnUiLCJtYWMiOiIxMjYyNGNmMTVmZWRlOTllMDU5OTMyYjRiMDUyNGUzNzA2MmIwMDU2M2I1Y2FiMjgzY2NlY2I5NTNkMTU1YzYzIiwidGFnIjoiIn0%3D; missav_session=eyJpdiI6Ik5sRjVYazlXVFh1WnJ1R045UitYYXc9PSIsInZhbHVlIjoiZ0NFbGNuUHZQajNvL1ZsRjZWYU8xa0ZScHEzZzlYK2V0RXR5QkN2amt2Zklza2pYNUExNWNHZi9xT2xWRHc3eXBNa05UclhRdmF4V25QQkxaZmtXRGcyZEFMa0RLQkhUYXJIMWRzd3pLeDNzaHFXTk1QMnp5M0dzTENJSEdjdFkiLCJtYWMiOiIzZDMzMDBiOGY0YjhlZGZjMWM3NGY1OGY5YTkxN2ZiYmQzZjE4NzA2OTBjYjFiODhhMTc1NWI2MGFkY2RmNmU4IiwidGFnIjoiIn0%3D; JAqUW5LRfMTVDbEcZGKMUjAVv0PDOs4CxhkLJKPT=eyJpdiI6ImxIUzRKWlpLTEYrZkRid0tSNFZFYnc9PSIsInZhbHVlIjoieW9XdEpJZDRxbnRZc2VSZXY1R1VBRU0yTHRDaWNkUyswcGVWRE4vY1VTODNUblo4djNaRnVieUszVitZN3VXZGNzT2lkWXA2c29xcnNXMCtYN0o1Y2lWOW1OUFRkQlFicTRYYUFURzQ3Nm1uOWdYYWQwRVozWk5yY2hTVUJRcm5USGdoL3JNYUdBbFZBK2FwZVZxWHVPME4xNHVJaFNOL0RxSVZDckdpTnRUMlVlb3lLL3pmQWlpdmRDdEZkdVpVTnNjN05wMDdiL2dBeEVQQ2N5cEVPeUNBSWR2RXdpT0RndVZwUmhlTWdzT1lmOU4xSTRMRC9QVFpyK0RWcEZjVXVtblo3Q2NrK2xQSFFuclkrMG1LRVFwYUFES2lBVTk4d3A3K3Q4VWQ2b3U0TkhwRU9meTlXVWhMbm56OWtWRTQwSUErTk5MYndKRVo4VkcrUGtyei9UQmpraEl1U3NzcFRRRWFaUjA2YjAyVzVHaHdORXJ3Vk1oMVhKUzk4NUM2bU9rWmNJcDB2bVNtMnNDV25OY0ZtQT09IiwibWFjIjoiZThhY2ZkMWI4NDZhNjFjOTBiM2I4NDAzYTAyYzM2OTFmNWVmNzA2M2U3MTA2YzlmOTg4Y2I2MmQ3ZTc5ZGUzNiIsInRhZyI6IiJ9; _ga_Z3V6T9VBM6=GS1.1.1705987979.8.1.1705988838.0.0.0',
        'if-modified-since': 'Tue, 23 Jan 2024 02:46:11 GMT',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }

    response = requests.get('https://missav.com/gesy-013', cookies=cookies, proxies=proxies, headers=headers)
    print(response.text)

if __name__ == '__main__':
    # json_data = search()
    # print(json_data)
    page()
