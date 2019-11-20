from qcloud_sms.sender import SMSSender

appid = ""
appkey = ""

templ_id = ""
params = ["1234"]
sign = "稻田Tanbo网"

phone_number = "186****8273"


if __name__ == "__main__":
    sender = SMSSender(appid, appkey)
    rsp = sender.send_by_template("86", phone_number, templ_id, params, sign, "", "")
    print(rsp.status_code, rsp.json())
