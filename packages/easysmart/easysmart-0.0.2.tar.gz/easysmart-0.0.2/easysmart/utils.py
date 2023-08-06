import os
import time

import requests
import zipfile


def start_emqx_server():
    # 检测emqx是否存在
    if not os.path.exists(r'emqx\bin\emqx'):
        download_emqx()
    # start emqx by run "emqx\bin\emqx start"
    os.system(r"emqx\bin\emqx start")
    print('emqx server started')


def download_emqx():
    print('emqx not found, downloading...')
    download_url = r'https://www.emqx.com/zh/downloads/broker/5.0.26/emqx-5.0.26-windows-amd64.zip'
    r = requests.get(download_url)
    with open('emqx.zip', 'wb') as f:
        f.write(r.content)
    print('download finished ,unziping...')
    time.sleep(1)
    with zipfile.ZipFile('emqx.zip', 'r') as zip_ref:
        zip_ref.extractall(path='emqx')
    print('unzip finished')
    time.sleep(1)


if __name__ == '__main__':
    start_emqx_server()
