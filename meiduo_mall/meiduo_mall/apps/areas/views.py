from django.shortcuts import render
from django.views import View
from areas.models import Area
from django import http
from django.core.cache import cache
import logging
# Create your views here.

logger = logging.getLogger("django")
class AreaView(View):
    def get(self, request):
        # 判断当前是要查询省份数据还是市区数据
        area_id = request.GET.get('area_id')

        if not area_id:
            # 获取并判断是否有缓存
            province_list = cache.get('province_list')

            if not province_list:
                # 查询省级数据
                try:
                    province_model_list = Area.objects.filter(parent__isnull=True)

                    # 需要将模型列表转成字典列表
                    province_list = []
                    for province_model in province_model_list:
                        province_dict = {
                            "id": province_model.id,
                            "name": province_model.name
                        }
                        province_list.append(province_dict)

                    # 缓存省份字典列表数据:默认存储到别名为"default"的配置中
                    cache.set('province_list', province_list, 3600)
                except Exception as e:
                    logger.error(e)
                    return http.JsonResponse({'code': 5000, 'errmsg': '查询省份数据错误'})

            # 响应省级JSON数据
            return http.JsonResponse({'code': '0', 'errmsg': 'OK', 'province_list': province_list})
        else:
            #查询城市区县级数据
            parent_model = Area.objects.get(id = area_id)
            sub_model_list = parent_model.subs.all()

            subs = []
            for i in sub_model_list:
                sub_dict = {
                    "id":i.id,
                    "name":i.name
                }
                subs.append(sub_dict)

            sub_data = {
                "id":parent_model.id,
                "name":parent_model.name,
                "subs":subs
            }

            return http.JsonResponse({'code':0,'errmsg':'OK','sub_data':sub_data})