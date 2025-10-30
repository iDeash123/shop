from calendar import c
from cgitb import text
from unicodedata import category
from django.shortcuts import render
from django.http import HttpResponse
from goods.models import Categories, Products


def index(request):

    context = {
        "title": "SEAR - Головна",
        "content": "Інтернет-магазин грилів SEAR",
    }
    return render(request, "main/index.html", context)


def about(request):
    context = {
        "title": "SEAR - Про нас",
        "content": "Про магазин SEAR",
        "text_on_page": "Текст сторінки про магазин грилів SEAR",
    }
    return render(request, "main/about.html", context)
