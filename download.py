import requests
import os
from threading import Thread
import threading


# Lock = threading.Lock()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36 Edg/84.0.522.63',
    'Cookie': 'p_ab_id=5; p_ab_id_2=3; p_ab_d_id=878920109; device_token=da7c95eb7c24722f6ba5debc6cead49d; privacy_policy_agreement=6; first_visit_datetime=2023-09-24+20%3A38%3A44; webp_available=1; c_type=21; privacy_policy_notification=0; a_type=0; b_type=0; login_ever=yes; _fbp=fb.1.1695555532455.233515470; yuid_b=EjQWgpA; first_visit_datetime_pc=2023-09-24%2020%3A45%3A54; _ga_3WKBFJLFCP=GS1.1.1695555526.1.1.1695555952.0.0.0; _gcl_au=1.1.5439523.1695561924; PHPSESSID=39211450_8Tio5idt0qYi2DxCGkgDY9kiLoGmd2Ac; _ga_MZ1NL4PHH0=GS1.1.1695651333.2.0.1695651337.0.0.0; QSI_S_ZN_5hF4My7Ad6VNNAi=v:0:0; _gid=GA1.2.951869111.1697588916; _im_vid=01HD02ZE0PZ9JWGB7BYBMCHFTF; cto_bundle=uLU36l9LSmhFU25aNWlIYzNvSUQ2dnpSODJqZmRrT2NUY0JneUthTDglMkZudyUyRnNUQmpmT3MlMkI5amdtSFBmMTRrcmhBOU1yJTJCMmdiNFJKekZWZlBkc0U0eWE2UFhBeGwxazRIaXQlMkJHdEtSaFJPc25mdlN5bVRoNm1CaXJTRURaM0xSclpaZUtLNjhJdWwzYW9XbldGY0FYRUVtbThRJTNEJTNE; __cf_bm=nDfn9MJbTmniDCYH9Dm3S23uKvdIHtpE3sNN5_.6dK4-1697808524-0-AdLROS/G2QvL1iL+DARRarvpXlOXs1u1GpVkaq9bYzYfo8JrEZIzb0Rk+ywoMa3dK2CD/sByxkjthyxTKtnSnztHRLq3hPG5MyXcqPE1wSsQ; _ga=GA1.1.281923281.1695555401; _ga_75BBYNYN9J=GS1.1.1697808533.16.0.1697808533.0.0.0; cf_clearance=pDtOLPYGH5GgegCwCB9EZwy8988.IbLiuLCZMZR7NhQ-1697808547-0-1-9f89d693.e24f240a.c8888973-0.2.1697808547'
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
