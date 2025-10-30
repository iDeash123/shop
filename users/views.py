import re
from django.shortcuts import render
from django.template import context


def login(request):
    context = {"title": "SEAR - Вхід"}
    return render(request, "users/login.html", context)


def registration(request):
    context = {"title": "SEAR - Реєстрація"}
    return render(request, "users/registration.html", context)


def profile(request):
    context = {"title": "SEAR - Кабінет"}
    return render(request, "users/profile.html", context)


def logout(request): ...
