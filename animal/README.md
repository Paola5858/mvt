# 🐾 CRUD de Animais com Function Based Views

Projeto de estudo focado em entender o ciclo completo de uma aplicação Django usando Function Based Views (FBV).

## 📋 Sobre

Sistema simples de cadastro de animais com informações básicas: nome, tutor, idade e peso.

O objetivo aqui não é fazer algo complexo, mas entender **como o Django funciona por baixo**, sem abstrações de CBV ou DRF.

## 🧠 Conceitos aplicados

- Function Based Views (FBV)
- ModelForm com validação automática
- `get_object_or_404` para tratamento de 404
- Fluxo de redirect pós-formulário
- Templates Django com `{% csrf_token %}`
- CRUD completo (Create, Read, Update, Delete)

## 📦 Modelo

```python
class Animal(models.Model):
    nome = models.CharField(max_length=100)
    tutor = models.CharField(max_length=100)
    idade = models.IntegerField()
    peso = models.DecimalField(max_digits=5, decimal_places=2)
```

## 🚀 Como rodar

```bash
# 1. Ativar ambiente virtual
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# 2. Instalar dependências
pip install django

# 3. Rodar migrações
python manage.py migrate

# 4. Iniciar servidor
python manage.py runserver
```

Acesse: `http://localhost:8000/`

## 🌐 Rotas disponíveis

| URL | View | Descrição |
|-----|------|-----------|
| `/` | listar_animais | Lista todos os animais |
| `/criar/` | criar_animal | Formulário de cadastro |
| `/editar/<pk>/` | editar_animal | Formulário de edição |
| `/deletar/<pk>/` | deletar_animal | Confirmação de exclusão |

## 📁 Estrutura

```
animal/
├── app/
│   ├── models.py          # Model Animal
│   ├── forms.py           # AnimalForm
│   ├── views.py           # FBVs do CRUD
│   ├── admin.py           # Registro no admin
│   └── templates/
│       ├── listar.html
│       ├── form.html
│       └── confirmar_delete.html
└── setup/
    ├── settings.py
    └── urls.py
```

## 💡 O que aprendi

- Como uma requisição HTTP vira uma resposta renderizada
- O papel do `request.method` no fluxo de formulários
- Por que usar `get_object_or_404` em vez de `Model.objects.get()`
- Como o `ModelForm` economiza código de validação
- A importância do `{% csrf_token %}` em formulários POST

---

**Parte do repositório:** [mvt - Estudos de Django REST Framework](../)
