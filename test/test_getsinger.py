import requests
import json

def get_singer():
    urls = [
        ("国内", "https://apis.netstart.cn/music/toplist/artist?type=1"),
        ("欧美", "https://apis.netstart.cn/music/toplist/artist?type=2"),
        ("日本", "https://apis.netstart.cn/music/toplist/artist?type=4")
    ]

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    for region, url in urls:
        response = requests.get(url=url, headers=headers)
        js = json.loads(response.text)

        if js['code'] != 200:
            print(f"{region} 获取歌手列表失败")
            continue

        singer_data = []
        for item in js['list']['artists']:
            singer_data.append({
                'name': item['name'],
                'id': item['id']
            })

        with open(f'{region}_singers.json', 'w', encoding='utf-8') as f:
            json.dump(singer_data, f, ensure_ascii=False, indent=4)

        print(f"{region} 获取歌手列表成功并保存到 {region}_singers.json")

get_singer()
