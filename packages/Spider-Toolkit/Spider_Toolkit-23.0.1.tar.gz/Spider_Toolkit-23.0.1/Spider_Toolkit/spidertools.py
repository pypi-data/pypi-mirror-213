from .tools import Download_byte
from .engine import Parameter_filtering_engine


def download_byte(
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
        Show_Progress_Bar: bool = False
):
    '''
    :param Max_Thread: 最大线程数
    :param Max_Rerty: 最大重试数
    :param Time_Sleep: 每轮休眠时间
    :param Request_Timeout: 请求超时时间
    :param urls: url列表或单个url
    :param headers: 请求头
    :param cookie: cookie
    :param param: param
    :param data: data
    :param proxies: 代理
    :param verify: verify
    :param path_: 保存路径
    :param Name_Rules: 命名规则
    :param titles: 标题
    :param Save_Error_Log: 保存失败日志
    :param Show_Progress_Bar: 显示进度条
    :return: 下载器对象
    '''
    if Parameter_filtering_engine.donwload_byte_filtering(
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
    ):
        if len(urls) == 1 or Max_Thread==0:
            return Download_byte.download_byte(
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
                Show_Progress_Bar=Show_Progress_Bar)
        else:
            return Download_byte.thread_download_byte(
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
                Show_Progress_Bar=Show_Progress_Bar)
    else:
        pass
