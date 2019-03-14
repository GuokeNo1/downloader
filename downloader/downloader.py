# -*- coding: utf-8 -*-

import urllib3
import threading
import os

class downloader:
    def __init__(self, url, local='', threadnumber=4, downnow=False, headers={'user-agent': 'PyDownloader/1.0'}):
        if 'user-agent' not in headers:
            headers['user-agent'] = 'PyDownloader/1.0'
        self.TN = threadnumber
        self.headers = headers
        self.url = url
        self.isDownload = False
        if local == '':
            self.local = './'+url.split('/')[-1]
        else:
            self.local = local
        urllib3.disable_warnings()
        if downnow:
            self.startDownload()

    def startDownload(self):
        #开始分配线程
        self.threads = []
        result = self.__head()
        if 'Content-Length' in dict(result.getheaders()):
            self.length = dict(result.getheaders())['Content-Length']
            self.canDownload = True
        else:
            self.length = 0
            self.canDownload = False
            return False
        for x in range(self.TN):
            self.threads.append({'id': x, 'thread': threading.Thread(target=self.__downloadThread, args=(x, ))})
        for t in self.threads:
            t['thread'].start()
        # 文件保存线程
        threading.Thread(target=self.__isDownloadDone).start()
        return True

    def getThreadsStatus(self):
        result = {}
        for t in self.threads:
            result['Thread-{0}-Done'.format(t['id'])] = not t['thread'].isAlive()
        return result


    def __downloadThread(self, threadid):
        headers = self.headers.copy()
        length = int(self.length)/len(self.threads)
        start = length*threadid
        if threadid == self.TN-1:
            end = self.length
        else:
            end = start+length
        headers['Range'] = 'bytes={0}-{1}'.format(int(start), int(end))
        result = self.__download(headers)
        self.threads[threadid]['data'] = result.data

    def __isDownloadDone(self):
        for t in self.threads:
            while t['thread'].isAlive():
                pass
        path = self.local
        if not os.path.exists(os.path.dirname(path)):
            os.mkdir(os.path.dirname(path))
        with open(path, 'wb') as save:
            for t in self.threads:
                save.seek(int(int(self.length)/len(self.threads))*int(t['id']))
                save.write(t['data'])

    def __head(self):
        http = urllib3.PoolManager()
        result = http.request('HEAD', self.url, headers=self.headers)
        return result

    def __download(self, headers):
        http = urllib3.PoolManager()
        result = http.request('GET', self.url, headers=headers)
        return result


