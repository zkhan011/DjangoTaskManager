# coding: UTF-8
"""streit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin

from django.contrib.auth.views import login, logout

import portal.views as portal
import rnd.views as rnd

from django.conf.urls import include

urlpatterns = [

    url(r'^$', portal.index),

    url(r'^support/?$', portal.support),
    url(r'^sys/search/?$', portal.search),

    url(r'^user/settings', portal.user_settings),

    url(r'^rnd/?$', portal.rnd),
    url(r'^rnd/projects/?$', rnd.projects),
    url(r'^rnd/models/?$', rnd.models_list),

    url(r'^rnd/project/([0-9]*)/?$', rnd.project),
    url(r'^rnd/model/([0-9]*)/?$', rnd.model),

    url(r'^rnd/requests/?$', rnd.requests_list),

    url(r'^rnd/request/create?$', rnd.request_create),

    url(r'^rnd/request/(?P<rid>[0-9]*)/details', rnd.request_details),
    url(r'^rnd/request/(?P<rid>[0-9]*)/delete', rnd.request_delete),

    # Finance
    url(r'^finance/', include('finance.urls')),

    #Portal / Tasks / Projects
    url(r'^', include('portal.urls')),


    #url(r'^cube/(?P<cid>[a-z]{3}[0-9]{2})/rent/(?P<key>[a-zA-Z0-9]*)/?$', sc_g.rent),


    #url(r'^accounts/login/$', login, {'template_name': 'login.html','authentication_form': LoginForm}, name="login"),

    url(r'^user/login$', login, {'template_name': 'login.html'}, name="login"),
    url(r'^user/logout$', logout),

    url(r'^admin/', admin.site.urls),
]
