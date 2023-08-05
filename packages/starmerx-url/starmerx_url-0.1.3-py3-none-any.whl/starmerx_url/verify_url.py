# !/usr/bin/env python
# -*- coding: UTF-8 -*-
import json
import re

from django.http import HttpResponse
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin

white_url_list = list()

reg1_compile = r"192\.168\.\d{1,3}.\d{1,3}"
reg2_compile = r"192\.168\.1.\d{1,3}"
remote_addr_real_host = ""
referer_host = ""

if hasattr(settings, "WHITE_URL_LIST"):
    white_url_list = settings.WHITE_URL_LIST

if hasattr(settings, "COMPILE_REG1"):
    reg1_compile = settings.COMPILE_REG1

if hasattr(settings, "COMPILE_REG2"):
    reg2_compile = settings.COMPILE_REG2

if hasattr(settings, "REMOTE_ADDR_REAL"):
    remote_addr_real_host = settings.REMOTE_ADDR_REAL

if hasattr(settings, "REFERER_HOST"):
    referer_host = settings.REFERER_HOST


class AuthEffectMiddleware(MiddlewareMixin):

    def validate_remote(self, request):
        remote_addr = request.META.get("REMOTE_ADDR", "")
        remote_addr_real = request.META.get("HTTP_X_REAL_IP", "")
        referer = request.META.get("HTTP_REFERER", "")
        reg2 = re.compile(reg2_compile)
        reg1 = re.compile(reg1_compile)

        if referer_host:
            return re.match(reg2, remote_addr) or \
                   re.match(reg1, remote_addr_real) or \
                   remote_addr_real == remote_addr_real_host or \
                   referer_host in referer

        return re.match(reg2, remote_addr) or \
               re.match(reg1, remote_addr_real) or \
               remote_addr_real == remote_addr_real_host

    def process_view(self, request, view_func, view_args, view_kwargs):
        user = request.user
        if (user and user.is_authenticated) or self.validate_remote(request) \
                or 'login' in request.path or 'logout' in request.path \
                or request.path in white_url_list:
            pass
        else:
            wrapper = {
                'code': 401,
                'msg': '请先登录或内网访问数据'
            }
            no_auth_res = HttpResponse(json.dumps(wrapper), status=401, content_type='application/json')
            return no_auth_res
