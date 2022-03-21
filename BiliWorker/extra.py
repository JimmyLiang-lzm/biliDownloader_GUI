import json, webbrowser
from time import sleep
from PySide2.QtCore import QThread, Signal

# 共享VIP Cookie预留（不使用请注释）
# import requests
# import req_encrypt as request

# 不使用共享VIP Cookie（不使用请取消注释）
import requests as request


############################################################################################
# 检查更新防阻滞线程类
class checkLatest(QThread):
    _feedback = Signal(int)
    def __init__(self, inVer):
        super(checkLatest, self).__init__()
        self.lab_version = inVer

    def ver2num(self,inVer):
        temp = inVer.replace("V","").split(".")
        temp = int(temp[0] + temp[1] + temp[2])
        return temp

    def run(self):
        try:
            des = request.get("https://jimmyliang-lzm.github.io/source_storage/biliDownloader_verCheck.json", timeout=5)
            res = json.loads(des.content.decode('utf-8'))["biliDownloader_GUI"]
            latestVer = self.ver2num(res)
            myVer = self.ver2num(self.lab_version)
            if latestVer <= myVer:
                self._feedback.emit(0)
                sleep(2)
                self._feedback.emit(-1)
            else:
                self._feedback.emit(1)
                webbrowser.open("https://github.com/JimmyLiang-lzm/biliDownloader_GUI/releases/latest")
                sleep(2)
        except Exception as e:
            print(e)
            self._feedback.emit(2)
            sleep(2)
            self._feedback.emit(-1)


############################################################################################
# 测试代理地址防阻滞线程类
class checkProxy(QThread):
    _feedback = Signal(dict)
    def __init__(self, in_Proxy):
        super(checkProxy, self).__init__()
        self.use_Proxy = in_Proxy
        self.index_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
        }

    def run(self):
        try:
            temp = {"code":1}
            des = request.get("https://api.live.bilibili.com/xlive/web-room/v1/index/getIpInfo",
                              headers=self.index_headers, timeout=10, stream=False, proxies=self.use_Proxy)
            res = json.loads(des.content.decode('utf-8'))["data"]
            temp["ip"] = res["addr"]
            temp["area"] = res["country"]
            self._feedback.emit(temp)
        except Exception as e:
            self._feedback.emit({"code":-1,"message":"测试失败"})
