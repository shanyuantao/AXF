from datetime import datetime

from django.utils.deprecation import MiddlewareMixin

from axf_app.models import UserModel


class AuthMiddleware(MiddlewareMixin):

    def process_request(self, request):

        ticket = request.COOKIES.get('ticket')
        if not ticket:
            pass
        user_ticket = UserModel.objects.filter(ticket=ticket)
        if user_ticket:
            out_time = user_ticket[0].out_time.replace(tzinfo=None)
            now_time = datetime.utcnow()
            if out_time > now_time:
                # 请求中放置键值对
                request.user = user_ticket[0]
            else:
                # 过期了删除用户
                user_ticket[0].delete()