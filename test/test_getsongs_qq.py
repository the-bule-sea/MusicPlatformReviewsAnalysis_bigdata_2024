# test_getsongs_qq.py
import os
import time
import requests
import json

def get_songs_from_singer_qq(singer_mid):
    url_template = (
        "https://u.y.qq.com/cgi-bin/musicu.fcg?data=%7B%22comm%22%3A%7B%22ct%22%3A24%2C%22cv%22%3A0%7D%2C%22singerSongList%22%3A%7B%22method%22%3A%22GetSingerSongList%22%2C%22param%22%3A%7B%22order%22%3A1%2C%22singerMid%22%3A%22{singer_mid}%22%2C%22begin%22%3A{begin}%2C%22num%22%3A{num}%7D%2C%22module%22%3A%22musichall.song_list_server%22%7D%7D"
    )
    url = url_template.format(singer_mid=singer_mid, begin=0, num=20)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"请求歌手 {singer_mid} 的歌曲列表失败")
        return []
    if not response.text:
        print(f"歌手 {singer_mid} 的歌曲列表为空")
        return []

    data = response.json()

    if data['code'] != 0 or data['singerSongList']['code'] != 0:
        print(f"获取歌手 {singer_mid} 的歌曲列表失败")
        return []

    songs = []
    for song in data['singerSongList']['data']['songList']:
        song_info = song['songInfo']
        songs.append({
            'name': song_info['name'],
            'id': song_info['id'],
            'mid': song_info['mid']
        })

    return songs

def get_songs_from_singers_qq(file_path, output_file):
    with open(file_path, 'r', encoding='utf-8') as f:
        singers = json.load(f)

    all_songs = []
    for singer in singers:
        singer_mid = singer['singer_mid']
        singer_name = singer['name']
        songs = get_songs_from_singer_qq(singer_mid)
        print(f"歌手 {singer_name} 的前20首歌曲信息已获取")
        for song in songs:
            all_songs.append({
                'singer_name': singer_name,
                'singer_mid': singer_mid,
                'song_name': song['name'],
                'song_id': song['id'],
                'song_mid': song['mid']
            })

    # 确保目录存在
    output_dir = '../../data'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(os.path.join(output_dir, output_file), 'w', encoding='utf-8') as f:
        json.dump(all_songs, f, ensure_ascii=False, indent=4)

    print(f"所有歌手的前20首歌曲信息已保存到 {output_file}")

if __name__ == "__main__":
    # 获取日本歌手的歌曲信息
    get_songs_from_singers_qq('日本_qqsingers.json', '日本_qqsongs.json')
    # 获取国内
    get_songs_from_singers_qq('国内_qqsingers.json', '国内_qqsongs.json')
    # 获取欧美
    get_songs_from_singers_qq('欧美_qqsingers.json', '欧美_qqsongs.json')
