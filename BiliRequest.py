import requests
import json
from fake_useragent import UserAgent
from requests import utils
import qrcode


class BiliRequest:
    qrcode_generate_url = 'https://passport.bilibili.com/x/passport-login/web/qrcode/generate'
    qrcode_poll_url = 'https://passport.bilibili.com/x/passport-login/web/qrcode/poll'
    qrcode_url = ''
    qrcode_key = ''
    refresh_token = ''
    cookies = {}

    request_headers = {
        'User-Agent': UserAgent().chrome,
    }

    # black_list_query_url = 'https://api.bilibili.com/x/relation/modify'
    black_list_add_url = "https://api.bilibili.com/x/relation/batch/modify"

    # 申请二维码
    def getQrcodeData(self):
        # 获取二维码数据
        res = requests.get(self.qrcode_generate_url, headers=self.request_headers)
        # 判断返回状态码
        if res.status_code != 200:
            raise Exception('获取二维码失败，状态码：' + str(res.status_code))
        # 解析返回包体
        data = res.json()
        # 判断返回值
        if data['code'] != 0:
            raise Exception('获取二维码失败，错误信息：' + data['message'])
        # 解析数据
        self.qrcode_url = data['data']['url']
        self.qrcode_key = data['data']['qrcode_key']
        img = qrcode.make(self.qrcode_url)
        img.save('loginqr.png')

    # 获取二维码扫码状态
    def getQrcodeScanData(self):
        res = requests.get(self.qrcode_poll_url, headers=self.request_headers, params={'qrcode_key': self.qrcode_key})
        # 判断返回状态码
        if res.status_code != 200:
            raise Exception('获取二维码扫描状态失败，状态码：' + str(res.status_code))
        # 解析返回数据
        data = res.json()
        if data['code'] != 0:
            raise Exception('获取二维码扫描状态失败，错误信息：' + data['message'])
        # 判断扫码状态
        if data['data']['code'] == 86101:  # 未扫描
            return 86101
        elif data['data']['code'] == 86090:  # 已扫描未确认
            return 86090
        elif data['data']['code'] == 86038:  # 已过期
            return 86038
        elif data['data']['code'] == 0:  # 已确认
            # 获取res里的cookie
            cookie_jar = res.cookies
            self.cookies = requests.utils.dict_from_cookiejar(cookie_jar)
            self.refresh_token = data['data']['refresh_token']
            return 0
        else:
            raise Exception('获取二维码扫描状态失败，错误信息：' + data['message'])

    # 批量拉黑
    def batchBlock(self, uids):
        # 构造请求头
        headers = self.request_headers
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
        # 添加cookie
        headers['Cookie'] = ''.join([f'{k}={v};' for k, v in self.cookies.items()])
        # 构造请求参数
        params = {
            'fids': ','.join(uids),
            'act': 5,
            're_src': 11,
            'csrf': self.cookies.get('bili_jct'),
        }

        res = requests.post(self.black_list_add_url, headers=headers, data=params)
        # 打印请求
        print(res.request.body)
        data = res.json()
        if data['code'] != 0:
            print('批量拉黑失败，错误信息：' + data['message'])
            return
        print("拉黑失败uid列表：" + str(data['data']['failed_fids']))
