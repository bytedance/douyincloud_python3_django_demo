from django.http import HttpResponse, Http404, JsonResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import get_object_or_404, render
from .models import Question, Choice
from django.core.cache import cache
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import logging
import json
import requests

logger = logging.getLogger('polls')

@csrf_exempt
def antidirt(request):
    concat = request.POST
    postBody = request.body
    json_result = json.loads(postBody)
    url = 'http://developer.toutiao.com/api/v2/tags/text/antidirt'
    data = {
        'tasks': [
            {
                'content': json_result['content']
            }
        ],
    }
    # 将数据转换为 JSON 格式
    json_data = json.dumps(data)
    # 指定请求头为 JSON
    headers = {'Content-Type': 'application/json'}
    # 发送以 JSON 形式的 POST 请求
    response = requests.post(url, data=json_data, headers=headers)
    # 获取响应内容
    json_result = json.loads(response.content)
    return JsonResponse(json_result)

@csrf_exempt
def openid(request):
    openid = request.META.get('HTTP_X_TT_OPENID')
    result_data = {
        'err_no': 0,
        'err_msg': 'success',
        'data': {
            'openid': openid
        }
    }
    return JsonResponse(result_data)
