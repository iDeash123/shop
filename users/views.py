import re
from django.contrib.auth.decorators import login_required
from django.contrib import auth, messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import context
from django.urls import reverse

from users.forms import UserLoginForm, UserRegistrationForm, ProfileForm


def login(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                messages.success(request, f"Ви успішно увійшли як {username}")
                if request.POST.get("next", None):
                    return HttpResponseRedirect(request.POST.get("next"))
                return HttpResponseRedirect(reverse("main:index"))
    else:
        form = UserLoginForm()
    context = {"title": "SEAR - Вхід", "form": form}

    return render(request, "users/login.html", context)


def registration(request):
    if request.method == "POST":
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = form.instance
            auth.login(request, user)
            messages.success(request, f"Ви успішно зареєструвалися як {user.username}")
            return HttpResponseRedirect(reverse("main:index"))
    else:
        form = UserRegistrationForm()

    context = {
        "title": "SEAR - Реєстрація",
        "form": form,
    }
    return render(request, "users/registration.html", context)


@login_required
def profile(request):
    if request.method == "POST":
        form = ProfileForm(
            data=request.POST, instance=request.user, files=request.FILES
        )
        if form.is_valid():
            form.save()
            messages.success(request, "Ваш профіль успішно оновлено!")
            return HttpResponseRedirect(reverse("user:profile"))
    else:
        form = ProfileForm(instance=request.user)

    context = {
        "title": "SEAR - Кабінет",
        "form": form,
    }
    return render(request, "users/profile.html", context)


def users_cart(request):
    context = {
        "title": "SEAR - Корзина",
    }
    return render(request, "users/users_cart.html", context)


@login_required
def logout(request):
    messages.success(request, f"{request.user.username}, ви успішно вийшли з акаунта.")
    auth.logout(request)
    return HttpResponseRedirect(reverse("main:index"))
