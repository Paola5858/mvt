from django.shortcuts import render, redirect
from .models import Pessoa

def cadastro(request):
    if request.method == "GET":
        return render(request, 'cadastro.html')
    elif request.method == "POST":
        nome = request.POST.get('nome')
        idade = request.POST.get('idade')
        email = request.POST.get('email')

        pessoa = Pessoa(nome=nome, idade=idade, email=email)
        pessoa.save()

        return redirect('lista')

def lista(request):
      pessoas = Pessoa.objects.all()
      return render(request, 'listar.html', {'pessoas': pessoas})
