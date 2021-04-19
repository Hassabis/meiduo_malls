from django.db import DatabaseError
from django.shortcuts import render,redirect,reverse
from django.http import HttpResponse
from django.views import View
from django import http
import re,json,logging
from django.contrib.auth import login,logout,authenticate #authenticate为Django自己提供的登录校验
from users.models import User,Address
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
from meiduo_mall.utlis.views import LoginRequiredJSONMixin




logger = logging.getLogger("django")

class UpdateDestoryAddressView(LoginRequiredJSONMixin, View):
    """更新和删除地址"""

    def put(self, request, address_id):
        """更新地址"""
        # 接收参数
        json_dict = json.loads(request.body.decode())
        receiver = json_dict.get('receiver')
        province_id = json_dict.get('province_id')
        city_id = json_dict.get('city_id')
        district_id = json_dict.get('district_id')
        place = json_dict.get('place')
        mobile = json_dict.get('mobile')
        tel = json_dict.get('tel')
        email = json_dict.get('email')

        # 校验参数
        if not all([receiver, province_id, city_id, district_id, place, mobile]):
            return http.HttpResponseForbidden('缺少必传参数')
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return http.HttpResponseForbidden('参数mobile有误')
        if tel:
            if not re.match(r'^(0[0-9]{2,3}-)?([2-9][0-9]{6,7})+(-[0-9]{1,4})?$', tel):
                return http.HttpResponseForbidden('参数tel有误')
        if email:
            if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
                return http.HttpResponseForbidden('参数email有误')

        # 使用最新的地址信息覆盖指定的旧的地址信息
        try:
            Address.objects.filter(id=address_id).update(
                user=request.user,
                title=receiver,
                receiver=receiver,
                province_id=province_id,
                city_id=city_id,
                district_id=district_id,
                place=place,
                mobile=mobile,
                tel=tel,
                email=email
            )
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'code': 5000, 'errmsg': '修改地址失败'})

        # 响应新的地址信息给前端渲染
        address = Address.objects.get(id=address_id)
        address_dict = {
            "id": address.id,
            "title": address.title,
            "receiver": address.receiver,
            "province": address.province.name,
            "city": address.city.name,
            "district": address.district.name,
            "place": address.place,
            "mobile": address.mobile,
            "tel": address.tel,
            "email": address.email
        }
        return http.JsonResponse({'code': '0', 'errmsg': '修改地址成功', 'address': address_dict})

    def delete(self, request, address_id):
        """删除地址"""
        # 实现指定地址的逻辑删除：is_delete=True
        try:
            address = Address.objects.get(id=address_id)
            address.is_deleted = True
            address.save()
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'code': 5000, 'errmsg': '删除地址失败'})

        # 响应结果：code, errmsg
        return http.JsonResponse({'code':'0', 'errmsg': '删除地址成功'})

class AddressView(LoginRequiredMixin, View):
    """用户收货地址"""

    def get(self, request):
        """查询并展示用户地址信息"""

        # 获取当前登录用户对象
        login_user = request.user
        # 使用当前登录用户和is_deleted=False作为条件查询地址数据
        addresses = Address.objects.filter(user=login_user, is_deleted=False)

        # 将用户地址模型列表转字典列表:因为JsonResponse和Vue.js不认识模型类型，只有Django和Jinja2模板引擎认识
        address_list= []
        for address in addresses:
            address_dict = {
                "id": address.id,
                "title": address.title,
                "receiver": address.receiver,
                "province": address.province.name,
                "city": address.city.name,
                "district": address.district.name,
                "place": address.place,
                "mobile": address.mobile,
                "tel": address.tel,
                "email": address.email
            }
            address_list.append(address_dict)

        # 构造上下文
        context = {
            'default_address_id': login_user.default_address_id,
            'addresses': address_list
        }

        return render(request, 'user_center_site.html', context)
class AddressCreateView(LoginRequiredJSONMixin, View):
    """新增地址"""

    def post(self, reqeust):
        """实现新增地址逻辑"""

        # 判断用户地址数量是否超过上限：查询当前登录用户的地址数量
        # count = Address.objects.filter(user=reqeust.user).count()
        count = reqeust.user.addresses.count()  # 一查多，使用related_name查询
        if count > 20:
            return http.JsonResponse({'code': 4002, 'errmsg': '超出用户地址上限'})

        # 接收参数
        json_str = reqeust.body.decode()
        json_dict = json.loads(json_str)
        receiver = json_dict.get('receiver')
        province_id = json_dict.get('province_id')
        city_id = json_dict.get('city_id')
        district_id = json_dict.get('district_id')
        place = json_dict.get('place')
        mobile = json_dict.get('mobile')
        tel = json_dict.get('tel')
        email = json_dict.get('email')

        # 校验参数
        if not all([receiver, province_id, city_id, district_id, place, mobile]):
            return http.HttpResponseForbidden('缺少必传参数')
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return http.HttpResponseForbidden('参数mobile有误')
        if tel:
            if not re.match(r'^(0[0-9]{2,3}-)?([2-9][0-9]{6,7})+(-[0-9]{1,4})?$', tel):
                return http.HttpResponseForbidden('参数tel有误')
        if email:
            if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
                return http.HttpResponseForbidden('参数email有误')

        # 保存用户传入的地址信息
        try:
            address = Address.objects.create(
                user=reqeust.user,
                title = receiver, # 标题默认就是收货人
                receiver = receiver,
                province_id = province_id,
                city_id = city_id,
                district_id = district_id,
                place = place,
                mobile = mobile,
                tel = tel,
                email = email,
            )

            # 如果登录用户没有默认的地址，我们需要指定默认地址
            if not reqeust.user.default_address:
                reqeust.user.default_address = address
                reqeust.user.save()
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'code': 5000, 'errmsg': '新增地址失败'})

        # 构造新增地址字典数据
        address_dict = {
            "id": address.id,
            "title": address.title,
            "receiver": address.receiver,
            "province": address.province.name,
            "city": address.city.name,
            "district": address.district.name,
            "place": address.place,
            "mobile": address.mobile,
            "tel": address.tel,
            "email": address.email
        }

        # 响应新增地址结果：需要将新增的地址返回给前端渲染
        return http.JsonResponse({'code': "0", 'errmsg': '新增地址成功', 'address': address_dict})
class UserAdderss(LoginRequiredMixin,View):
    def get(self,request):
        return render(request,'user_center_site.html')




class EmailView(LoginRequiredJSONMixin,View):
    """保存用户的邮箱"""
    def put(self,request):
        """接收参数"""
        json_str = request.body.decode()
        json_dict = json.loads(json_str)
        email = json_dict.get("email")

        try:
            request.user.email = email
            request.user.save()
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'code':1,'errmsg':"邮箱保存失败"})

        return http.JsonResponse({"code":0,"errmsg":"OK"})


class UserCenter(LoginRequiredMixin,View):
    def get(self,request):
        context = {
            "username":request.user.username,
            "mobile":request.user.mobile,
            "email":request.user.email,
            "email_active":request.user.email_active
        }
        return render(request,'user_center_info.html',context)


class LogoutView(View):
    def get(self,request):
        response = redirect(reverse("content:index"))
        #退出登录
        logout(request)
        response.delete_cookie("username")

        return response



class LoginUser(View):
    def get(self,request):
        return render(request,'login.html')


    def post(self,request):
        #后台校验,防止恶意用户
        username = request.POST.get("username")
        password = request.POST.get("password")
        remembered = request.POST.get("remembered")
        if not all([username,password]):
            return http.HttpResponseForbidden("缺少必传参数")

        if not re.match(r'[a-zA-Z0-9_-]{5,20}$', username):
            return http.HttpResponseForbidden('请输入5-20位的用户名')

        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            return http.HttpResponseForbidden('请输入8-20位的密码')

        user = authenticate(username = username,password = password)
        if user is None:
            return render(request,'login.html',{"account_errmsg":"账号或密码错误"})

        #状态保持
        login(request,user)
        if remembered != 'on':
            request.session.set_expiry(0)
        else:
            #默认两周
            request.session.set_expiry(None)
        next = request.GET.get("next")
        if next:
            response = redirect(next)

        else:
            response = redirect(reverse("content:index"))
        response.set_cookie('username',user.username,max_age=3600 * 24 * 15)
        return response



class UserNameCount(View):
    def get(self,request,username):
        count = User.objects.filter(username = username).count()
        return http.JsonResponse({"code":0,"errmsg":'OK','count':count})


class PhoneCount(View):
    def get(self,request,mobile):
        count = User.objects.filter(mobile=mobile).count()
        return http.JsonResponse({"code":0,"errmsg":"OK","count":count})

class UsersView(View):
    """用户注册"""
    def get(self,request):
        return render(request,'register.html')

    def post(self,request):
        username = request.POST.get("user_name")
        password = request.POST.get("pwd")
        password2 = request.POST.get("cpwd")
        mobile = request.POST.get("phone")
        allow = request.POST.get("allow")
        #进行后端较校验
        if not all([username,password,password2,mobile,allow]):
            return http.HttpResponseForbidden('缺少参数')

        if not re.match(r'[a-zA-Z0-9_-]{5,20}$',username):
            return http.HttpResponseForbidden('请输入5-20位的用户名')

        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            return http.HttpResponseForbidden('请输入8-20位的密码')

        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return http.HttpResponseForbidden('请输入正确的手机号码')

        if allow != 'on':
            return http.HttpResponseForbidden('请勾选协议')

        # return render(request, 'register.html', {"register_errmes": "注册失败"})

        try:
            user = User.objects.create_user(username=username,password=password,mobile = mobile)
        except DatabaseError:
            return render(request,'register.html',{"register_errmes":"注册失败"})

        login(request,user)

        return redirect(reverse("content:index"))