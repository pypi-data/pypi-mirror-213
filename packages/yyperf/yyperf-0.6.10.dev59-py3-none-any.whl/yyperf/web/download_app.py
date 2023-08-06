import requests
import os
import logging
import re
import time
from tqdm import tqdm
import urllib.request as urllib
import socket

def download_by_urllib(url,path,count=5):
    if count<0:
        return False
    try:
        import ssl
        ssl._create_default_https_context = ssl._create_unverified_context
        socket.setdefaulttimeout(180)
        urllib.urlretrieve(url,path)
        return True
    except Exception as e:
        logging.error(str(e))
        return download_by_urllib(url, path,count-1)

class DownloadAPP(object):

    @staticmethod
    def surpport_continue(url):
        headers = {
            'Range': 'bytes=0-4'
        }
        try:
            r = requests.head(url, headers=headers)
            crange = r.headers['content-range']
            total = int(re.match(r'^bytes 0-4/(\d+)$', crange).group(1))
            return True,total
        except:
            pass
        try:
            total = int(r.headers['content-length'])
        except:
            total = 0
        return False,total

    @staticmethod
    def download(url,path):
        try:
            size = 0
            flag,total = DownloadAPP.surpport_continue(url)
            if flag:
                logging.info("支持断点续传")
                fp = open(path,mode='wb')
                start = time.perf_counter()
                with tqdm(total=total, unit='B', unit_scale=True, ascii=True, desc=path) as bar:  # 打印下载时的进度条，实时显示下载速度
                    while size<total and time.perf_counter()-start<1200:
                        res = requests.get(url, stream=True, verify=False, headers={'Range': 'bytes=%d-'%size})
                        try:
                            for chunk in res.iter_content(chunk_size=1024):
                                if chunk:
                                    fp.write(chunk)
                                    bar.update(len(chunk))
                                    size += len(chunk)
                                    fp.flush()
                        except Exception as e:
                            logging.info(str(e))
                if size<total:
                    return False
                return True
            else:
                logging.info("不支持断点续传")
                return download_by_urllib(url, path)
        except Exception as e:
            logging.info(str(e))
            return False
