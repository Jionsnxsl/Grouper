from django.conf.urls import url
from . import views
from django.contrib.auth.views import login, logout

urlpatterns = [
    # url(r'^fishes/', include(fishes.site.urls)),
    url(r'^login/', login, {'template_name': 'users/login.html'}, name="login"),
    # 没有测试！！！！！
    url(r'^logout/', logout, {'template_name': 'users/login.html'}, name="logout"),
    url(r'^findpwd/', views.FindPasswordView.as_view(), name="find_password"),
]
