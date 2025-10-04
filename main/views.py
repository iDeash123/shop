from calendar import c
from cgitb import text
from unicodedata import category
from django.shortcuts import render
from django.http import HttpResponse
from goods.models import Categories, Products


def index(request):
    categories = Categories.objects.all()

    context = {
        "title": "Home - Головна",
        "content": "Магазин мебели HOME",
        "categories": categories,
    }
    return render(request, "main/index.html", context)


def about(request):
    context = {
        "title": "Home - О нас",
        "content": "О нас",
        "text_on_page": "Текст страницы о нас",
    }
    return render(request, "main/about.html", context)
