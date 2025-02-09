import hashlib
import random
from qcloud_sms import tools

class SMSSender:
    """ 发送单条短信"""
    appid = 0
    appkey = ""
    url = "https://yun.tim.qq.com/v5/tlssmssvr/sendsms"

    def __init__(self, appid, appkey):
        self.appid = appid
        self.appkey = appkey

    def send_msg(self, sms_type, nation_code, phone_number, msg, extend, ext):
        """ 普通群发接口
        明确指定内容，如果有多个签名，请在内容中以【】的方式添加到信息内容中，否则系统将使用默认签名

        Args:
            sms_type: 短信类型，0 为普通短信，1 为营销短信
            nation_code: 国家码，如 86 为中国
            phone_number: 不带国家码的手机号
            msg: 信息内容，必须与申请的模板格式一致，否则将返回错误
            extend: 扩展码，可填空串
            ext: 服务端原样返回的参数，可填空串

	Request Data:
            {
                "tel": {
                    "nationcode": "86",
                    "mobile": "13788888888"
                },
                "type": 0,
                "msg": "你的验证码是1234",
                "sig": "fdba654e05bc0d15796713a1a1a2318c",
                "time": 1479888540,
                "extend": "",
                "ext": ""
            }

	Response:

            {
                "result": 0,
                "errmsg": "OK",
                "ext": "",
                "sid": "xxxxxxx",
                "fee": 1
            }
        """
        rnd = tools.get_random()
        cur_time = tools.get_cur_time()

        data = {}

        tel = {"nationcode": nation_code, "mobile": phone_number}
        data["tel"] = tel
        data["type"] = sms_type
        data["msg"] = msg
        data["sig"] = hashlib.sha256("appkey=" + self.appkey + "&random=" + str(rnd)
                                     + "&time=" + str(cur_time) + "&mobile=" + phone_number).hexdigest()
        data["time"] = cur_time
        data["extend"] = extend
        data["ext"] = ext

        url = "{url}?sdkappid={appid}&random={rnd}".format(url=self.url, appid=self.appid, rnd=rnd)
        return tools.send_request(url, data)

    def send_by_template(self, nation_code, phone_number, templ_id, params, sign, extend, ext):
        """ 指定模板单发

        Args:
            nation_code: 国家码，如 86 为中国
            phone_number: 不带国家码的手机号
            templ_id: 模板 id
            params: 模板参数列表，如模板 {1}...{2}...{3}，那么需要带三个参数
            sign: 签名，如果填空串，系统会使用默认签名
            extend: 扩展码，可填空串
            ext: 服务端原样返回的参数，可填空串

        Returns:
            json string { "result": xxxx, "errmsg": "xxxxx" ... }，被省略的内容参见协议文档
            请求包体
            {
                "tel": {
                    "nationcode": "86",
                    "mobile": "13788888888"
                },
                "sign": "腾讯云",
                "tpl_id": 19,
                "params": [
                    "验证码",
                    "1234",
                    "4"
                ],
                "sig": "fdba654e05bc0d15796713a1a1a2318c",
                "time": 1479888540,
                "extend": "",
                "ext": ""
            }
            应答包体
            {
                "result": 0,
                "errmsg": "OK",
                "ext": "",
                "sid": "xxxxxxx",
                "fee": 1
            }
        """
        rnd = tools.get_random()
        cur_time = tools.get_cur_time()

        data = {}

        tel = {"nationcode": nation_code, "mobile": phone_number}
        data["tel"] = tel
        data["tpl_id"] = templ_id
        data["sign"] = sign
        data["sig"] = tools.calculate_sig(self.appkey, rnd, cur_time, phone_number)
        data["params"] = params
        data["time"] = cur_time
        data["extend"] = extend
        data["ext"] = ext

        url = "{url}?sdkappid={appid}&random={rnd}".format(url=self.url, appid=self.appid, rnd=rnd)
        return tools.send_request(url, data)


class SMSBatchSender:
    """ 群发短信"""
    appid = 0
    appkey = ""
    url = "https://yun.tim.qq.com/v5/tlssmssvr/sendmultisms2"

    def __init__(self, appid, appkey):
        self.appid = appid
        self.appkey = appkey

    def send_msg(self, sms_type, nation_code, phone_numbers, msg, extend, ext):
        """ 普通群发
        【注意】海外短信没有群发功能

        Args:
            sms_type: 短信类型，0 为普通短信，1 为营销短信
            nation_code: 国家码，如 86 为中国
            phone_numbers: 不带国家码的手机号列表
            msg: 信息内容，必须与申请的模板格式一致，否则将返回错误
            extend: 扩展码，可填空串
            ext: 服务端原样返回的参数，可填空串

        Returns:
            json string { "result": xxxx, "errmsg": "xxxxx" ... }，被省略的内容参见协议文档

        请求包体
        {
            "tel": [
                {
                    "nationcode": "86",
                    "mobile": "13788888888"
                },
                {
                    "nationcode": "86",
                    "mobile": "13788888889"
                }
            ],
            "type": 0,
            "msg": "你的验证码是1234",
            "sig": "fdba654e05bc0d15796713a1a1a2318c",
            "time": 1479888540,
            "extend": "",
            "ext": ""
        }
        应答包体
        {
            "result": 0,
            "errmsg": "OK",
            "ext": "",
            "detail": [
                {
                    "result": 0,
                    "errmsg": "OK",
                    "mobile": "13788888888",
                    "nationcode": "86",
                    "sid": "xxxxxxx",
                    "fee": 1
                },
                {
                    "result": 0,
                    "errmsg": "OK",
                    "mobile": "13788888889",
                    "nationcode": "86",
                    "sid": "xxxxxxx",
                    "fee": 1
                }
            ]
        }
        """
        rnd = tools.get_random()
        cur_time = tools.get_cur_time()

        data = {}

        data["tel"] = tools.phone_numbers_to_list(nation_code, phone_numbers)
        data["type"] = sms_type
        data["msg"] = msg
        data["sig"] = tools.calculate_sig(self.appkey, rnd, cur_time, phone_numbers)
        data["time"] = cur_time
        data["extend"] = extend
        data["ext"] = ext

        url = "{url}?sdkappid={appid}&random={rnd}".format(url=self.url, appid=self.appid, rnd=rnd)
        return tools.send_request(url, data)

    def send_by_template(self, nation_code, phone_numbers, templ_id, params, sign, extend, ext):
        """ 指定模板群发
        【注意】海外短信没有群发功能

        Args:
            nation_code: 国家码，如 86 为中国
            phone_numbers: 不带国家码的手机号列表
            templ_id: 模板 id
            params: 模板参数列表，如模板 {1}...{2}...{3}，那么需要带三个参数
            sign: 签名，如果填空串，系统会使用默认签名
            extend: 扩展码，可填空串
            ext: 服务端原样返回的参数，可填空串

        Returns:
            json string { "result": xxxx, "errmsg": "xxxxx" ... }，被省略的内容参见协议文档
        请求包体
        {
            "tel": {
                "nationcode": "86",
                "mobile": "13788888888"
            },
            "sign": "腾讯云",
            "tpl_id": 19,
            "params": [
                "验证码",
                "1234",
                "4"
            ],
            "sig": "fdba654e05bc0d15796713a1a1a2318c",
            "time": 1479888540,
            "extend": "",
            "ext": ""
        }
        应答包体
        {
            "result": 0,
            "errmsg": "OK",
            "ext": "",
            "detail": [
                {
                    "result": 0,
                    "errmsg": "OK",
                    "mobile": "13788888888",
                    "nationcode": "86",
                    "sid": "xxxxxxx",
                    "fee": 1
                },
                {
                    "result": 0,
                    "errmsg": "OK",
                    "mobile": "13788888889",
                    "nationcode": "86",
                    "sid": "xxxxxxx",
                    "fee": 1
                }
            ]
        }
        """
        rnd = tools.get_random()
        cur_time = tools.get_cur_time()

        data = {}

        data["tel"] = tools.phone_numbers_to_list(nation_code, phone_numbers)
        data["sign"] = sign
        data["sig"] = tools.calculate_sig(self.appkey, rnd, cur_time, phone_numbers)
        data["tpl_id"] = templ_id
        data["params"] = params
        data["time"] = cur_time
        data["extend"] = extend
        data["ext"] = ext

        url = "{url}?sdkappid={appid}&random={rnd}".format(url=self.url, appid=self.appid, rnd=rnd)
        return tools.send_request(url, data)
