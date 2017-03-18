from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect

from .models import Greeting
from hello.utils.match import Matcher

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    context = {}
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



def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})

