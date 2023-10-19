from download import *


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36 Edg/84.0.522.63',
    'Cookie': ''
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
                crawler_latest(url, i, mode)

        else:
            print('输入错误，请输入 1, 2 or 3')
            continue
        break
    print('下载完成')

# https://www.pixiv.net/artworks/92691155
