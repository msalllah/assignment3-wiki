from django.shortcuts import render,redirect
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from markdown2 import Markdown
import random

from django.contrib import messages

from . import util


def convert_md_to_html(title):
     content = util.get_entry(title)
     markdowner = Markdown()
     if content == None:
          return None
     else:
        return markdowner.convert(content)

def entry(request, title):
    html_content = convert_md_to_html(title)
    if html_content ==None:
        return render(request, "encyclopedia/error.html",{
            "message":"This entry does not exit"
        })
    else:
        return render(request, "encyclopedia/entry.html",{
            "title":title,
            "content":html_content
        })


def search(request):
    if request.method == "POST":
       entry_search =  request.POST['q']
       html_content = convert_md_to_html(entry_search)
       if html_content is not None:
           return render(request, "encyclopedia/entry.html", {
               "title":entry_search,
               "content":html_content      
                              })               
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


 
def new_page(request):
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
  
        
def randompage(request):
    allEntries = util.list_entries()
    randompage_entry = random.choice(allEntries)
    html_content = convert_md_to_html(randompage_entry)
    return render(request, "encyclopedia/entry.html", {
       "title":randompage_entry,
       "content":html_content
    })
     