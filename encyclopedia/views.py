from django.shortcuts import render, redirect
import markdown2
from . import util
from django.http import HttpResponse
from .util import save_entry
from .util import get_entry
from django import forms
import random    
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from . import util


def index(request):
    
    entries = util.list_entries()
    
    return render(request, "encyclopedia/index.html", {
        "entries": entries
    })


def randomm(request):
    entries = util.list_entries()
    random_entry = random.choice(entries)
    return redirect("entry", title=random_entry) 


def entry_page(request, title):
    
    content = util.get_entry(title)
    
    if content is None:
       
        return render(request, "encyclopedia/error.html", {
            "message": "No such page exists, Maybe try something else (;"
        })
    
    
    content_html = markdown2.markdown(content)
    
   
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": content_html
    })


def search(request):

    query = request.GET.get("q", "").strip()
    
    if not query:
        return redirect("index")
       
    entries = util.list_entries()
    
    if query.lower() in [entry.lower() for entry in entries]:
        return redirect("entry", title=query)
    
    results = [entry for entry in entries if query.lower() in entry.lower()]
    
    return render(request, "encyclopedia/results.html", {
        "query": query,
        "results": results
    })


def title_exists(title):
    return util.get_entry(title) is not None


def new(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")

        if title_exists(title):
            return render(request, "encyclopedia/exist.html", {
                "error": "An entry with this title already exists."
            })
        
        save_entry(title, content)
        return redirect("index")

    return render(request, "encyclopedia/new.html")


# class NewPageForm(forms.Form):
#     title = forms.CharField(label="Title", max_length=100, widget=forms.TextInput(attrs={
#         'class': 'form-control',
#         'placeholder': 'Enter the title'
#     }))
#     content = forms.CharField(label="Content", widget=forms.Textarea(attrs={
#         'class': 'form-control',
#         'placeholder': 'Enter the content',
#         'rows': 10
#     }))


class SearchForm(forms.Form):
    title = forms.CharField(label='', widget=forms.TextInput(attrs={
      "class": "search",
      "placeholder": "Search Qwikipedia"}))

class CreateForm(forms.Form):
    title = forms.CharField(label='', widget=forms.TextInput(attrs={
      "placeholder": "Page Title"}))
    text = forms.CharField(label='', widget=forms.Textarea(attrs={
      "placeholder": "Enter Page Content using Github Markdown"
    }))

class EditForm(forms.Form):
  text = forms.CharField(label='', widget=forms.Textarea(attrs={
      "placeholder": "Enter Page Content using Github Markdown"
    }))




def edit(request, title):

    if request.method == "GET":
        text = util.get_entry(title)

        if text == None:
            messages.error(request, f'"{title}"" page does not exist and can\'t be edited, please create a new page instead!')

        return render(request, "encyclopedia/edit.html", {
          "title": title,
          "edit_form": EditForm(initial={'text':text}),
          "search_form": SearchForm()
        })

    elif request.method == "POST":
        form = EditForm(request.POST)

        if form.is_valid():
          text = form.cleaned_data['text']
          util.save_entry(title, text)
          messages.success(request, f'Entry "{title}" updated successfully!')
          return redirect(reverse('entry', args=[title]))

        else:
          messages.error(request, f'Editing form not valid, please try again!')
          return render(request, "encyclopedia/edit.html", {
            "title": title,
            "edit_form": form,
            "search_form": SearchForm()
          })


def delete_entry(request, title):
    if request.method == "POST":
        util.delete_entry(title)
        messages.success(request, f'Entry "{title}" has been deleted successfully!')
        return redirect('index')
    
    return render(request, "encyclopedia/del_confirm.html", {
        "title": title
    })
