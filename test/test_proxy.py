import time
import random
import requests

def load_proxies(proxy_file_path):
    with open(proxy_file_path, 'r') as f:
        proxies = [line.strip() for line in f.readlines()]
    return proxies

def main():
    proxy_file_path = 'proxy.txt'
    while True:
        proxies = random.choice(load_proxies(proxy_file_path))
        url = "https://mail.163.com/"
        print("当前代理IP"+proxies)
        r = requests.get(url ,proxies={"http": "http://{}".format(proxies)})
        print(r.status_code)
        time.sleep(5)

if __name__ == "__main__":
    main()

