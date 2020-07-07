from django.shortcuts import render, redirect
from django import forms
from django.http import HttpResponse
from re import search

from . import util

class SearchForm(forms.Form):
    title = forms.CharField(label=False)


def index(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            if util.get_entry(title): # Check is title contains an existing entry.
                return redirect('wiki:entry', title=title)
            else:
                return redirect('wiki:search_result', title=title)
    else:
        context = {"entries": util.list_entries(), "form": SearchForm()}
        return render(request, "encyclopedia/index.html", context)


def entry(request, title):
    context = {"entry": util.get_entry(title), "title": title, "form": SearchForm()}
    return render(request, "encyclopedia/entry.html", context)


def search_result(request, title):
    entries = util.substring_search(title)
    context = {"form": SearchForm(), "entries": entries, "title": title}
    return render(request, "encyclopedia/search_result.html", context)