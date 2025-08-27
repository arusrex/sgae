from django.shortcuts import render, redirect, get_list_or_404


def index(request):


    context = {

    }

    return render(request, 'index.html', context)