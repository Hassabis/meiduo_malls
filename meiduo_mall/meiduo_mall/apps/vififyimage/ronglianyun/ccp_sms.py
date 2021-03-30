# 最是人间留不住,朱颜辞镜花辞树
# -*- coding:utf-8 -*-
from CCPRestSDK import REST
# import ConfigParser

accountSid = '8a216da878005a80017880b48e6c2f57'
# 说明：主账号，登陆云通讯网站后，可在控制台首页中看到开发者主账号ACCOUNT SID。

accountToken = '3dcb7fd74b37490c8376b83d7a311fea'
# 说明：主账号Token，登陆云通讯网站后，可在控制台首页中看到开发者主账号AUTH TOKEN。

appId = '8a216da878005a80017880b48f632f5d'
# 请使用管理控制台中已创建应用的APPID。

serverIP = 'app.cloopen.com'
# 说明：请求地址，生产环境配置成app.cloopen.com。

serverPort = '8883'
# 说明：请求端口 ，生产环境为8883.

softVersion = '2013-12-26'  # 说明：REST API版本号保持不变。


def sendTemplateSMS(to, datas, tempId):
    # 初始化REST SDK
    rest = REST(serverIP, serverPort, softVersion)
    rest.setAccount(accountSid, accountToken)
    rest.setAppId(appId)

    result = rest.sendTemplateSMS(to, datas, tempId)
    print(result)


if __name__ == '__main__':
    sendTemplateSMS('18274912702',['123456',10],1)