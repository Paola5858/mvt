# cadastro de pessoas com django mvt

primeiro contato com django. sem api, sem drf, sem abstrações.

só o básico: model, view, template.

## sobre

sistema de cadastro de pessoas com formulário html puro e listagem renderizada no servidor.

o objetivo aqui era entender **como o django funciona antes de qualquer framework rest**. como uma requisição vira uma resposta. como o template recebe dados. como o post é processado.

nada de json. só html renderizado.

## conceitos aplicados

- padrão mvt (model-view-template)
- renderização server-side com `render()`
- processamento de formulários com `request.POST`
- context processors
- `{% csrf_token %}` em formulários
- estrutura básica de um app django

## modelo

```python
class Pessoa(models.Model):
    nome = models.CharField(max_length=100)
    idade = models.IntegerField()
    email = models.EmailField(unique=True)
```

simples. três campos. nada de relacionamento, nada de validação customizada.

## como rodar

```bash
# 1. ativar ambiente virtual
.venv\Scripts\activate  # windows
source .venv/bin/activate  # linux/mac

# 2. instalar dependências
pip install -r requirements.txt

# 3. rodar migrações
python manage.py migrate

# 4. iniciar servidor
python manage.py runserver
```

acesse: `http://localhost:8000/`

## rotas disponíveis

| url | view | descrição |
|-----|------|-----------|
| `/cadastro/` | cadastro | formulário de cadastro |
| `/lista/` | lista | lista todas as pessoas |

## estrutura

```
primeiro/
├── Pessoa/
│   ├── models.py          # model pessoa
│   ├── views.py           # cadastro, lista
│   └── templates/
│       ├── cadastro.html  # formulário html
│       └── listar.html    # listagem
└── setup/
    ├── settings.py
    └── urls.py
```

## o que aprendi

- como o django processa uma requisição do zero
- a diferença entre get e post no fluxo de formulários
- por que o `{% csrf_token %}` existe
- como passar dados do banco pro template via context
- que dá pra fazer muita coisa sem precisar de api

---

**parte do repositório:** [mvt - estudos de django rest framework](../)
