import os, sys, re, json, subprocess
from time import sleep
from PySide2.QtCore import QThread, Signal

# 共享VIP Cookie预留（不使用请注释）
# import requests
# import req_encrypt as request

# 不使用共享VIP Cookie（不使用请取消注释）
import requests as request


############################################################################################
# biliDownloader下载主工作线程
class biliWorker(QThread):
    # 信息槽发射
    business_info = Signal(str)
    vq_list = Signal(str)
    aq_list = Signal(str)
    media_list = Signal(list)
    progr_bar = Signal(dict)
    is_finished = Signal(int)
    interact_info = Signal(dict)

    # 初始化
    def __init__(self, args, model=0):
        super(biliWorker, self).__init__()
        self.run_model = model
        self.haveINFO = False
        self.pauseprocess = False
        self.subpON = False
        self.killprocess = False
        self.index_url = args["Address"]
        self.d_list = args["DownList"]
        self.VQuality = args["VideoQuality"]
        self.AQuality = args["AudioQuality"]
        self.output = args["Output"]
        self.synthesis = args["sym"]
        self.systemd = args["sys"]
        self.re_playinfo = 'window.__playinfo__=([\s\S]*?)</script>'
        self.re_INITIAL_STATE = 'window.__INITIAL_STATE__=([\s\S]*?);\(function'
        self.vname_expression = '<title(.*?)</title>'
        self.chunk_size = args["chunk_size"]
        self.set_err = args["dl_err"]
        self.index_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
        }
        self.second_headers = {
            "accept": "*/*",
            "Connection": "keep-alive",
            "accept-encoding": "identity",
            "accept-language": "zh-CN,zh;q=0.9",
            "origin": "https://www.bilibili.com",
            "sec-fetch-site": "cross-site",
            "sec-fetch-mode": "cors",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
        }
        if args["useCookie"]:
            self.index_headers["cookie"] = args["cookie"]
            self.second_headers["cookie"] = args["cookie"]
        else:
            self.index_headers["cookie"] = ""
            self.second_headers["cookie"] = ""
        if args["useProxy"]:
            self.Proxy = args["Proxy"]
        else:
            self.Proxy = None

    # 运行模式设置函数
    def model_set(self, innum):
        self.run_model = innum

    # 结束进程函数
    def close_process(self):
        self.killprocess = True
        self.pauseprocess = False
        self.business_info.emit("正在结束下载进程......")

    # 暂停下载进程函数
    def pause(self):
        if self.subpON:
            self.business_info.emit("视频正在合成，只能终止不能暂停")
            return False
        else:
            self.business_info.emit("下载已暂停")
            self.pauseprocess = True

    # 恢复下载进程函数
    def resume(self):
        self.business_info.emit("下载已恢复")
        self.pauseprocess = False

    # File name conflict replace
    def name_replace(self, name):
        vn = name.replace(' ', '_').replace('\\', '').replace('/', '')
        vn = vn.replace('*', '').replace(':', '').replace('?', '').replace('<', '')
        vn = vn.replace('>', '').replace('\"', '').replace('|', '').replace('\x08', '')
        return vn

    # Change /SS movie address
    def ssADDRCheck(self, inurl):
        # checking1:番剧首页视频地址检查； checking2:番剧单个视频地址检查
        checking1 = re.findall('/play/ss', inurl.split("?")[0], re.S)
        checking2 = re.findall('/play/ep', inurl.split("?")[0], re.S)
        try:
            if checking1 != []:
                res = request.get(inurl, headers=self.index_headers, stream=False, timeout=10, proxies=self.Proxy)
                dec = res.content.decode('utf-8')
                INITIAL_STATE = re.findall(self.re_INITIAL_STATE, dec, re.S)
                temp = json.loads(INITIAL_STATE[0])
                self.index_url = temp["mediaInfo"]["episodes"][0]["link"]
                return 1, temp["mediaInfo"]["episodes"][0]["link"]
            elif checking2 != []:
                return 1, inurl
            else:
                return 0, inurl
        except Exception as e:
            print(e)
            return 0, inurl

    # Searching Key Word
    def search_preinfo(self, index_url):
        # Get Html Information
        index_url = self.ssADDRCheck(index_url)
        try:
            res = request.get(index_url[1], headers=self.index_headers, stream=False, timeout=10, proxies=self.Proxy)
            dec = res.content.decode('utf-8')
        except:
            print("初始化信息获取失败。")
            return 0, "", "", {}
        # Use RE to find Download JSON Data
        playinfo = re.findall(self.re_playinfo, dec, re.S)
        INITIAL_STATE = re.findall(self.re_INITIAL_STATE, dec, re.S)
        if playinfo == [] or INITIAL_STATE == []:
            print("Session等初始化信息获取失败。")
            return 0, "", "", {}
        # Bangumi Video
        re_init = json.loads(INITIAL_STATE[0])
        re_GET = json.loads(playinfo[0])
        # Normal Video
        # if index_url[0] == 0:
        #     now_cid = re_init["videoData"]["pages"][re_init["p"]-1]["cid"]
        #     try:
        #         makeurl = "https://api.bilibili.com/x/player/playurl?cid="+ str(now_cid) +\
        #                   "&qn=116&type=&otype=json&fourk=1&bvid="+ re_init["bvid"] +\
        #                   "&fnver=0&fnval=976&session=" + re_GET["session"]
        #         self.second_headers['referer'] = index_url[1]
        #         res = request.get(makeurl, headers=self.second_headers, stream=False, timeout=10, proxies=self.Proxy)
        #         re_GET = json.loads(res.content.decode('utf-8'))
        #         # print(json.dumps(re_GET))
        #     except Exception as e:
        #         print("获取Playlist失败:",e)
        #         return 0, "", "", {}
        # If Crawler can GET Data
        try:
            # Get video name
            vn1 = re.findall(self.vname_expression, dec, re.S)[0].split('>')[1]
            vn2 = ""
            if "videoData" in re_init:
                vn2 = re_init["videoData"]["pages"][re_init["p"] - 1]["part"]
            elif "mediaInfo" in re_init:
                vn2 = re_init["epInfo"]["titleFormat"] + ":" + re_init["epInfo"]["longTitle"]
            video_name = self.name_replace(vn1) + "_[" + self.name_replace(vn2) + "]"
            # List Video Quality Table
            length, down_dic = self.tmp_dffss(re_GET)
            # Return Data
            return 1, video_name, length, down_dic
        except Exception as e:
            print("PreInfo:", e)
            return 0, "", "", {}

    def tmp_dffss(self, re_GET):
        temp_v = {}
        for i in range(len(re_GET["data"]["accept_quality"])):
            temp_v[str(re_GET["data"]["accept_quality"][i])] = str(re_GET["data"]["accept_description"][i])
        # List Video Download Quality
        down_dic = {"video": {}, "audio": {}}
        i = 0
        # Get Video identity information and Initial SegmentBase.
        for dic in re_GET["data"]["dash"]["video"]:
            if str(dic["id"]) in temp_v:
                qc = temp_v[str(dic["id"])]
                down_dic["video"][i] = [qc, [dic["baseUrl"]], 'bytes=' + dic["SegmentBase"]["Initialization"]]
                if dic.get('backupUrl') is list:
                    for a in range(len(dic["backupUrl"])):
                        down_dic["video"][i][1].append(dic["backupUrl"][a])
                i += 1
            else:
                continue
        # List Audio Stream
        i = 0
        for dic in re_GET["data"]["dash"]["audio"]:
            au_stream = dic["codecs"] + "  音频带宽：" + str(dic["bandwidth"])
            down_dic["audio"][i] = [au_stream, [dic["baseUrl"]],
                                    'bytes=' + dic["SegmentBase"]["Initialization"]]
            if dic.get('backupUrl') is list:
                for a in range(len(dic["backupUrl"])):
                    down_dic["audio"][i][1].append(dic["backupUrl"][a])
            i += 1
        # Get Video Length
        length = re_GET["data"]["dash"]["duration"]
        return length, down_dic

    # Search the list of Video download address.
    def search_videoList(self, index_url):
        try:
            res = request.get(index_url, headers=self.index_headers, stream=False, timeout=10, proxies=self.Proxy)
            dec = res.content.decode('utf-8')
        except:
            return 0, {}
        INITIAL_STATE = re.findall(self.re_INITIAL_STATE, dec, re.S)
        if INITIAL_STATE != []:
            try:
                re_init = json.loads(INITIAL_STATE[0])
                init_list = {}
                if "videoData" in re_init:
                    init_list["bvid"] = re_init["bvid"]
                    init_list["p"] = re_init["p"]
                    init_list["pages"] = re_init["videoData"]["pages"]
                    # print(init_list)
                    return 1, init_list
                elif "mediaInfo" in re_init:
                    init_list["bvid"] = re_init["mediaInfo"]["media_id"]
                    init_list["p"] = re_init["epInfo"]["i"] + 1
                    init_list["pages"] = re_init["mediaInfo"]["episodes"]
                    # print(init_list)
                    return 2, init_list
                else:
                    return 0, {}
            except Exception as e:
                print("videoList:", e)
                return 0, {}
        else:
            return 0, {}

    # Show preDownload Detail
    def show_preDetail(self):
        # flag,video_name,length,down_dic,init_list = self.search_preinfo()
        temp = self.search_preinfo(self.index_url)
        preList = self.search_videoList(self.index_url)
        self.business_info.emit('--------------------我是分割线--------------------')
        try:
            if temp[0] and preList[0] != 0:
                if preList[0] == 1:
                    # Show video pages
                    # self.business_info.emit("We Get!")
                    self.business_info.emit('当前需要下载的BV号为：{}'.format(preList[1]["bvid"]))
                    self.business_info.emit('当前BV包含视频数量为{}个'.format(len(preList[1]["pages"])))
                    for sp in preList[1]["pages"]:
                        form_str = "{}-->{}".format(sp["page"], sp["part"])
                        if sp["page"] == preList[1]["p"]:
                            self.media_list.emit([1, form_str])
                        else:
                            self.media_list.emit([0, form_str])
                elif preList[0] == 2:
                    # Show media pages
                    self.business_info.emit('当前需要下载的媒体号为：{}'.format(preList[1]["bvid"]))
                    self.business_info.emit('当前媒体包含视频数量为{}个'.format(len(preList[1]["pages"])))
                    # self.business_info.emit('-----------具体分P视频名称与下载号-----------')
                    i = 0
                    for sp in preList[1]["pages"]:
                        i += 1
                        form_str = "{}-->{}".format(i, sp["share_copy"])
                        if i == preList[1]["p"]:
                            self.media_list.emit([1, form_str])
                        else:
                            self.media_list.emit([0, form_str])
                self.business_info.emit('--------------------我是分割线--------------------')
                # Show Video Download Detail
                self.business_info.emit('当前下载视频名称：{}'.format(temp[1]))
                self.business_info.emit('当前下载视频长度： {} 秒'.format(temp[2]))
                # print('当前可下载视频流：')
                for i in range(len(temp[3]["video"])):
                    # print("{}-->视频画质：{}".format(i, temp[3]["video"][i][0]))
                    self.vq_list.emit("{}.{}".format(i + 1, temp[3]["video"][i][0]))
                for i in range(len(temp[3]["audio"])):
                    # print("{}-->音频编码：{}".format(i, temp[3]["audio"][i][0]))
                    self.aq_list.emit("{}.{}".format(i + 1, temp[3]["audio"][i][0]))
                return 1
            else:
                return 0
        except Exception as e:
            print(e)
            return 0

    # Download Stream function
    def d_processor(self, url_list, output_dir, output_file, dest):
        for line in url_list:
            self.business_info.emit('使用线路：{}'.format(line.split("?")[0]))
            try:
                # video stream length sniffing
                video_bytes = request.get(line, headers=self.second_headers, stream=False, timeout=(5, 10),
                                          proxies=self.Proxy)
                vc_range = video_bytes.headers['Content-Range'].split('/')[1]
                self.business_info.emit("获取{}流范围为：{}".format(dest, vc_range))
                self.business_info.emit('{}  文件大小：{} MB'.format(dest, round(float(vc_range) / 1024 / 1024), 4))
                # Get the full video stream
                proc = {"Max": int(vc_range), "Now": 0, "finish": 0}
                err = 0
                while err <= self.set_err:
                    try:
                        self.second_headers['range'] = 'bytes=' + str(proc["Now"]) + '-' + vc_range
                        m4sv_bytes = request.get(line, headers=self.second_headers, stream=True, timeout=10,
                                                 proxies=self.Proxy)
                        self.progr_bar.emit(proc)
                        if not os.path.exists(output_dir):
                            os.makedirs(output_dir)
                        with open(output_file, 'ab') as f:
                            for chunks in m4sv_bytes.iter_content(chunk_size=self.chunk_size):
                                while self.pauseprocess:
                                    sleep(1.5)
                                    if self.killprocess:
                                        return -1
                                if chunks:
                                    f.write(chunks)
                                    proc["Now"] += self.chunk_size
                                    self.progr_bar.emit(proc)
                                if self.killprocess:
                                    m4sv_bytes.close()
                                    return -1
                        if proc["Now"] >= proc["Max"]:
                            m4sv_bytes.close()
                            break
                        else:
                            print("服务器断开连接，重新连接下载端口....")
                    except Exception as e:
                        if not re.findall('10054', str(e), re.S):
                            err += 1
                        print(e, err)
                if err > self.set_err:
                    raise Exception('线路出错，切换线路。')
                proc["finish"] = 1
                self.progr_bar.emit(proc)
                self.business_info.emit("{}成功！".format(dest))
                return 0
            except Exception as e:
                print(e)
                self.business_info.emit("{}出错：{}".format(dest, e))
                # print(proc)
                if os.path.exists(output_file):
                    os.remove(output_file)
        return 1

    # # 线程部署 -> List
    # def make_Thread_list(self, url: str, thread_num: int, byte_weight: int, tmp_dir) -> list:
    #     thread_list = []
    #     st_byte = -1
    #     for i in range(thread_num):
    #         # 确定线程下载范围
    #         st_byte += 1
    #         ed_byte = int(byte_weight/thread_num) * (i+1)
    #         if i == (thread_num - 1):
    #             ed_byte = byte_weight
    #         range_tuple = (st_byte, ed_byte)
    #         # 新建线程类
    #         t = DLThread(url, range_tuple, tmp_dir+'/{}.tmp'.format(i), self.second_headers, self.Proxy)
    #         tmp = []
    #         tmp.append(i)
    #         tmp.append(t)
    #         thread_list.append(tmp)
    #         st_byte = ed_byte
    #     return thread_list
    #
    #
    # # Download Stream function (NEW)
    # def d_processor(self, url_list, output_dir, output_file, dest):
    #     for line in url_list:
    #         self.business_info.emit('使用线路：{}'.format(line.split("?")[0]))
    #         try:
    #             # video stream length sniffing
    #             video_bytes = request.get(line, headers=self.second_headers, stream=False, timeout=(5, 10),
    #                                       proxies=self.Proxy)
    #             vc_range = video_bytes.headers['Content-Range'].split('/')[1]
    #             self.business_info.emit("获取{}流范围为：{}".format(dest, vc_range))
    #             self.business_info.emit(
    #                 '{}  文件大小：{} MB'.format(dest, round(float(vc_range) / self.chunk_size / 1024), 4))
    #             # 开始线程分配与文件夹制作
    #             thread_num = 4
    #             tmp_dir = output_dir + '/tmp_{}'.format(int(time.time()*1000))
    #             if not os.path.exists(tmp_dir):
    #                 os.makedirs(tmp_dir)
    #             thread_queue = self.make_Thread_list(line, thread_num, int(vc_range), tmp_dir)
    #             # Get the full video stream
    #             proc = {"Max": int(vc_range), "Now": 0, "finish": 0}
    #             err = 0
    #             self.business_info.emit("下载线程数：{}".format(thread_num))
    #             # 激活线程
    #             for t in thread_queue:
    #                 t[1].start()
    #             # 下载线程遍历监视代码
    #             while(err <= 3):
    #                 # 暂停下载
    #                 if self.pauseprocess:
    #                     for th in thread_queue:
    #                         th[1].pause()
    #                     while self.pauseprocess:
    #                         sleep(1.5)
    #                         if self.killprocess:
    #                             for th in thread_queue:
    #                                 th[1].stop()
    #                             return -1
    #                 # 停止下载
    #                 if self.killprocess:
    #                     for th in thread_queue:
    #                         th[1].stop()
    #                     return -1
    #                 # 获取总状态
    #                 progress = 0
    #                 finished_thread = 0
    #                 for th in thread_queue:
    #                     status = th[1].get_status()
    #                     if status['status'] == 3:
    #                         err += 1
    #                         th[1].start()
    #                     if status['now'] >= status['end']:
    #                         finished_thread += 1
    #                     progress += status['progress']
    #                 proc['Now'] = progress
    #                 self.progr_bar.emit(proc)
    #                 sleep(0.5)
    #                 if finished_thread == thread_num:
    #                     break
    #             if err > 3:
    #                 for th in thread_queue:
    #                     th[1].stop()
    #                 # 删除临时文件与文件夹
    #                 for i in os.listdir(tmp_dir):
    #                     os.remove(tmp_dir + '/{}'.format(i))
    #                 os.remove(tmp_dir)
    #                 raise Exception('线路出错，切换线路。')
    #             # 进行文件拼接
    #             self.business_info.emit("正在进行文件拼接.....")
    #             if os.path.isfile(output_file):
    #                 os.remove(output_file)
    #             with open(output_file, 'ab') as f:
    #                 for p in thread_queue:
    #                     with open(tmp_dir+'/{}.tmp'.format(p[0]), 'rb') as bf:
    #                         f.write(bf.read())
    #             # 删除临时文件与文件夹
    #             for i in os.listdir(tmp_dir):
    #                 os.remove(tmp_dir + '/{}'.format(i))
    #             os.remove(tmp_dir)
    #             # 结束下载进程
    #             proc["finish"] = 1
    #             self.progr_bar.emit(proc)
    #             self.business_info.emit("{}成功！".format(dest))
    #             return 0
    #         except Exception as e:
    #             print(e)
    #             self.business_info.emit("{}出错：{}".format(dest, e))
    #             if os.path.exists(output_file):
    #                 os.remove(output_file)
    #     return 1

    # FFMPEG Synthesis Function
    def ffmpeg_synthesis(self, input_v, input_a, output_add):
        if os.path.exists(output_add):
            self.business_info.emit("文件：{}\n已存在。".format(output_add))
            return -1
        ffcommand = ""
        if self.systemd == "win32":
            ffpath = os.path.dirname(os.path.realpath(sys.argv[0]))
            ffcommand = '"' + ffpath + '\\ffmpeg.exe" -i "' + \
                        input_v + '" -i "' + \
                        input_a + '" -c:v copy -c:a aac -strict experimental "' + output_add + '"'
        elif self.systemd == "linux":
            ffcommand = 'ffmpeg -i "' + input_v + '" -i "' + input_a + '" -c:v copy -c:a aac -strict experimental "' + output_add + '"'
        elif self.systemd == "darwin":
            ffpath = os.path.dirname(os.path.realpath(sys.argv[0]))
            ffcommand = '"' + ffpath + '/ffmpeg" -i "' + \
                        input_v + '" -i "' + \
                        input_a + '" -c:v copy -c:a aac -strict experimental "' + output_add + '"'
        else:
            self.business_info.emit("未知操作系统：无法确定FFMpeg命令。")
            return -2
        # 内测版专属
        # self.business_info.emit('--------------------内测分割线--------------------')
        # self.business_info.emit("操作系统：{}\nFFMPEG命令：{}".format(self.systemd, ffcommand))
        # self.business_info.emit('--------------------内测分割线--------------------')
        try:
            self.subpON = True
            temp = self.subp_GUIFollow(ffcommand)
            if temp:
                raise Exception(temp)
            self.subpON = False
            self.business_info.emit("视频合并完成！")
            os.remove(input_v)
            os.remove(input_a)
        except Exception as e:
            self.business_info.emit("视频合成失败：{}".format(e))
            self.subpON = False

    # Subprocess Progress of FFMPEG, RUN and Following Function
    def subp_GUIFollow(self, ffcommand):
        proc = {"Max": 100, "Now": 0, "finish": 2}
        subp = subprocess.Popen(ffcommand, shell=True, stderr=subprocess.PIPE, stdin=subprocess.PIPE,
                                encoding=sys.getfilesystemencoding())
        self.business_info.emit('FFMPEG正在执行合成指令')
        while True:
            status = subp.poll()
            if status is not None:
                if status != 0:
                    self.business_info.emit("FFMPEG运行出错，代码：{}".format(status))
                    proc["finish"] = 1
                    self.progr_bar.emit(proc)
                    return status
                else:
                    proc["finish"] = 1
                    self.progr_bar.emit(proc)
                    return 0
            if self.killprocess:
                subp.stdin.write('q')
            line = os.read(subp.stderr.fileno(), 1024)
            if line:
                # print(line)
                sf = re.findall('Duration: ([\s\S]*?),', str(line), re.S)
                cf = re.findall('time=([\s\S]*?) bitrate=', str(line), re.S)
                if sf:
                    temp = sf[0]
                    temp = temp.split(".")[0].split(":")
                    num = int(temp[0]) * 3600 + int(temp[1]) * 60 + int(temp[2])
                    # print("视频总长：", num)
                    proc["Max"] = num
                if cf:
                    temp = cf[0].split(".")[0].split(":")
                    cnum = int(temp[0]) * 3600 + int(temp[1]) * 60 + int(temp[2])
                    # print("当前进度", cnum)
                    proc["Now"] = cnum
                self.progr_bar.emit(proc)

    # For Download Single Video
    def Download_single(self, index=""):
        # Get video pre-detial
        if index == "":
            flag, video_name, _, down_dic = self.search_preinfo(self.index_url)
            index = self.index_url
        else:
            flag, video_name, _, down_dic = self.search_preinfo(index)
        # If we can access the video page
        if flag:
            try:
                # Judge file whether exists
                video_dir = self.output + '/' + video_name + '_video.m4s'
                audio_dir = self.output + '/' + video_name + '_audio.m4s'
                sym_video_dir = self.output + '/' + video_name + '.mp4'
                if os.path.exists(video_dir):
                    self.business_info.emit("文件：{}\n已存在。".format(video_dir))
                    return -1
                if os.path.exists(audio_dir):
                    self.business_info.emit("文件：{}\n已存在。".format(audio_dir))
                    return -1
                if os.path.exists(sym_video_dir):
                    self.business_info.emit("文件：{}\n已存在。".format(sym_video_dir))
                    return -1
                # self.business_info.emit("需要下载的视频：{}".format(video_name))
                # Perform video stream length sniffing
                self.second_headers['referer'] = index
                self.second_headers['range'] = down_dic["video"][self.VQuality][2]
                # Switch between main line and backup line(video).
                if self.killprocess:
                    return -2
                a = self.d_processor(down_dic["video"][self.VQuality][1], self.output, video_dir, "下载视频")
                # Perform audio stream length sniffing
                self.second_headers['range'] = down_dic["audio"][self.AQuality][2]
                # Switch between main line and backup line(audio).
                if self.killprocess:
                    return -2
                b = self.d_processor(down_dic["audio"][self.AQuality][1], self.output, audio_dir, "下载音频")
                if a or b:
                    return -3
                # Merge audio and video (USE FFMPEG)
                if self.killprocess:
                    return -2
                if self.synthesis:
                    self.business_info.emit('正在启动FFMPEG......')
                    # Synthesis processor
                    self.ffmpeg_synthesis(video_dir, audio_dir, sym_video_dir)
            except Exception as e:
                print(e)
        else:
            self.business_info.emit("下载失败：尚未找到源地址，请检查网站地址或充值大会员！")

    # For Download partition Video
    def Download_List(self):
        r_list = self.d_list
        all_list = self.search_videoList(self.index_url)
        preIndex = self.index_url.split("?")[0]
        # print(all_list,r_list)
        # print(preIndex)
        if all_list[0] == 1:
            if r_list[0] == 0:
                for p in all_list[1]["pages"]:
                    if self.killprocess:
                        break
                    self.Download_single(preIndex + "?p=" + str(p["page"]))
            else:
                listLEN = len(all_list[1]["pages"])
                for i in r_list:
                    if self.killprocess:
                        break
                    if i <= listLEN:
                        self.Download_single(preIndex + "?p=" + str(i))
                    else:
                        continue
            self.business_info.emit("列表视频下载进程结束！")
        elif all_list[0] == 2:
            if r_list[0] == 0:
                for p in all_list[1]["pages"]:
                    if self.killprocess:
                        break
                    self.Download_single(p["link"])
            else:
                listLEN = len(all_list[1]["pages"])
                for i in r_list:
                    if self.killprocess:
                        break
                    if i <= listLEN:
                        self.Download_single(all_list[1]["pages"][i - 1]["link"])
                    else:
                        continue
            self.business_info.emit("媒体视频下载进程结束！")
        else:
            self.business_info.emit("未找到视频列表信息。")

    ###################################################################
    # 交互进程初始数据获取函数
    def interact_preinfo(self):
        self.now_interact = {"cid": "", "bvid": "", "session": "", "graph_version": "", "node_id": "", "vname": ""}
        t1 = self.Get_Init_Info(self.index_url)
        self.index_headers['referer'] = self.index_url
        self.second_headers = self.index_headers
        t2 = self.isInteract()
        if t1[0] or t2[0]:
            return 1, {}, {}
        return 0, self.now_interact

    # Interactive video download
    def requests_start(self, now_interact, iv_structure):
        self.now_interact = now_interact
        self.recursion_for_Download(iv_structure, self.output)
        self.business_info.emit("下载交互视频完成。")

    # 设置预下载信息
    def Set_Structure(self, now_interact, iv_structure):
        self.now_interact = now_interact
        self.iv_structure = iv_structure

    # Interactive video initial information
    def Get_Init_Info(self, url):
        try:
            res = request.get(url, headers=self.index_headers, stream=False, timeout=10, proxies=self.Proxy)
            dec = res.content.decode('utf-8')
            playinfo = re.findall(self.re_playinfo, dec, re.S)
            INITIAL_STATE = re.findall(self.re_INITIAL_STATE, dec, re.S)
            if playinfo == [] or INITIAL_STATE == []:
                raise Exception("无法找到初始化信息。")
            playinfo = json.loads(playinfo[0])
            INITIAL_STATE = json.loads(INITIAL_STATE[0])
            self.now_interact["session"] = playinfo["session"]
            self.now_interact["bvid"] = INITIAL_STATE["bvid"]
            self.now_interact["cid"] = str(INITIAL_STATE["cidMap"][INITIAL_STATE["bvid"]]["cids"]["1"])
            self.now_interact["vname"] = self.name_replace(INITIAL_STATE["videoData"]["title"])
            return 0, ""
        except Exception as e:
            return 1, str(e)

    # Judge the interactive video.
    def isInteract(self):
        make_API = "https://api.bilibili.com/x/player/v2"
        param = {
            'cid': self.now_interact["cid"],
            'bvid': self.now_interact["bvid"],
        }
        try:
            res = request.get(make_API, headers=self.index_headers, params=param, timeout=10, proxies=self.Proxy)
            des = json.loads(res.content.decode('utf-8'))
            if "interaction" not in des["data"]:
                raise Exception("非交互视频")
            self.now_interact["graph_version"] = str(des["data"]["interaction"]["graph_version"])
            return 0, ""
        except Exception as e:
            return 1, str(e)

    # Get interactive video download URL and Dict
    def down_list_make(self, cid_num):
        make_API = "https://api.bilibili.com/x/player/playurl"
        param = {
            'cid': cid_num,
            'bvid': self.now_interact["bvid"],
            'qn': '116',
            'type': '',
            'otype': 'json',
            'fourk': '1',
            'fnver': '0',
            'fnval': '976',
            'session': self.now_interact["session"]
        }
        try:
            des = request.get(make_API, headers=self.index_headers, params=param, timeout=10, proxies=self.Proxy)
            playinfo = json.loads(des.content.decode('utf-8'))
        except Exception as e:
            return False, str(e)
        if playinfo != {}:
            re_GET = playinfo
            # List Video Quality Table
            length, down_dic = self.tmp_dffss(re_GET)
            # Return Data
            return True, length, down_dic
        else:
            return False, "Get Download List Error."

    # Interactive video download processor (Use recursion algorithm)
    def recursion_for_Download(self, json_list, output_dir):
        for ch in json_list:
            chn = self.name_replace(ch)
            output = output_dir + "/" + chn
            video_dir = output + "/" + chn + '_video.m4s'
            audio_dir = output + "/" + chn + '_audio.m4s'
            # 新字典判断
            if json_list[ch]['isChoose']:
                # if "cid" in json_list[ch]:
                dic_return = self.down_list_make(json_list[ch]["cid"])
                # print(dic_return)
                if not dic_return[0]:
                    self.business_info.emit("节点（{}）获取下载地址出错".format(ch))
                    print(dic_return[1])
                    return -1
                _, _, down_dic = dic_return
                self.second_headers["range"] = down_dic["video"][self.VQuality][2]
                self.d_processor(down_dic["video"][self.VQuality][1], output, video_dir, "下载视频：" + chn)
                self.second_headers['range'] = down_dic["audio"][self.AQuality][2]
                self.d_processor(down_dic["audio"][self.AQuality][1], output, audio_dir, "下载音频：" + chn)
                if self.synthesis:
                    self.business_info.emit('正在启动ffmpeg......')
                    self.ffmpeg_synthesis(video_dir, audio_dir, output + '/' + chn + '.mp4')
            if "choices" in json_list[ch]:
                self.recursion_for_Download(json_list[ch]["choices"], output)
        return 0

    ###################################################################
    # 音频进程
    def search_AUPreinfo(self, au_url):
        # check1:音乐歌单页面检测；check2:单个音乐页面检测
        check1 = re.findall(r'/audio/am(\d+)', au_url, re.S)
        check2 = re.findall(r'/audio/au(\d+)', au_url, re.S)
        if check1:
            # print(check1[0])
            temps = self.AuList_Maker(check1[0], 2)
            if temps[0]:
                # print(json.dumps(temps[1]))
                return 1, temps[1]
            else:
                return 0, "Audio List Get Error."
        elif check2:
            # print(check2[0])
            temps = self.AuList_Maker(check2[0], 1)
            if temps[0]:
                # print(json.dumps(temps[1]))
                return 2, temps[1]
            else:
                return 0, "Audio Single Get Error."
        else:
            print("Is NOT Music.")
            return 0, {}

    def AuList_Maker(self, sid, modeNUM):
        list_dict = {"audio": [], "total": 0}
        if modeNUM == 1:
            try:
                makeURL = "https://www.bilibili.com/audio/music-service-c/web/song/info?sid=" + sid
                res = request.get(makeURL, headers=self.index_headers, stream=False, timeout=10, proxies=self.Proxy)
                des = res.content.decode('utf-8')
                auinfo = json.loads(des)["data"]
                temp = {
                    "title": auinfo["title"] + "_" + auinfo["author"],
                    "sid": sid, "cover": auinfo["cover"],
                    "duration": auinfo["duration"],
                    "lyric": auinfo["lyric"]
                }
                list_dict["audio"].append(temp)
                list_dict["total"] = 1
            except Exception as e:
                print("AuList_Maker_Single:", e)
                return 0, "AuList_Maker_Single:{}".format(e)
            return 1, list_dict
        elif modeNUM == 2:
            try:
                pn = 1
                while True:
                    makeURL = "https://www.bilibili.com/audio/music-service-c/web/song/of-menu?sid=" + sid + "&pn=" + str(
                        pn) + "&ps=30"
                    res = request.get(makeURL, headers=self.index_headers, stream=False, timeout=10, proxies=self.Proxy)
                    des = res.content.decode('utf-8')
                    mu_dic = json.loads(des)["data"]
                    for sp in mu_dic["data"]:
                        # print(sp)
                        temp = {
                            "title": sp["title"] + "_" + sp["author"],
                            "sid": str(sp["id"]), "cover": sp["cover"],
                            "duration": sp["duration"], "lyric": sp["lyric"]
                        }
                        list_dict["audio"].append(temp)
                        list_dict["total"] += 1
                    if pn >= mu_dic["pageCount"]:
                        break
                    else:
                        pn += 1
                        continue
            except Exception as e:
                print("AuList_Maker_List:", e)
                return 0, "AuList_Maker_List:{}".format(e)
            return 1, list_dict
        else:
            return 0, "ModeNum Error."

    # 显示音频信息
    @property
    def Audio_Show(self):
        au_dic = self.search_AUPreinfo(self.index_url)
        if au_dic[0] == 0:
            print(au_dic[1])
            return 0
        if au_dic[0] == 1:
            self.business_info.emit('当前歌单包含音乐数量为{}个'.format(au_dic[1]["total"]))
        elif au_dic[0] == 2:
            self.business_info.emit('当前下载歌曲名称为：{}'.format(au_dic[1]["audio"][0]["title"]))
            self.business_info.emit('歌曲长度为：{}'.format(au_dic[1]["audio"][0]["duration"]))
        else:
            return 0
        i = 0
        for sp in au_dic[1]["audio"]:
            i += 1
            form_make = "{}-->{}".format(i, sp["title"])
            self.media_list.emit([0, form_make])
        self.vq_list.emit("无")
        self.aq_list.emit("最高音质")
        return 1

    # 获取单个音频下载地址
    def Audio_getDownloadList(self, sid):
        make_url = "https://www.bilibili.com/audio/music-service-c/web/url?sid=" + sid
        res = request.get(make_url, headers=self.index_headers, stream=False, timeout=10, proxies=self.Proxy)
        des = res.content.decode('utf-8')
        au_list = json.loads(des)["data"]["cdns"]
        return au_list

    # 附带资源下载
    def simple_downloader(self, url, output_dir, output_file):
        try:
            res = request.get(url, headers=self.index_headers, timeout=10, proxies=self.Proxy)
            file = res.content
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            with open(output_file, 'wb') as f:
                f.write(file)
        except Exception as e:
            self.business_info.emit("附带下载失败：{}".format(url))
            print("附带下载失败：", e)

    # 音乐下载函数
    def audio_downloader(self):
        self.second_headers["referer"] = "https://www.bilibili.com/"
        self.second_headers["sec-fetch-dest"] = 'audio'
        self.second_headers["sec-fetch-mode"] = 'no-cors'
        temp_dic = self.search_AUPreinfo(self.index_url)
        if temp_dic[0] == 0:
            self.business_info.emit("获取音乐前置信息出错。")
            return 0
        try:
            for index in self.d_list:
                sp = temp_dic[1]["audio"][index - 1]
                output_dir = self.output + "/" + self.name_replace(sp["title"])
                output_name = output_dir + "/" + self.name_replace(sp["title"])
                self.business_info.emit("正在下载音乐：{}".format(sp["title"]))
                if sp["cover"] != "":
                    self.simple_downloader(sp["cover"], output_dir, output_name + "_封面.jpg")
                if sp["lyric"] != "":
                    self.simple_downloader(sp["lyric"], output_dir, output_name + "_歌词.lrc")
                au_downlist = self.Audio_getDownloadList(sp["sid"])
                self.second_headers["range"] = 'bytes=0-'
                self.d_processor(au_downlist, output_dir, output_name + ".mp3", "下载音乐")
            self.business_info.emit("音乐下载进程结束！")
            return 1
        except Exception as e:
            self.business_info.emit("音频下载出错：{}".format(e))
            print("音频下载出错：", e)
            return 0

    ###################################################################
    # 运行线程
    def run(self):
        # self.reloader()
        if self.run_model == 0:
            # 探查资源类型
            self.interact_info.emit({"state": 0})
            d = self.interact_preinfo()
            r = self.show_preDetail()
            if r == 1:
                if d[0] == 0:
                    self.interact_info.emit({"state": 1, "data": d[1]})
                self.is_finished.emit(1)
            elif self.Audio_Show:
                self.is_finished.emit(4)
            else:
                self.is_finished.emit(0)
        elif self.run_model == 1:
            # 下载非交互视频
            if self.d_list:
                # print(1)
                self.Download_List()
                if self.killprocess:
                    self.business_info.emit("下载已终止")
                self.progr_bar.emit({"finish": 1})
                self.is_finished.emit(2)
            else:
                self.is_finished.emit(2)
        # elif self.run_model == 2:
        #     # 交互视频信息读取
        #     d = self.interact_nodeList()
        #     if d == {}:
        #         self.interact_info.emit({"state":-2,"data":{}})
        #         self.is_finished.emit(3)
        #     else:
        #         self.interact_info.emit({"state":2,"nowin":self.now_interact,"ivf":d})
        elif self.run_model == 3:
            # 交互视频下载
            self.requests_start(self.now_interact, self.iv_structure)
            self.is_finished.emit(3)
        elif self.run_model == 4:
            # 音频列表下载
            if self.d_list:
                self.audio_downloader()
                if self.killprocess:
                    self.business_info.emit("下载已终止")
                self.progr_bar.emit({"finish": 1})
                self.is_finished.emit(2)
            else:
                self.is_finished.emit(2)

#
# # 下载线程类
# class DLThread(QThread):
#     # 初始化
#     def __init__(self, url_str: str, byte_range: tuple, tmp_dir: str, header_dict: dict, proxy_dict: dict):
#         super(DLThread, self).__init__()
#         assert len(byte_range) == 2
#         self.url = url_str
#         self.tmpf_dir = tmp_dir
#         self.st_byte = byte_range[0]
#         self.now_byte = byte_range[0]
#         self.ed_byte = byte_range[1]
#         self.header = header_dict
#         self.Proxy = proxy_dict
#         self.chunk_size = 1024
#         self.err = 0
#         # 线程状态status：0为正常下载，1为暂停下载，2为停止下载，3为下载出错
#         self.status = 0
#
#     # 获取线程状态
#     def get_status(self):
#         feedback = {}
#         feedback['status'] = self.status
#         feedback['start'] = self.st_byte
#         feedback['end'] = self.ed_byte
#         feedback['now'] = self.now_byte
#         feedback['progress'] = self.now_byte - self.st_byte
#         feedback['err'] = self.err
#         return feedback
#
#     def pause(self):
#         if self.status == 0:
#             self.status = 1
#
#     def stop(self):
#         self.status = 2
#
#     def resume(self):
#         if self.status == 1:
#             self.status = 0
#
#     def run(self) -> None:
#         while (self.err <= 3):
#             try:
#                 self.header['range'] = 'bytes=' + str(self.st_byte) + '-' + str(self.ed_byte)
#                 m4sv_bytes = request.get(self.url, headers=self.header, stream=True, timeout=10, proxies=self.Proxy)
#                 # if not os.path.exists(output_dir):
#                 #     os.makedirs(output_dir)
#                 with open(self.tmpf_dir, 'wb') as f:
#                     for chunks in m4sv_bytes.iter_content(chunk_size=self.chunk_size):
#                         # 暂停事件函数
#                         while self.status == 1:
#                             sleep(1)
#                             if (self.status == 2) or (self.status == 3):
#                                 return None
#                             else:
#                                 continue
#                         if chunks:
#                             f.write(chunks)
#                             self.now_byte += self.chunk_size
#                             # self.progr_bar.emit(proc)
#                         if self.status == 2:
#                             m4sv_bytes.close()
#                             return None
#                 if self.now_byte >= self.ed_byte:
#                     m4sv_bytes.close()
#                     break
#                 else:
#                     print("线程范围：{}-{} -> 服务器断开连接，重新连接下载端口....".format(self.st_byte, self.ed_byte))
#             except Exception as e:
#                 if re.findall('10054', str(e), re.S) == []:
#                     self.err += 1
#                 print(e, self.err)
#         if self.err > 3:
#             self.status = 3
#             # raise Exception('线路出错，切换线路。')
#
