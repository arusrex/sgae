from django.shortcuts import render, redirect, get_list_or_404

def login(request):

    context = {

    }

    return render(request, "login.html", context)

def registro(request):

    context = {}

    return render(request, "registro.html", context)

def redefinir_senha(request):

    context = {}

    return render(request, "redefinir_senha.html", context)

def index(request):


    context = {

    }

    return render(request, 'index.html', context)

def sistema(request):

    context = {}

    return render(request, 'sistema.html', context)