from django.shortcuts import render,redirect
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from markdown2 import Markdown
import random

from django.contrib import messages

from . import util

markdowner = Markdown()

# def convert_md_to_html(title):
#      content = util.get_entry(title)
#      markdowner = Markdown()
#      if content == None:
#           return None
#      else:
#         return markdowner.convert(content)

def entry(request, title):
    if util.get_entry(title) == None:
        return render(request, "encyclopedia/error.html",{
            "message":"This entry does not exit"
        })
    else:
        html_content = markdowner.convert(util.get_entry(title))
        return render(request, "encyclopedia/entry.html",{
            "title":title,
            "content":html_content
        })


def search(request):
    entry_search =  request.GET.get('q')
    if util.get_entry(entry_search) is not None:
        return redirect('entry', title=entry_search)
    else:
        allEntries = util.list_entries()
        recommendation = []  
        for entry in allEntries:
            if entry_search.lower() in entry.lower():
                recommendation.append(entry)
        return render(request,"encyclopedia/search.html",{
            "recommendation":recommendation
        })          



class AddPageForm(forms.Form):
    title = forms.CharField(label= 'Entrytitle')
    content = forms.CharField(label= 'Content')

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
    })


 
def new_page0(request):
    if request.method == "GET":
            return render(request,"encyclopedia/new.html")
    else:
            title = request.POST['title']
            content = request.POST['content']
            titleExist = util.get_entry(title)
            if titleExist is not None:
                return render(request, "encyclopedia/error.html", {
            "message": "Entry page already exists"
        })
            else:
                util.save_entry(title, content)
                html_content = convert_md_to_html(title)
            return render (request,"encyclopedia/entry.html",{
                "title":title,
                "content":html_content
            })
            
def new_page(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        if util.get_entry(title) is not None:
            return render(request, "encyclopedia/new.html", {
                "error_message": "Entry page already exists"
            })
        util.save_entry(title, content)
        return redirect('entry', title)
    else: 
        return render(request,"encyclopedia/new.html")

    
        
def randompage(request):
    allEntries = util.list_entries()
    randompage_entry = random.choice(allEntries)
    return redirect('entry', title=randompage_entry)
     