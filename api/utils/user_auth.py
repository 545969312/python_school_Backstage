from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from api import models


class UserAuthentication(BaseAuthentication):

    def authenticate(self, request):
        """
        用户认证
        :param request:
        :return:
        """
        token = request.query_params.get('token')
        token_obj = models.UserToken.objects.filter(token=token).first()
        if not token_obj:
            raise AuthenticationFailed({'code': 0, 'error': '认证失败'})
        # 认证成功
        return (token_obj.user, token_obj)