import requests
import os
from threading import Thread
import threading


# Lock = threading.Lock()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36 Edg/84.0.522.63',
    'Cookie': ''
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


def download_img_1(url, referer, mode):  # 获取到图片url后定义个函数用于下载
    headers_download = {
        "referer": str(referer)
    }
    name = url.split("/")[-1]  # 将图片链接以斜杠分割后取最后面的信息作为名字，因为爬取的图片有jeg也有png
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

    for i in range(len(images_list)):
        image_1 = images_list[i]
        Referer_ = f"https://www.pixiv.net/artworks/{image_1}"
        image_url = f"https://www.pixiv.net/ajax/illust/{image_1}/pages?lang=zh"  # 通过以下链接，请求图片详情
        image_data = requests.get(image_url, headers=headers).json()["body"]  # 数据保存在body字段        print(image_data)
        for b in image_data:  # thumb_mini/small/regular/original
            t = Thread(target=download_img_1, args=(b['urls']['original'], Referer_, mode),
                       name=image_1)
            t.start()  # 如果不加referer字段，直接请求下载链接p站不给结果
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
            t = Thread(target=download_img_1, args=(b['urls']['original'], Referer_,  mode),
                       name=image_1)
            t.start()  # 如果不加referer字段，直接请求下载链接p站不给结果
        print(f'第{page * 60 + i + 1}张正在下载')
