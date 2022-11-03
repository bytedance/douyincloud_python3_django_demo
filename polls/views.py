from django.http import HttpResponse, Http404, JsonResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import get_object_or_404, render
from .models import Question, Choice
from django.core.cache import cache
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import logging

logger = logging.getLogger('polls')

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

def question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/question.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    logger.info(question.question_text)
    for choice in question.choice_set.all():
        logger.info(choice.choice_text)
    return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/vote.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

@csrf_exempt
def redis(request, key):
    result_data = {
        'err_no': 0,
        'err_msg': 'success',
        'data': {
            'key': key,
            'value': cache.get(key)
        }
    }
    return JsonResponse(result_data)

@csrf_exempt
def redis_add(request, key, value):
    cache.set(key, value)
    result_data = {
        'err_no': 0,
        'err_msg': 'success'
    }
    return JsonResponse(result_data)

@csrf_exempt
def openid(request):
    openid = request.headers['X-TT-OPENID']
    result_data = {
        'err_no': 0,
        'err_msg': 'success',
        'data': {
            'openid': openid
        }
    }
    return JsonResponse(result_data)
