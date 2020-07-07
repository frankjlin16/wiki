from django.shortcuts import render, redirect
from django import forms

from . import util

class SearchForm(forms.Form):
	title = forms.CharField(label=False)


def index(request):
	if request.method == 'POST':
		form = SearchForm(request.POST)
		if form.is_valid():
			title = form.cleaned_data["title"]
			return redirect('wiki:entry', title=title)
	else:
		context = {"entries": util.list_entries(), "form": SearchForm()}
		return render(request, "encyclopedia/index.html", context)


def entry(request, title):
	context = {"entry": util.get_entry(title), "title": title}
	return render(request, "encyclopedia/entry.html", context)

	redirect()