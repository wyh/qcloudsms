# 腾讯云SMS Python3 SDK
代码修改自： `samhjn/qcloudsms-python3`

目标是初始化后立即可以使用

这个项目尝试用很简单的代码完成绝大部分功能，删除了语音这些很少用到的东西，
特别是变更了原代码中糟糕的class 命名，已经不使用默认的 requests 来发送请求，
做很多复杂的包装；


### 用法

```python
import json
from sms.sms import SMSSender

appid = 1000000
appkey = "ffffffffffffffffffffffffff"  
sender = SMSSender(appid, appkey)

templ_id = 20000
phone_number = "132xxxxxxxx"
params = ["赋影", "100.00"]
rsp = sender.send_by_template("86", phone_number, templ_id, params, "", "", "")
print(rsp.results)
```

其余功能的具体使用与官方SDK类似，可以参考[官方SDK使用样例](https://github.com/qcloudsms/qcloudsms/blob/master/demo/python/main.py)。

**注意:** 这个例子引入SDK的方式和官方文档有所不同，目录结构较官方文档也少一层，使用的时候需自行注意这些问题。
