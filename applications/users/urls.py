from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r'^fishes/', include(fishes.site.urls)),
    url(r'^login/', views.LoginView.as_view(), name="login"),
    url(r'^findpwd/', views.FindPasswordView.as_view(), name="find_password"),
]
