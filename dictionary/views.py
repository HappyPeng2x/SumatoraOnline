from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from dictionary.forms import SearchForm

import dictionary.queries as q

def index(request):
    return HttpResponse("Hello, world. You're at the dictionary index.")

def results(request, term):
    results = q.execute(term, 0, 30)

    context = { 'results':results, 'term':term}
    
    return render(request, 'dictionary/results.html', context)

def search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)

        if form.is_valid():
            return HttpResponseRedirect(reverse('results',  kwargs={'term':form.clean_expression()}))                                        
    else:
        form = SearchForm()

    context = { 'form':form }

    return render(request, 'dictionary/search.html', context)
