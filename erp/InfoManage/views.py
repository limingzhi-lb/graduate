from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


# def index(request):
#     return render(request, 'base.html')
from .models import PredictData
from rest_framework.response import Response
from rest_framework.views import APIView
from script.predict import main
from .models import PredictData
# 返回整数，例如 1.1 为 1.1%
class index(APIView):
    queryset = PredictData.objects.all()
    # 这里是一个get请求
    def get(self, request, *args, **kwargs):
        data = main()
        print(data)
        # return Response('Day,产品1,产品2\n05/22/2018,4,4\n05/23/2018,4,5\n05/24/2018,2,2\n')
        return Response(data)
