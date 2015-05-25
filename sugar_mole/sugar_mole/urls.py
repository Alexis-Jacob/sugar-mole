from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework import routers
import api.views as views

urlpatterns = patterns('',
    url(r'^api/user/', views.UserView.as_view()),
    url(r'^api/scenario/', views.ScenarioView.as_view()),
    url(r'^api/condition/', views.ConditionView.as_view()),
    url(r'^api/action/', views.ActionView.as_view()),
    url(r'^api/house/(?P<uuid>\S+)/$', views.HouseView.as_view()),
    url(r'^api/house/', views.HouseView.as_view()),
    url(r'^api/apiDetails/', views.APIDetails.as_view()),
    url(r'^api/devicesInfo/', views.DevicesInfos.as_view()),
    url(r'^docs/', include('rest_framework_swagger.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
)
