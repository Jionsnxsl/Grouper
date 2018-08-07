from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r'^fishes/', include(fishes.site.urls)),
    url(r'^$', views.Homepage, name="homepage"),
    url(r'^search-result/', views.SearchView, name="search_view"),
    url(r'^admin/$', views.AdminView, name="admin_view"),
    url(r'^admin/productinfo/$', views.ProductInfoView, name="productinfo"),
    url(r'^admin/productdetail/$', views.ProductDetailView.as_view(), name="productdetail"),
    url(r'^admin/imageupload/$', views.ImageUploadView, name="imageupload"),

    # 用户相关(START)
    url(r'^admin/userinfo/$', views.UserInfoView, name="userinfo"),
    url(r'^admin/userdetail/(?P<uid>\d+)/$', views.UserDetailView, name="userdetail"),
    url(r'^admin/adduser/$', views.AddUserView.as_view(), name="adduser"),
    url(r'^admin/deleteuser/$', views.DeleteUserView, name="deleteuser"),
    # 用户相关(END)

    # 鱼池相关(START)
    url(r'^admin/fishpoolinfo/$', views.FishPoolInfoView, name="fishpoolinfo"),
    url(r'^admin/generateqrcode/(?P<key>\w+)-(?P<pid>\d+)$', views.GenerateQRCode, name="generateqrcode"),
    url(r'^admin/addfishpool/$', views.AddFishPoolView.as_view(), name="addfishpool"),
    url(r'^admin/deletefishpool/$', views.DeleteFishPool, name="deletefishpool"),
    # 鱼池相关(END)

    # 手机端(START)
    # url(r'^admin/m/main/$', views.MobileMainPage, name="mainpage"),
    url(r'^admin/m/fishpool/$', views.FishPoolView.as_view(), name="fishpool"),
    url(r'^admin/m/addproduct/$', views.AddProductView, name="addproduct"),
    url(r'^admin/m/transproduct/$', views.TranProductView.as_view(), name="tranproduct"),
    url(r'^admin/m/processproduct/$', views.ProcessProductView.as_view(), name="processproduct"),
    # 手机端(END)

    url(r'^admin/generateercode/$', views.GenerateERCodeView, name="generateercode"),
    url(r'^admin/thirdtestreport/$', views.ThirdPartTestReportView, name="thirdtestreport"),
    url(r'^admin/variety/$', views.VarietyView, name="variety"),
    url(r'^admin/addvariety/$', views.AddVarietyView, name="addvariety"),
    url(r'^admin/delvariety/$', views.DelVarietyView, name="delvariety"),
    url(r'^admin/feedbacknotreply/$', views.FeedbackNOTReplyView, name="feedbacknotreply"),
    url(r'^admin/feedbackreply/$', views.FeedbackReplyView, name="feedbackreply"),
    url(r'^admin/syssethomepage/$', views.SysSetForHomepageView, name="syssethomepage"),
    url(r'^admin/syssetsearchresult/$', views.SysSetForSearchResultView, name="syssetsearchresult"),
]