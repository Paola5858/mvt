from django import forms
from .models import Animal

class AnimalForm(forms.ModelForm):
    class Meta:
        model = Animal
        fields = ['nome', 'tutor', 'idade', 'peso']
        labels = {'nome': 'Nome do Animal',
                  'tutor': 'Nome do Tutor',
                  'idade': 'Idade do animal',
                  'peso': 'Peso do animal(kg)'}
