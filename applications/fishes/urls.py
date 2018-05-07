from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r'^fishes/', include(fishes.site.urls)),
    url(r'^$', views.homepage, name="homepage"),
    url(r'^search-result/', views.search_view, name="search_view"),
    url(r'^admin/$', views.adminView, name="admin_view"),
    url(r'^admin/productinfo/$', views.productInfoView, name="productinfo"),

    # 用户相关(START)
    url(r'^admin/userinfo/$', views.userInfoView, name="userinfo"),
    url(r'^admin/userdetail/(?P<uid>\d+)/$', views.userDetailView, name="userdetail"),
    url(r'^admin/adduser/$', views.AddUserView.as_view(), name="adduser"),
    url(r'^admin/deleteuser/$', views.deleteUserView, name="deleteuser"),
    # 用户相关(END)

    # 鱼池相关(START)
    url(r'^admin/fishpoolinfo/$', views.fishPoolInfoView, name="fishpoolinfo"),
    url(r'^admin/fishpooldetail/(?P<pid>\d+)$', views.fishPoolDetailView, name="fishpooldetail"),
    url(r'^admin/addfishpool/$', views.AddFishPoolView.as_view(), name="addfishpool"),
    url(r'^admin/deletefishpool/$', views.deleteFishPool, name="deletefishpool"),
    # 鱼池相关(END)

    url(r'^admin/generateercode/$', views.generateERCodeView, name="generateercode"),
    url(r'^admin/thirdtestreport/$', views.thirdPartTestReportView, name="thirdtestreport"),
    url(r'^admin/feedbacknotreply/$', views.feedbackNOTReplyView, name="feedbacknotreply"),
    url(r'^admin/feedbackreply/$', views.feedbackReplyView, name="feedbackreply"),
    url(r'^admin/syssethomepage/$', views.sysSetForHomepageView, name="syssethomepage"),
    url(r'^admin/syssetsearchresult/$', views.sysSetForSearchResultView, name="syssetsearchresult"),
]