from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r'^fishes/', include(fishes.site.urls)),
    url(r'^$', views.homepage, name="homepage"),
    url(r'^search-result/', views.search_view, name="search_view"),
    url(r'^admin/$', views.adminView, name="admin_view"),
    url(r'^admin/productinfo/$', views.ProductInfoView, name="productinfo"),
]