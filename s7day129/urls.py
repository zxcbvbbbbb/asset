"""s7day129 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include

from django.contrib import admin
from api.views import views,jira
from django.views import View
from django.conf.urls.static import static
from s7day129 import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^api/v1/auth/$', views.AuthView.as_view()),
    # url(r'^api/v1/order/$', views.OrderView.as_view()),
    # url(r'^api/v1/info/$', views.UserInfoView.as_view()),
    url(r'^client/create/$',views.ClientCreateView.as_view(),name="client_create"),
    url(r'^ajax/load_cities/$',views.ajax_load_cities,name="ajax_load_cities"),
    url(r'^load_models/$',views.load_models,name="load_models"),
    # url(r'^posttest/$',views.posttest,name="posttest"),
    # url(r'^test/$',views.Test.as_view(),name="test"),
    url(r'^$', views.index, name="index"),
    url(r'^modal/$', views.modal, name="modal"),
    #url(r'^reg/$', views.addnew, name="reg"),
    #url(r'^dropuser/$', views.dropuser, name="dropuser"),
    url(r'^login/$', views.login, name="login"),
    url(r'^logout/$', views.logout, name="logout"),
    url(r'^classes/$', views.handle_classes, name="classes"),
    url(r'^edit_class/$', views.edit_class, name="edit_class"),
    url(r'^del_consul/$', views.del_consul, name="del_consul"),
    url(r'^teacher/$', views.handle_teacher, name="teacher"),
    url(r'^edit_teacher-(\d+)/$', views.edit_teacher, name="edit_teacher"),
    url(r'^add_teacher/$', views.add_teacher, name="add_teacher"),
    url(r'^asset-(?P<mod__type_id>\d+)-(?P<status>\d+)/$', views.handle_asset, name="asset"),
    url(r'asset-json',views.AssetJsonView.as_view(),name='asset-json'),
    url(r'asset-detail-(?P<asset_nid>\d+)',views.AssetDetail.as_view(),name='asset-detail'),
    url(r'^edit_asset/$', views.edit_asset, name="edit_asset"),
    url(r'^del_asset/$', views.del_asset, name="del_asset"),
    url(r'^clear_asset/$', views.clear_asset, name="clear_asset"),
    url(r'^add_asset/$', views.add_asset, name="add_asset"),
    url(r'^add_Arecord/$', views.add_Arecord, name="add_Arecord"),
    url(r'^add_configure/$', views.add_configure, name="add_configure"),
    url(r'^add_model/$', views.add_model, name="add_model"),
    url(r'^add_employee/$', views.add_employee, name="add_employee"),
    url(r'^upload/$', views.upload, name="upload"),
    url(r'^search/$', views.search, name="search"),
    url(r'^add_consul/$', views.add_consul, name="add_consul"),
    #url(r'^compare/$', views.compare, name="compare"),
    url(r'^blur/$', views.blur, name="blur"),
    url(r'^ftp/$', views.ftp, name="ftp"),
    url(r'^test/$', views.test, name="test"),
    # url(r'^test-json/$', views.TestJsonView),
    url(r'^insert/$', views.insert, name="insert"),
    url(r'^jquery/$', views.jquery, name="jquery"),
    url(r'^tab/$', views.tab, name="tab"),
    url(r'^top/$', views.top, name="top"),
    url(r'^ipinfo/$', views.ipinfo, name="ipinfo"),
    url(r'^staff_month/$', jira.staff_month, name="staff_month"),
    url(r'^staff_season/$', jira.staff_season, name="staff_season"),
    url(r'^bug_count/$', jira.bug_count, name="bug_count"),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
