from calendar import c
from cgitb import text
from unicodedata import category
from django.shortcuts import render
from django.http import HttpResponse
from goods.models import Categories, Products


def index(request):

    context = {
        "title": "VULCANO - Головна",
        "content": "Інтернет-магазин грилів VULCANO",
    }
    return render(request, "main/index.html", context)


def about(request):
    context = {
        "title": "VULCANO - Про нас",
        "content": "Про магазин VULCANO",
        "text_on_page": "Текст сторінки про магазин грилів VULCANO",
    }
    return render(request, "main/about.html", context)
