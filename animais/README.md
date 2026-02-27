# 🌾 API REST com múltiplos recursos

Projeto de estudo focado em entender como o Django REST Framework abstrai a construção de APIs.

## 📋 Sobre

Dois recursos completamente diferentes servidos como API REST:
- **Animal**: nome, tutor
- **Talhão**: nome, área (hectares), cultura plantada

O objetivo é entender o que o DRF faz automaticamente e o que ainda preciso controlar.

## 🧠 Conceitos aplicados

- `ModelViewSet` (CRUD automático)
- `DefaultRouter` (geração automática de URLs)
- `ModelSerializer` (conversão Python ↔ JSON)
- Múltiplos apps no mesmo projeto
- Interface navegável do DRF

## 📦 Modelos

```python
# api_animal/models.py
class Animal(models.Model):
    nome = models.CharField(max_length=100)
    tutor = models.CharField(max_length=100)

# api_talhao/models.py
class Talhao(models.Model):
    nome = models.CharField(max_length=100)
    area = models.DecimalField(max_digits=6, decimal_places=2)
    cultura = models.CharField(max_length=100)
```

## 🚀 Como rodar

```bash
# 1. Ativar ambiente virtual
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# 2. Instalar dependências
pip install django djangorestframework

# 3. Rodar migrações
python manage.py migrate

# 4. Criar superusuário (opcional)
python manage.py createsuperuser

# 5. Iniciar servidor
python manage.py runserver
```

Acesse: `http://localhost:8000/`

## 🌐 Endpoints disponíveis

### Animais

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/animals/` | Lista todos os animais |
| POST | `/animals/` | Cadastra novo animal |
| GET | `/animals/{id}/` | Detalhe de um animal |
| PUT | `/animals/{id}/` | Atualiza animal |
| DELETE | `/animals/{id}/` | Remove animal |

### Talhões

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/talhoes/` | Lista todos os talhões |
| POST | `/talhoes/` | Cadastra novo talhão |
| GET | `/talhoes/{id}/` | Detalhe de um talhão |
| PUT | `/talhoes/{id}/` | Atualiza talhão |
| DELETE | `/talhoes/{id}/` | Remove talhão |

## 📝 Exemplo de requisição

```bash
# POST /animals/
curl -X POST http://localhost:8000/animals/ \
  -H "Content-Type: application/json" \
  -d '{"nome": "Rex", "tutor": "João Silva"}'

# POST /talhoes/
curl -X POST http://localhost:8000/talhoes/ \
  -H "Content-Type: application/json" \
  -d '{"nome": "Talhão A", "area": "15.50", "cultura": "Milho"}'
```

## 📁 Estrutura

```
animais/
├── api_animal/
│   ├── models.py          # Animal
│   ├── serializers.py     # AnimalSerializer
│   ├── views.py           # AnimalViewSet
│   ├── urls.py            # Router
│   └── admin.py
├── api_talhao/
│   ├── models.py          # Talhao
│   ├── serializers.py     # TalhaoSerializer
│   ├── views.py           # TalhaoViewSet
│   ├── urls.py            # Router
│   └── admin.py
└── animal/
    ├── settings.py
    └── urls.py
```

## 💡 O que aprendi

- Como o `ModelViewSet` entrega 5 endpoints com uma classe
- O que o `DefaultRouter` faz por mim
- Como o `ModelSerializer` converte automaticamente entre Python e JSON
- A diferença entre `fields = '__all__'` e especificar campos manualmente
- Como organizar múltiplos apps no mesmo projeto Django

---

**Parte do repositório:** [mvt - Estudos de Django REST Framework](../)
