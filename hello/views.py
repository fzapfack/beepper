from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect

from .models import Greeting
from hello.utils.match import Matcher
from .models import Question, Answer
from .forms import QuestionForm, AnswerForm


# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    questions = Question.objects.all().order_by("-id")[:5]
    context = {}
    context['questions']=questions
    return render(request, 'index.html', context)


def open_query(request):
    print(request.POST)
    if request.method == 'POST':
        query = request.POST.get('query')
        m = Matcher()
        questions = m.match_question(query)
        context = {'query': query,
                   'questions': questions}
        return render(request, 'index2.html', context)
    else:
        return HttpResponseRedirect('/')


def new_question(request):
    q = Question(src='website')
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=q)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.txt_clean = instance.txt
            instance.save()
            return HttpResponseRedirect('/')
        else:
            pass
    else:
        form = QuestionForm(instance=q)
    context = {
        'form': form,
    }
    return render(request, 'new_question.html', context)


def new_answer(request, question_id=None):
    if 'question_id' not in request.GET:
        return HttpResponse("Une erreur est survenue. Merci de réessayer")
    else:
        question_id = request.GET['question_id']
    a = Answer(src='website', question_id=question_id)
    if request.method == 'POST':
        form = AnswerForm(request.POST, instance=a)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.txt_clean = instance.txt
            instance.save()
            return HttpResponseRedirect('/')
        else:
            pass
    else:
        form = AnswerForm(instance=a)
    context = {
        'form': form,
    }
    return render(request, 'new_answer.html', context)



def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})

