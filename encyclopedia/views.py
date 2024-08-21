from django.shortcuts import render, redirect
import markdown2
from . import util
from django.http import HttpResponse
from .util import save_entry
from .util import get_entry

def index(request):
    
    entries = util.list_entries()
    
    return render(request, "encyclopedia/index.html", {
        "entries": entries
    })


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
    
    return render(request, "encyclopedia/search.html", {
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

def edit(request, title):
    entry = get_entry(title)
    
    if entry is None:
        return render(request, "encyclopedia/error.html", {
            "error_message": "Page does not exist."
        })

    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            new_title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            
            if title != new_title and title_exists(new_title):
                return render(request, "encyclopedia/exist.html", {
                    "error_message": "A page with this title already exists."
                })
            
            save_entry(new_title, content)
            return redirect('entry', title=new_title)
    else:
        form = NewPageForm(initial={'title': title, 'content': entry})

    return render(request, "encyclopedia/edit.html", {
        "form": form,
        "title": title
    })