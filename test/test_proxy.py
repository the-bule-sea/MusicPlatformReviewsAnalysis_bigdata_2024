import time

import requests

def load_proxies(proxy_file_path):
    with open(proxy_file_path, 'r') as f:
        proxies = [line.strip() for line in f.readlines()]
    return proxies

def main():
    proxy_file_path = 'proxy.txt'
    proxies = load_proxies(proxy_file_path)
    url = "https://mail.163.com/"
    for proxy in proxies:
        print("当前代理IP"+proxy)
        r = requests.get(url ,proxies={"http": proxy, "https": proxy})
        print(r.status_code)
        time.sleep(5)

if __name__ == "__main__":
    main()

