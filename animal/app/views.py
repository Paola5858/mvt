from django.shortcuts import render, redirect, get_object_or_404
from .models import Animal
from .forms import AnimalForm

# LISTAR
def listar_animais(request):
    animais = Animal.objects.all()
    return render(request, 'listar.html', {'animais': animais})

# CRIAR
def criar_animal(request):
    if request.method == 'POST':
        form = AnimalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_animais')
    else:
        form = AnimalForm()
    return render(request, 'form.html', {'form': form})

# EDITAR
def editar_animal(request, pk):
    animal = get_object_or_404(Animal, pk=pk)
    if request.method == 'POST':
        form = AnimalForm(request.POST, instance=animal)
        if form.is_valid():
            form.save()
            return redirect('listar_animais')
    else:
        form = AnimalForm(instance=animal)
    return render(request, 'form.html', {'form': form})

# DELETAR
def deletar_animal(request, pk):
    animal = get_object_or_404(Animal, pk=pk)
    if request.method == 'POST':
        animal.delete()
        return redirect('listar_animais')
    return render(request, 'confirmar_delete.html', {'animal': animal})
