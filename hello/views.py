from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect

from .models import Greeting

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    context = {}
    return render(request, 'index.html', context)

def open_query(request):
    print(request.POST)
    if request.method == 'POST':
        query = request.POST.get('query')
        return HttpResponse(query)
    else:
        return HttpResponseRedirect('/')



def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})

