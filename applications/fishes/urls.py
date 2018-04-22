from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r'^fishes/', include(fishes.site.urls)),
    url(r'^$', views.homepage, name="homepage"),
    url(r'^search-result/', views.search_view, name="search_view"),
    url(r'^admin/$', views.adminView, name="admin_view"),
    url(r'^admin/productinfo/$', views.productInfoView, name="productinfo"),
    url(r'^admin/userinfo/$', views.userInfoView, name="userinfo"),
    url(r'^admin/adduser/$', views.addUserView, name="adduser"),
    url(r'^admin/fishpoolinfo/$', views.fishPoolInfoView, name="fishpoolinfo"),
    url(r'^admin/addfishpool/$', views.addFishPoolView, name="addfishpool"),
]