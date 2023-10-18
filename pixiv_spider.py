import requests
import os
from download import *


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36 Edg/84.0.522.63',
    'Cookie': 'first_visit_datetime_pc=2023-06-19+19%3A30%3A47; p_ab_id=7; p_ab_id_2=2; p_ab_d_id=1092351479; _fbp=fb.1.1687170651382.1896136824; yuid_b=OXJzgHM; PHPSESSID=39211450_lSvwgFP92VwBrZ6OkAKqqkaZu5CHHMQQ; device_token=8ca113844dc0b65ec6e89ebe174ec9ee; _ga_MZ1NL4PHH0=GS1.1.1694609297.1.0.1694609300.0.0.0; c_type=21; privacy_policy_notification=0; a_type=0; b_type=0; _gid=GA1.2.86092035.1695553945; privacy_policy_agreement=6; QSI_S_ZN_5hF4My7Ad6VNNAi=v:0:0; first_visit_datetime=2023-09-24%2020%3A16%3A39; webp_available=1; login_ever=yes; _ga_75BBYNYN9J=GS1.1.1695553940.5.1.1695555284.0.0.0; cf_clearance=SmDqQYLlHsUj1OpS79K_SJfU6lK7LRkUiavJFgji6ho-1695555854-0-1-635f1c18.7b581fed.345e43f8-0.2.1695555854; _ga=GA1.2.1492906685.1687170650; __cf_bm=cjEX6RCBnxGLQTalZJrzth6X3PBGdcXc46U3nwWu4rI-1695555858-0-AYJsIjjE1C/9AUhrP7yV0ixIzKos3QxC29Y2wENRfhEqwg6VvsnpQZcTE4mEafR+0f2hn3dcUWs1+bI5hLEWoK9kutJt1bAJBG41rvY/GTEH; _ga_3WKBFJLFCP=GS1.1.1695554215.1.1.1695556040.0.0.0'
}


if __name__ == "__main__":
    print('''1.下载排行榜(日/周/月榜)
2.下载画师主页
3.下载个人主页最近更新''')

    url = 'https://www.pixiv.net/'
    while True:
        choice = input('请输入想要下载的模式：')
        if choice == '1':   # https://www.pixiv.net/ranking.php?mode=monthly&p=1&format=json
            print('输入下载的模式: daily / daily_r18 / weekly / weekly_r18 / monthly')
            mode = input('输入上面的选项之一:')
            if not os.path.exists(mode):
                os.makedirs(mode)
            page = int(input('输入想要下载的页数(50张为一页):'))
            for i in range(page):
                url += f"ranking.php?mode={mode}&p={i+1}&format=json"
                crawler_ranking(url, i, mode)

        elif choice == '2':   # https://www.pixiv.net/ajax/user/23945843/profile/all?lang=zh
            num = input('输入作者主页号:')
            mode = 'user' + num
            if not os.path.exists(mode):
                os.makedirs(mode)
            url += 'ajax/user/' + num + '/profile/all?lang=zh'
            crawler_users(url, mode)

        elif choice == '3':   # https://www.pixiv.net/ajax/follow_latest/illust?lang=zh&mode=r18&p=1
            num = int(input('是否只下载r18(否输入0 是输入1)'))
            page = int(input('输入想要下载的页数(60张为一页):'))
            mode = 'latest'
            url += 'ajax/follow_latest/illust?lang=zh'
            if num:
                url += '&mode=r18'
                mode += '_r18'
            if not os.path.exists(mode):
                os.makedirs(mode)
            for i in range(page):
                url += f"&p={i+1}"
                print(url)
                crawler_latest(url, i, mode)

        else:
            print('输入错误，请输入 1, 2 or 3')
            continue
        break
    print('下载完成')

# https://www.pixiv.net/artworks/92691155
