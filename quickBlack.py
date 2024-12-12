import re
from itertools import islice
from time import sleep

import xlrd
import requests
import json
from fake_useragent import UserAgent
from requests import utils
from BiliRequest import BiliRequest


def chunker(iterable, size):
    """将列表分成多个指定大小的块"""
    iterator = iter(iterable)
    for first in iterator:
        yield [first] + list(islice(iterator, size - 1))


if __name__ == '__main__':
    data = xlrd.open_workbook('./B站直播间机器人_实时更新.xlsx')
    table = data.sheet_by_name('机器人名单')
    blackAddr = table.col_values(2)
    breq = BiliRequest()
    breq.getQrcodeData()
    code = -1
    while code != 0 or code == 86038:
        ncode = breq.getQrcodeScanData()
        if ncode != code:
            if ncode == 86101:
                print('等待扫描二维码')
            if ncode == 86090:
                print('已扫描，请确认')
            if ncode == 86038:
                print('二维码已失效')
                exit(0)
            if ncode == 0:
                print('已登录')
                code = ncode
                break
        code = ncode
        sleep(1)
    if code == 0:
        print(breq.cookies)
    print("需要拉黑：", table.nrows)
    blackUids = []
    for url in blackAddr[1:]:
        match = re.search(r"bilibili\.com/(\d+)/", url)
        if match:
            blackUids.append(match.group(1))
    for i, group in enumerate(chunker(blackUids, 20), start=1):
        # 这里可以执行你的操作，例如：
        print(f"处理第{i}组: {', '.join(group)}")
        # 执行你的操作，例如 API 请求等
        breq.batchBlock(group)
        sleep(1)
    print("拉黑完成")
