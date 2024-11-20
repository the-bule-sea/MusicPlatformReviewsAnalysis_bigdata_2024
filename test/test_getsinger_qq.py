import requests
import json

# 定义API URL模板
API_URL = "https://u.y.qq.com/cgi-bin/musicu.fcg?data={}"

# 定义请求参数
params = {
    "comm": {"ct": 24, "cv": 0},
    "singerList": {
        "module": "Music.SingerListServer",
        "method": "get_singer_list",
        "param": {
            "area": -100,
            "sex": -100,
            "genre": -100,
            "index": -100,
            "sin": 0,
            "cur_page": 1
        }
    }
}

# 定义地区和对应的文件名
areas = {
    200: "国内_qqsingers.json",
    5: "欧美_qqsingers.json",
    4: "日本_qqsingers.json"
}

# 定义每页歌手数量
PAGE_SIZE = 80

def get_singers(area, page):
    params["singerList"]["param"]["area"] = area
    params["singerList"]["param"]["sin"] = PAGE_SIZE * (page - 1)
    params["singerList"]["param"]["cur_page"] = page
    response = requests.get(API_URL.format(json.dumps(params)))
    return response.json()

def extract_singers(data):
    singers = []
    for singer in data["singerList"]["data"]["singerlist"]:
        singers.append({
            "singer_id": singer["singer_id"],
            "singer_mid": singer["singer_mid"],
            "name": singer["singer_name"]
        })
    return singers

def save_singers_to_file(singers, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(singers, f, ensure_ascii=False, indent=4)

def main():
    for area, filename in areas.items():
        all_singers = []
        page = 1
        max_singers = 80
        while len(all_singers) < max_singers:
            data = get_singers(area, page)
            if data["code"] != 0 or not data["singerList"]["data"]["singerlist"]:
                break
            singers = extract_singers(data)
            all_singers.extend(singers)
            page += 1
        save_singers_to_file(all_singers, filename)
        print(f"Saved {len(all_singers)} singers to {filename}")

if __name__ == "__main__":
    main()
