import os, sys

# 发布版本信息
Release_INFO = ["V1.5.20220311","2022/03/11"]

# 保存个人信息模板初始化
indict = {
    "Address": "",
    "DownList": [],
    "VideoQuality": 0,
    "AudioQuality": 0,
    "Output": "",
    "Synthesis": 1,
    "sys": "",
    "cookie": "",
    "sym": True,
    "useCookie": False,
    "useProxy": False,
    "Proxy": {
        'http': '',
        'https': '',
    }
}

# 本地
DF_Path = os.path.dirname(os.path.realpath(sys.argv[0]))