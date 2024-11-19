# test_getsongs.py
import os
import time
import requests
import json

def get_songs_from_singer(singer_id):
    url = f"https://apis.netstart.cn/music/artists?id={singer_id}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"请求歌手 {singer_id} 的歌曲列表失败")
        return []
    if not response.text:
        print(f"歌手 {singer_id} 的歌曲列表为空")
        return []

    time.sleep(1)
    print(f"等待一秒，正在获取歌手信息")
    data = json.loads(response.text)

    if data['code'] != 200:
        print(f"获取歌手 {singer_id} 的歌曲列表失败")
        return []

    songs = []
    for song in data['hotSongs'][:20]:
        songs.append({
            'name': song['name'],
            'id': song['id']
        })

    return songs

def get_songs_from_singers(file_path, output_file):
    with open(file_path, 'r', encoding='utf-8') as f:
        singers = json.load(f)

    all_songs = []
    for singer in singers:
        singer_id = singer['id']
        songs = get_songs_from_singer(singer_id)
        print(f"歌手 {singer['name']} 的前20首歌曲信息已获取")
        for song in songs:
            all_songs.append({
                'singer_name': singer['name'],
                'singer_id': singer_id,
                'song_name': song['name'],
                'song_id': song['id']
            })

    # 确保目录存在
    output_dir = '../../data'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(os.path.join(output_dir, output_file), 'w', encoding='utf-8') as f:
        json.dump(all_songs, f, ensure_ascii=False, indent=4)

    print(f"所有歌手的前20首歌曲信息已保存到 {output_file}")

if __name__ == "__main__":
    # 获取欧美歌手的歌曲信息(爬过了)
    # get_songs_from_singers('欧美_singers.json', '欧美_songs.json')

    # 获取国内歌手的歌曲信息
    get_songs_from_singers('国内_singers.json', '国内_songs.json')
    time.sleep(60)
    # 获取日本歌手的歌曲信息
    get_songs_from_singers('日本_singers.json', '日本_songs.json')
