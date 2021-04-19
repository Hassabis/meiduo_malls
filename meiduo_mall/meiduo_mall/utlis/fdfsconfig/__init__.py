# 最是人间留不住,朱颜辞镜花辞树
# -*- coding:utf-8 -*-
import fdfs_client.client
from fdfs_client.client import Fdfs_client
conf = fdfs_client.client.get_tracker_conf(r'C:\projects\meiduo_malls\meiduo_mall\meiduo_mall\utlis\fdfsconfig\client.conf')
client = Fdfs_client(conf)
ret = client.upload_by_filename('C:\服务器接收数据\csdn161266885678721146.jpg')
print(ret)
