# 内部方法-byte下载器参数过滤器
def donwload_byte_filtering(
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
    '''
    该方法为内部方法，是用于判断设置的参数是否正常，如果输入的参数出现问题，将抛出异常
    '''

    try:
        Max_Thread = int(Max_Thread)
    except:
        raise '设置的MAX_THREAD不为整型'

    try:
        Max_Rerty = int(Max_Rerty)
    except:
        raise '设置的MAX_RETRY不为整型'

    try:
        Time_Sleep = float(Time_Sleep)
    except:
        raise '设置的Time_Sleep不为整型或浮点型'

    try:
        Request_Timeout = float(Request_Timeout)
    except:
        raise '设置的的Request_Timeout不为整型或浮点型'

    if Name_Rules != 'default' and Name_Rules != 'title':
        raise '设置的Name_Rules"{}"并不存在'.format(Name_Rules)
    else:
        pass

    if titles != None and len(titles) == len(urls) and Name_Rules.lower() == 'title':
        pass
    elif titles == None and Name_Rules.lower() == 'default':
        pass
    elif titles == None and Name_Rules.lower() == 'title':
        raise '当前命名模式为title,但并未设置titles'
    elif titles != None and Name_Rules.lower() == 'default':
        raise '当前命名模式为default,但设置了titles'
    elif titles != None and len(titles) != len(urls):
        raise '当前传入的urls与titles的长度不符'
    else:
        pass

    if Save_Error_Log != True and Save_Error_Log != False:
        raise '错误日志保存只可为True或False'
    else:
        pass

    if Show_Progress_Bar != True and Show_Progress_Bar != False:
        raise '进度条设置只可为True或False'
    else:
        pass

    if len(urls) < 1 or urls == None:
        raise '未传入urls或urls为空'
    else:
        pass

    return True
