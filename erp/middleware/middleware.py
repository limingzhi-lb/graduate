from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse
from django.contrib.auth.urls import *
from django.contrib.sessions.backends.db import SessionStore

class GetUserModel(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            pass

    def process_response(self, request, response):
        # print(request.session['user'])
        return response


class Row2(MiddlewareMixin):
    def process_request(self,request):
        print("中间件2请求")
        # return HttpResponse("走")

    def process_response(self,request,response):
        print("中间件2返回")
        return response


class Row3(MiddlewareMixin):
    def process_request(self,request):
        print("中间件3请求")

    def process_response(self,request,response):
        print("中间件3返回")
        return response