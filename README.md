# downloader
Python3 HTTP/HTTPS协议文件多线程下载模块

使用方法：
'''
import downloader
#url=下载链接, local=本地文件名, threadnumber=线程数(默认4), downnow=是否立即下载(默认否), headers=header定义(默认{'user-agent': 'PyDownloader/1.0'})
download = downloader.downloader(url='downloadurl', local='local file name')
#startDownload()开始下载,返回True表示开始下载,返回False表示不支持下载
if download.startDownload():
    #getThreadsStatus() 获取所有线程状态,False未完成,True下载完成
    result = download.getThreadsStatus()
    #查看线程是否下载完成
    #result = {'Thread-0-Done': False, 'Thread-1-Done': False, 'Thread-2-Done': False, 'Thread-3-Done': False}
    #result = {'Thread-0-Done': True, 'Thread-1-Done': True, 'Thread-2-Done': True, 'Thread-3-Done': True}

#download.canDownload 为bool值显示当前url是否可下载
#download.isSave 为bool值显示是否保存
'''
