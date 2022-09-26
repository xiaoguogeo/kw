import json
import os
import requests

# 设置请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
                       Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.42',
    'Cookie': 'kw_token=HMRTU794L49',  # 设置cookie和csrf，否则会报错“CSRF Token Not Found”
    'csrf': 'HMRTU794L49'
}


# 获取音乐信息（获取rid）
def get_music_info(url):
    music_info_list = list()  # 用于存储音乐信息，里面存储字典类型的数据

    resp = requests.get(url, headers=headers).text

    resp = json.loads(resp)  # 此时的响应是字符串，将字符串转化为字典

    # 遍历列表，以生成音乐对象
    for music in resp['data']['musicList']:
        item = dict()
        item['name'] = music['name']
        item['artist'] = music['artist']
        item['rid'] = music['rid']
        music_info_list.append(item)  # 将音乐对象添加到列表中，方便遍历

    return music_info_list


# 拼接mid以获得音乐的url
def join_url(musicList):
    for music in musicList:
        mid = music['rid']
        url = f'http://www.kuwo.cn/api/v1/www/music/playUrl?mid={mid}&type=music&httpsStatus='

        music['url'] = url  # 往每一首音乐对象中添加上自己的地址


# 下载音乐
def download_music(musicList):
    print('\033[32m---------------下载开始---------------\033[0m\n')
    music_folder = 'music'

    for music in musicList:
        url = music['url']
        resp = requests.get(url, headers=headers).content  #获取音乐二进制内容

        artist = music['artist']
        music_name = music['name']
        music_file = music_name + '-' + artist + '.mp3'  #格式化为【音乐+歌手.mp3】格式

        print(f'正在下载 \033[34m{music_file}\033[0m ...')
        path = os.path.join(music_folder, music_file)  #将音乐文件放到“music”文件夹下
        with open(path, 'wb') as f:
            f.write(resp)

    print('\n\033[32m---------------下载完成---------------\033[0m')


# 执行爬虫
def exec_spider(url):
    # 判断是否存在名为“music”的文件夹，没有则新建一个
    if not os.path.exists('music'):
        os.mkdir('music')

    music_info_list = get_music_info(url)
    join_url(music_info_list)
    download_music(music_info_list)


if __name__ == '__main__':
    start_url = 'http://www.kuwo.cn/api/www/bang/bang/musicList?bangId=93&pn=1&rn=30&httpsStatus=1'
    exec_spider(start_url)
