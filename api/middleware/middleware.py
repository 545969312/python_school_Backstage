from django.utils.deprecation import MiddlewareMixin

# 解决跨域问题，简单的模式直接加header=‘Access-Control-Allow-Origin’


class CorsMiddleware(MiddlewareMixin):

    def process_response(self, request, response):
        response['Access-Control-Allow-Origin'] = 'http://localhost:8080'
        if request.method == "OPTIONS":
            response["Access-Control-Allow-Methods"] = "POST,PUT,DELETE"
            response["Access-Control-Allow-Headers"] = "Content-Type"
        return response