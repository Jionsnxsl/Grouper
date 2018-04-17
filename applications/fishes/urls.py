from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.homepage, name="homepage"),
    url(r'^search-result/', views.search_view, name="search_view"),
]