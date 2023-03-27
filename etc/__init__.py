import os, sys

# 发布版本信息
Release_INFO = ["V1.7.20230327", "2023/03/26"]

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
    "dl_err": 3,
    "chunk_size": 1024,
    "Proxy": {
        'http': '',
        'https': '',
    },
    "ProxyAuth": {
        'inuse': False,
        'usr': '',
        'pwd': '',
    }
}

# 本地
DF_Path = os.path.dirname(os.path.realpath(sys.argv[0]))

# Echarts CDN
Echart_CDN = 'https://gitee.com/zmtechn/echart-jscdn/raw/master/'
