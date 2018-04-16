from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.homepage, name="homepage"),
]