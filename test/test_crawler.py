# test_crawler.py
import requests
import json
import time
import os

headers = {
    'Host': 'music.163.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
}

def get_user(user_id):
    """
    获取用户注册时间
    """
    data = {}
    url = 'https://music.163.com/api/v1/user/detail/' + str(user_id)
    response = requests.get(url=url, headers=headers)
    # 将字符串转为json格式
    js = json.loads(response.text)
    if js['code'] == 200:
        # 性别
        data['gender'] = js['profile']['gender']
        # 年龄
        if int(js['profile']['birthday']) < 0:
            data['age'] = 0
        else:
            data['age'] = (2018 - 1970) - (int(js['profile']['birthday']) // (1000 * 365 * 24 * 3600))
        if int(data['age']) < 0:
            data['age'] = 0
        # 城市
        data['city'] = js['profile']['city']
        # 个人介绍
        data['sign'] = js['profile']['signature']
    else:
        data['gender'] = '无'
        data['age'] = '无'
        data['city'] = '无'
        data['sign'] = '无'
    return data

def get_comments(song_id, page):
    """
    获取评论信息
    """
    url = f'http://music.163.com/api/v1/resource/comments/R_SO_4_{song_id}?limit=100&offset={page}'
    response = requests.get(url=url, headers=headers)
    # 将字符串转为json格式
    result = json.loads(response.text)
    items = result['comments']
    time.sleep(1)
    for item in items:
        # 用户名
        user_name = item['user']['nickname'].replace(',', '，')
        # 用户ID
        user_id = str(item['user']['userId'])
        # 获取用户信息
        user_message = get_user(user_id)
        # 用户年龄
        user_age = str(user_message['age'])
        # 用户性别
        user_gender = str(user_message['gender'])
        # 用户所在地区
        user_city = str(user_message['city'])
        # 个人介绍
        user_introduce = user_message['sign'].strip().replace('\n', '').replace(',', '，')
        # 评论内容
        comment = item['content'].strip().replace('\n', '').replace(',', '，')
        # 评论ID
        comment_id = str(item['commentId'])
        # 评论点赞数
        praise = str(item['likedCount'])
        # 评论时间
        date = time.localtime(int(str(item['time'])[:10]))
        date = time.strftime("%Y-%m-%d %H:%M:%S", date)
        print(user_name, user_id, user_age, user_gender, user_city, user_introduce, comment, comment_id, praise, date)

        return user_name, user_id, user_age, user_gender, user_city, user_introduce, comment, comment_id, praise, date

def save_comments_to_csv(comments, file_path):
    with open(file_path, 'a', encoding='utf-8-sig') as f:
        for comment in comments:
            f.write(','.join(comment) + '\n')

def main():
    regions = ['欧美', '国内', '日本']
    for region in regions:
        input_file = f'{region}_songs.json'
        output_file = f'{region}_music_comments.csv'

        # 确保目录存在
        output_dir = '../../data'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        with open(input_file, 'r', encoding='utf-8') as f:
            songs = json.load(f)

        with open(os.path.join(output_dir, output_file), 'w', encoding='utf-8-sig') as f:
            f.write('user_name,user_id,user_age,user_gender,user_city,user_introduce,comment,comment_id,praise,date\n')

        for song in songs:
            song_id = song['song_id']
            print(f'正在获取歌曲 {song["song_name"]} ({song_id}) 的评论')
            comments = []
            for page in range(0, 1060, 20):
                print(f'\n---------------第 {page // 20 + 1} 页---------------')
                try:
                    comment_data = get_comments(song_id, page)
                    comments.append(comment_data)
                except Exception as e:
                    print(f'获取评论失败: {e}')
                    break
            save_comments_to_csv(comments, os.path.join(output_dir, output_file))
            time.sleep(60)  # 每次获取完一首歌的评论后暂停60秒

if __name__ == '__main__':
    main()
