from django.shortcuts import render
from django.http import HttpResponse
from .models import Pessoa

def Cadastro(request):
    if request.method == "GET":
        return render(request, 'cadastro.html')
    elif request.method == "POST":
        nome = request.POST.get('nome')
        idade = request.POST.get('idade')
        email = request.POST.get('email')

        pessoa = Pessoa(nome=nome, idade=idade, email=email)
        pessoa.save()

        return HttpResponse("Pessoa cadastrada com sucesso!")
