import requests
import os
from threading import Thread
import threading


# Lock = threading.Lock()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36 Edg/84.0.522.63',
    'Cookie': 'first_visit_datetime_pc=2023-06-19+19%3A30%3A47; p_ab_id=7; p_ab_id_2=2; p_ab_d_id=1092351479; _fbp=fb.1.1687170651382.1896136824; yuid_b=OXJzgHM; PHPSESSID=39211450_lSvwgFP92VwBrZ6OkAKqqkaZu5CHHMQQ; device_token=8ca113844dc0b65ec6e89ebe174ec9ee; _ga_MZ1NL4PHH0=GS1.1.1694609297.1.0.1694609300.0.0.0; c_type=21; privacy_policy_notification=0; a_type=0; b_type=0; _gid=GA1.2.86092035.1695553945; privacy_policy_agreement=6; QSI_S_ZN_5hF4My7Ad6VNNAi=v:0:0; first_visit_datetime=2023-09-24%2020%3A16%3A39; webp_available=1; login_ever=yes; _ga_75BBYNYN9J=GS1.1.1695553940.5.1.1695555284.0.0.0; cf_clearance=SmDqQYLlHsUj1OpS79K_SJfU6lK7LRkUiavJFgji6ho-1695555854-0-1-635f1c18.7b581fed.345e43f8-0.2.1695555854; _ga=GA1.2.1492906685.1687170650; __cf_bm=cjEX6RCBnxGLQTalZJrzth6X3PBGdcXc46U3nwWu4rI-1695555858-0-AYJsIjjE1C/9AUhrP7yV0ixIzKos3QxC29Y2wENRfhEqwg6VvsnpQZcTE4mEafR+0f2hn3dcUWs1+bI5hLEWoK9kutJt1bAJBG41rvY/GTEH; _ga_3WKBFJLFCP=GS1.1.1695554215.1.1.1695556040.0.0.0'
}


def download_img(url, referer, i, mode):  # 获取到图片url后定义个函数用于下载
    headers_download = {
        "referer": str(referer)
    }
    name = str(i) + '_' + url.split("/")[-1]  # 将图片链接以斜杠分割后取最后面的信息作为名字，因为爬取的图片有jeg也有png
    if os.path.exists(f"{mode}/{name}"):
        print(f'{name}存在', end='  ')
        return

    response = requests.get(url=url, headers=headers_download)  # print(url)
    with open(f"{mode}/{name}", "wb") as file:
        file.write(response.content)  # 将图片二进制数据存入，图片也就得到了


def crawler_ranking(url, page, mode):  # https://www.pixiv.net/ranking.php?mode=monthly_r18&p=1&format=json   # https://www.pixiv.net/bookmark_new_illust
    res = requests.get(url, headers=headers)
    datas = res.json()["contents"]  # print(datas)
    images_list = []
    for data in datas:
        image = {
            "title": data["title"],
            "user_name": data["user_name"],
            "p_id": data["illust_id"],
            "referer": f"https://www.pixiv.net/artworks/{data['illust_id']}"
        }
        images_list.append(image)  # print(images_list)

    for i in range(len(images_list)):
        image_1 = images_list[i]
        image_url = f"https://www.pixiv.net/ajax/illust/{image_1['p_id']}/pages?lang=zh"  # 通过以下链接，请求图片详情
        print({image_1['p_id']})
        image_data = requests.get(image_url, headers=headers).json()["body"]  # 数据保存在body字段        print(image_data)
        # Lock.acquire()
        for b in image_data:  # thumb_mini/small/regular/original
            t = Thread(target=download_img, args=(b['urls']['original'], image_1["referer"], page * 50 + i + 1, mode),
                       name=image_1['p_id'])
            t.start()  # 如果不加referer字段，直接请求下载链接p站不给结果
        print(f'第{page * 50 + i + 1}张正在下载')
        # Lock.release()


def crawler_users(url, mode):  # https://www.pixiv.net/ajax/user/23945843/profile/all?lang=zh
    res = requests.get(url, headers=headers)
    datas = res.json()["body"]  # print(datas["illusts"])

    images_list = list(datas["illusts"].keys())  # print(images_list)
    count = len(images_list)
    for i in range(len(images_list)):
        image_1 = images_list[i]
        Referer_ = f"https://www.pixiv.net/artworks/{image_1}"
        image_url = f"https://www.pixiv.net/ajax/illust/{image_1}/pages?lang=zh"  # 通过以下链接，请求图片详情
        image_data = requests.get(image_url, headers=headers).json()["body"]  # 数据保存在body字段        print(image_data)
        for b in image_data:  # thumb_mini/small/regular/original
            t = Thread(target=download_img, args=(b['urls']['original'], Referer_, count, mode),
                       name=image_1)
            t.start()  # 如果不加referer字段，直接请求下载链接p站不给结果
        count -= 1
        print(f'第{i + 1}张正在下载')


def crawler_latest(url, page, mode):#  https://www.pixiv.net/ajax/follow_latest/illust?p=1&mode=r18&lang=zh
    res = requests.get(url, headers=headers)
    datas = res.json()["body"]  # print(datas["illusts"])
    images_list = datas["page"]["ids"]  # print(images_list, len(images_list))

    for i in range(len(images_list)):
        image_1 = images_list[i]
        Referer_ = f"https://www.pixiv.net/artworks/{image_1}"
        image_url = f"https://www.pixiv.net/ajax/illust/{image_1}/pages?lang=zh"  # 通过以下链接，请求图片详情
        image_data = requests.get(image_url, headers=headers).json()["body"]  # 数据保存在body字段        print(image_data)
        for b in image_data:  # thumb_mini/small/regular/original
            t = Thread(target=download_img, args=(b['urls']['original'], Referer_, page * 60 + i + 1, mode),
                       name=image_1)
            t.start()  # 如果不加referer字段，直接请求下载链接p站不给结果
        print(f'第{page * 60 + i + 1}张正在下载')
