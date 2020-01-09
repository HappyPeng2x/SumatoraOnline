from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from dictionary.forms import SearchForm
from dictionary.models import DictionaryDisplayElement

def index(request):
    return HttpResponse("Hello, world. You're at the dictionary index.")

def results(request, term):
    query = """
SELECT
  1 AS entryOrder,
  DictionaryEntry.seq,
  DictionaryEntry.readingsPrio, 
  DictionaryEntry.readings, 
  DictionaryEntry.writingsPrio,
  DictionaryEntry.writings,
  DictionaryEntry.pos,
  DictionaryEntry.xref,
  DictionaryEntry.ant,
  DictionaryEntry.misc, 
  DictionaryEntry.lsource,
  DictionaryEntry.dial,
  DictionaryEntry.s_inf, 
  DictionaryEntry.field,
  DictionaryTranslation.lang,
  DictionaryTranslation.gloss
FROM
  jmdict.DictionaryEntry, 
  eng.DictionaryTranslation
WHERE
  DictionaryEntry.seq = DictionaryTranslation.seq AND
  DictionaryEntry.seq IN
  (SELECT DictionaryIndex.`rowid`
   FROM DictionaryIndex
   WHERE writingsPrio MATCH %s)"""

    results = DictionaryDisplayElement.objects.raw(query, [term])

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
