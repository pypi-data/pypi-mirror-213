import sys
import time
import requests
import os
import datetime
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED
from collections import deque

class download_byte():

    def __init__(
            self,
            Max_Thread: int = 0,
            Max_Rerty: int = 3,
            Time_Sleep: [float, int] = 0,
            Request_Timeout: [float, int] = 10,
            urls: list = None,
            headers: [dict[str, any], None] = None,
            cookie: [dict[str, any], None] = None,
            param: [dict[str, any], None] = None,
            data: [dict[str, any], None] = None,
            proxies: [dict[str, any], None] = None,
            verify: bool = True,
            path_: str = './',
            Name_Rules: str = 'default',
            titles: [list, None] = None,
            Save_Error_Log: bool = True,
            Show_Progress_Bar: bool = False,
    ):
        self.Max_Thread = Max_Thread
        self.Max_Rerty = Max_Rerty
        self.Time_Sleep = Time_Sleep
        self.Request_Timeout = Request_Timeout
        self.urls = urls
        self.headers = headers
        self.cookie = cookie
        self.param = param
        self.data = data
        self.proxies = proxies
        self.verify = verify
        self.path_ = path_
        self.Name_Rules = Name_Rules
        self.titles = titles
        self.Save_Error_Log = Save_Error_Log
        self.Show_Progress_Bar = Show_Progress_Bar
        self.error_list = []
        if self.path_[-1] != '/':
            self.path_ += '/'
        self.deque_ = deque(maxlen=len(self.urls) + 1)
        self.title_deque_ = None
        self.all_task_number = len(self.urls)
        for u in self.urls:
            self.deque_.append({'url': u, 'n': 0, 'log': ''})
        if self.titles != 'title':
            self.title_deque_ = deque(maxlen=len(self.urls) + 1)
        else:
            self.title_deque_ = deque(maxlen=len(self.titles) + 1)
            for t in self.titles:
                self.title_deque_.append(t)
        self.urls = None
        self.titles = None

    def start(self):

        if self.Name_Rules.lower() == 'default':
            while bool(self.deque_):
                url = self.deque_.popleft()
                print(url)
                if '?' in url['url']:
                    title = url['url'].split('?')[0].split('/')[-1].split('.')[0]
                    format = url['url'].split('?')[0].split('/')[-1].split('.')[1]
                else:
                    title = url['url'].split('/')[-1].split('.')[0]
                    format = url['url'].split('/')[-1].split('.')[1]
                self.get_(url, title, format)
                if self.Show_Progress_Bar:
                    self.progress_bar(self.all_task_number - self.deque_.__len__(), self.all_task_number)
                else:
                    pass
        else:
            while bool(self.deque_):
                url = self.deque_.popleft()
                if '?' in url['url']:
                    title = self.titles[0]
                    format = url['url'].split('?')[0].split('/')[-1].split('.')[1]
                else:
                    title = self.titles[0]
                    format = url['url'].split('/')[-1].split('.')[1]
                self.get_(url, title, format)
                if self.Show_Progress_Bar:
                    self.progress_bar(self.all_task_number - self.deque_.__len__(), self.all_task_number)
                else:
                    pass


    def get_(self, url, name, type_):
        try:
            respones = requests.get(url=url['url'], headers=self.headers, cookies=self.cookie, proxies=self.proxies,
                                    verify=self.verify, params=self.param, data=self.data)
            if respones.status_code == 200:
                self.save_(respones.content, name, type_)
            else:
                raise Exception('响应码:{}，请求失败'.format(respones.status_code))
        except Exception as e:
            self.error_prompt(e, url, name)
        time.sleep(self.Time_Sleep)

    def error_prompt(self, e, url, name):
        if url['n'] < self.Max_Rerty:
            print('当前url：{}\n出现异常：{}\n未超出指定重试次数({}/{})，将添加回对列\n'.format(url['url'], e, url['n'] + 1,
                                                                        self.Max_Rerty))
            self.deque_.append({'url': url['url'], 'n': url['n'] + 1, 'log': ''})
            self.title_deque_.append(name)
        else:
            print('当前url：{}\n出现异常：{}\n超出指定重试次数({})，将写入错误列表\n'.format(url['url'], e,
                                                                     self.Max_Rerty))
            self.error_list.append({'url': url['url'], 'n': url['n'] + 1, 'log': e})

    def save_(self, content_, name, type_):
        if os.path.exists(self.path_):
            pass
        else:
            os.makedirs(self.path_)
        with open(self.path_ + name + '.' + type_, 'wb') as f:
            f.write(content_)

    def progress_bar(self, finish_tasks_number, all_task_number):
        percentage = round(finish_tasks_number / all_task_number * 100)
        print("\r下载进度: {}%: ".format(percentage), "▓" * (percentage // 2), end="")
        sys.stdout.flush()

    def save_log(self):
        if os.path.exists(self.path_):
            pass
        else:
            os.makedirs(self.path_)
        with open(self.path_ + datetime.datetime.now().strftime("%Y年%m月%d日_%H时%M分%S秒") + '_log.txt', 'w',
                  encoding='utf-8') as f:
            for i in self.error_list:
                f.write(str(i) + '\n')

class thread_download_byte(download_byte):
    def __init__(
            self,
            Max_Thread: int = 0,
            Max_Rerty: int = 3,
            Time_Sleep: [float, int] = 0,
            Request_Timeout: [float, int] = 10,
            urls: list = None,
            headers: [dict[str, any], None] = None,
            cookie: [dict[str, any], None] = None,
            param: [dict[str, any], None] = None,
            data: [dict[str, any], None] = None,
            proxies: [dict[str, any], None] = None,
            verify: bool = True,
            path_: str = './',
            Name_Rules: str = 'default',
            titles: [list, None] = None,
            Save_Error_Log: bool = True,
            Show_Progress_Bar: bool = False,
    ):
        super(thread_download_byte, self).__init__(
            Max_Thread=Max_Thread,
            Max_Rerty=Max_Rerty,
            Time_Sleep=Time_Sleep,
            Request_Timeout=Request_Timeout,
            urls=urls,
            headers=headers,
            cookie=cookie,
            param=param,
            data=data,
            proxies=proxies,
            verify=verify,
            path_=path_,
            Name_Rules=Name_Rules,
            titles=titles,
            Save_Error_Log=Save_Error_Log,
            Show_Progress_Bar=Show_Progress_Bar
        )
        self.threadpool = ThreadPoolExecutor(max_workers=self.Max_Thread)

    def start(self):
        self.all_task = []
        if self.Name_Rules.lower() == 'default':
            while bool(self.deque_):
                self.all_task = []
                if self.deque_.__len__() >= self.Max_Thread:
                    for i in range(self.Max_Thread):
                        self.creat_default_thread()
                    wait(self.all_task, return_when=ALL_COMPLETED, timeout=self.Request_Timeout)
                else:
                    for i in range(self.deque_.__len__()):
                        self.creat_default_thread()
                    wait(self.all_task, return_when=ALL_COMPLETED, timeout=self.Request_Timeout)
                if self.Show_Progress_Bar:
                    self.progress_bar(self.all_task_number - self.deque_.__len__(), self.all_task_number)
                else:
                    pass

        else:
            while bool(self.deque_):
                self.all_task = []
                if self.deque_.__len__() >= self.Max_Thread:
                    for t in range(self.Max_Thread):
                        self.creat_title_thread()
                    wait(self.all_task, return_when=ALL_COMPLETED)
                else:
                    for t in range(self.deque_.__len__()):
                        self.creat_title_thread()
                    wait(self.all_task, return_when=ALL_COMPLETED)
                if self.Show_Progress_Bar:
                    self.progress_bar(self.all_task_number - self.deque_.__len__(), self.all_task_number)
                else:
                    pass
        if self.Save_Error_Log and self.error_list != []:
            self.save_log()

    def creat_default_thread(self):
        url_ = self.deque_.popleft()
        if '?' in url_['url']:
            title = url_['url'].split('?')[0].split('/')[-1].split('.')[0]
            format = url_['url'].split('?')[0].split('/')[-1].split('.')[1]
        else:
            title = url_['url'].split('/')[-1].split('.')[0]
            format = url_['url'].split('/')[-1].split('.')[1]
        args = [url_,
                title,
                format]
        self.all_task.append(self.threadpool.submit(lambda p: self.get_(*p), args))

    def creat_title_thread(self):
        url_ = self.deque_.popleft()
        if '?' in url_['url']:
            format = url_['url'].split('?')[0].split('/')[-1].split('.')[1]
        else:
            format = url_['url'].split('/')[-1].split('.')[1]
        args = [url_,
                str(self.title_deque_.popleft()),
                format]
        self.all_task.append(self.threadpool.submit(lambda p: self.get_(*p), args))
