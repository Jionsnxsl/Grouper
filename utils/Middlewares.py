from django.http import HttpResponseRedirect
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from re import compile

EXEMPT_URLS = [compile(settings.LOGIN_URL.lstrip('/'))]
if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
    EXEMPT_URLS += [compile(expr) for expr in settings.LOGIN_EXEMPT_URLS]

# 参考：https://python-programming.com/recipes/django-require-authentication-pages/
class LoginRequiredMiddleware(MiddlewareMixin):
    """
    Middleware that requires a user to be authenticated to view any page other
    than LOGIN_URL. Exemptions to this requirement can optionally be specified
    in settings via a list of regular expressions in LOGIN_EXEMPT_URLS (which
    you can copy from your urls.py).

    Requires authentication middleware and template context processors to be
    loaded. You'll get an error if they aren't.
    """

    def process_request(self, request):
        assert hasattr(request, 'user'), "The Login Required middleware\
                requires authentication middleware to be installed. Edit your\
                MIDDLEWARE_CLASSES setting to insert\
                'django.contrib.auth.middlware.AuthenticationMiddleware'. If that doesn't\
                work, ensure your TEMPLATE_CONTEXT_PROCESSORS setting includes\
                'django.core.context_processors.auth'."
        if not request.user.is_authenticated():
            # TODO_fix : 这里发现一个BUG，request.path只获取了访问路径，没有获取访问参数，如果登录的时候是个GET请求就会出错
            url_full = request.build_absolute_uri()   # 可以获取完整路径
            pattern = compile(r'.*?/(\?.*)')
            result = pattern.match(url_full)
            args = ""
            if result:
                # print("match:", )
                args = result.group(1)
            path = request.path_info.lstrip('/') + args
            # print(path)
            if not any(m.match(path) for m in EXEMPT_URLS):
                return HttpResponseRedirect(settings.LOGIN_URL+"?next=/"+path)
