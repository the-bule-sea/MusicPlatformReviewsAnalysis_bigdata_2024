import requests
import json
import time
import os
import random

# User-Agent池
user_agent_pool = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]

headers = {
    'User-Agent': random.choice(user_agent_pool)
}

def get_comments_qq(song_id, page, proxies):
    """
    获取QQ音乐评论信息
    """
    url = f'https://c.y.qq.com/base/fcgi-bin/fcg_global_comment_h5.fcg?biztype=1&topid={song_id}&cmd=8&pagenum={page}&pagesize=25'
    # 随机挑选代理ip
    proxy = random.choice(proxies)
    proxy_dict = {
        'http': f'http://{proxy}',
        'https': f'http://{proxy}'
    }

    response = requests.get(url=url, headers=headers, proxies=proxy_dict)
    if response.status_code != 200:
        print(f"请求歌曲 {song_id} 的评论失败")
        return []

    data = response.json()
    if data['code'] != 0:
        print(f"获取歌曲 {song_id} 的评论失败")
        return []

    comments = []
    time.sleep(1)
    for comment_type in ['comment', 'hot_comment']:
        if comment_type in data and 'commentlist' in data[comment_type]:
            for item in data[comment_type]['commentlist']:
                # 检查是否存在 rootcommentnick
                if 'rootcommentnick' not in item:
                    continue

                # 评论ID
                comment_id = item['commentid']
                # 评论用户
                comment_user = item['rootcommentnick'].replace('@', '').strip().replace('\n', '').replace(',', '，')
                # 评论内容
                comment_content = item['rootcommentcontent'].replace('@', '').strip().replace('\n', '').replace(',', '，')
                # 点赞数
                praise = str(item['praisenum'])
                # 评论时间
                date = time.localtime(int(item['time']))
                date = time.strftime("%Y-%m-%d %H:%M:%S", date)
                comments.append((comment_id, comment_user, comment_content, praise, date))
                print((comment_id, comment_user, comment_content, praise, date))
    return comments

def save_comments_to_csv(comments, file_path):
    with open(file_path, 'a', encoding='utf-8-sig') as f:
        for comment in comments:
            f.write(','.join(comment) + '\n')

def load_proxies(proxy_file_path):
    with open(proxy_file_path, 'r') as f:
        proxies = [line.strip() for line in f.readline()]
    return proxies

def main():
    regions = ['日本2','国内2','欧美2']
    #  加载ip池
    proxy_file_path = 'proxy.txt'
    proxies = load_proxies(proxy_file_path)

    for region in regions:
        input_file = f'{region}_qqsongs.json'
        output_file = f'{region}_qq_music_comments.csv'

        # 确保目录存在
        output_dir = '../../data'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # 构建完整的输入文件路径
        input_file_path = os.path.join(output_dir, input_file)

        with open(input_file_path, 'r', encoding='utf-8') as f:
            songs = json.load(f)

        with open(os.path.join(output_dir, output_file), 'w', encoding='utf-8-sig') as f:
            f.write('comment_id,comment_user,comment_content,praise,date\n')

        for song in songs:
            song_id = song['song_id']
            print(f'正在获取歌曲 {song["song_name"]} ({song_id}) 的评论')
            all_comments = []
            for page in range(0, 41):
                print(f'\n---------------第 {page} 页---------------')
                try:
                    comments = get_comments_qq(song_id, page, proxies)
                    all_comments.extend(comments)
                except Exception as e:
                    print(f'获取评论失败: {e}')
                    break
            save_comments_to_csv(all_comments, os.path.join(output_dir, output_file))
            time.sleep(1)

if __name__ == '__main__':
    main()
