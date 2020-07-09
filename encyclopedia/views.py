from django.shortcuts import render, redirect
from django import forms
from django.http import HttpResponse
from re import search

from . import util

class SearchForm(forms.Form):
    title = forms.CharField(label=False)


class NewEntryForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Title'}), label=False)
    text = forms.CharField(widget=forms.Textarea(attrs={'cols':100, 'rows':10, 'placeholder': 'Content here...'}), label=False)

class EditEntryForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={'cols':100, 'rows':10, 'placeholder': 'Content here...'}), label=False)


def index(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            #title = request.POST.get("title")
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


def new_entry(request):
    if request.method == 'POST':
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            text = form.cleaned_data["text"]
            if util.no_entry_conflict(title):
                util.save_entry(title, text)
                return redirect('wiki:entry', title=title)
            else:
                context = {"form": SearchForm(), "new_entry_form": form}
                return render(request, "encyclopedia/new_entry_duplicate.html", context)  
    
    else:
        context = {"form": SearchForm(), "new_entry_form": NewEntryForm()}

    
    return render(request, "encyclopedia/new_entry.html", context)



def edit(request, title):
    entry = util.get_entry(title)
    if request.method == 'POST':
        form = EditEntryForm(data=request.POST)
        if form.is_valid():
            text = form.cleaned_data["text"]
            util.save_entry(title, text)
            return redirect('wiki:entry', title=title)

    else:
        form = EditEntryForm(initial={'text': entry})
    context = {"form": SearchForm(), "title": title, "edit_form": form}
    return render(request, "encyclopedia/edit.html", context) 