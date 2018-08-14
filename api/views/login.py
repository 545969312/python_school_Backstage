import uuid
from api import models
from api.utils.response import BaseResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ViewSetMixin


class Login(ViewSetMixin, APIView):
    def login(self, request, *args, **kwargs):
        res = BaseResponse()
        try:
            user = request.data.get('username')
            pwd = request.data.get('password')
            user_obj = models.Account.objects.filter(username=user, password=pwd).first()
            if not user_obj:
                res.code = 0
                res.error = '用户名或者密码错误'
            uid = uuid.uuid4()
            # 把token写进数据库，有则更改，无则添加
            models.UserToken.objects.update_or_create(user=user_obj, defaults={'token': uid})
            res.data = uid
        except Exception as e:
            res.code = 0
            res.error = '登陆失败'
        return Response(res.dict)