# api de doadores de sangue

projeto com relacionamento foreignkey entre models. dois recursos conectados: tipo sanguíneo e doador.

## sobre

api rest para gerenciar doadores de sangue com seus tipos sanguíneos. modelagem 1:N onde um tipo sanguíneo pode ter vários doadores.

o foco aqui era entender como o drf lida com relacionamentos e como representar isso na api.

## conceitos aplicados

- foreignkey e relacionamentos 1:N
- serialização de relacionamentos
- filtros com django-filter
- busca e ordenação
- admin customizado com filtros
- select_related para otimização de queries

## modelos

```python
class TipoSanguineo(models.Model):
    tipo = models.CharField(max_length=3, choices=TIPOS)
    # A+, A-, B+, B-, AB+, AB-, O+, O-

class Doador(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    cpf = models.CharField(max_length=14, unique=True)
    tipo_sanguineo = models.ForeignKey(TipoSanguineo)
    data_nascimento = models.DateField()
    telefone = models.CharField(max_length=15)
    ultima_doacao = models.DateField(null=True, blank=True)
    ativo = models.BooleanField(default=True)
```

## como rodar

```bash
# 1. ativar ambiente virtual
.venv\Scripts\activate  # windows
source .venv/bin/activate  # linux/mac

# 2. instalar dependências
pip install -r requirements.txt

# 3. rodar migrações
python manage.py makemigrations
python manage.py migrate

# 4. criar superusuário
python manage.py createsuperuser

# 5. iniciar servidor
python manage.py runserver
```

acesse: `http://localhost:8000/`

## endpoints disponíveis

### tipos sanguíneos

| método | endpoint | descrição |
|--------|----------|-----------|
| GET | `/tipo-sanguineo/` | lista tipos com total de doadores |
| POST | `/tipo-sanguineo/` | cadastra novo tipo |
| GET | `/tipo-sanguineo/{id}/` | detalhe de um tipo |
| PUT | `/tipo-sanguineo/{id}/` | atualiza tipo |
| DELETE | `/tipo-sanguineo/{id}/` | remove tipo |

### doadores

| método | endpoint | descrição |
|--------|----------|-----------|
| GET | `/doador/` | lista todos os doadores |
| POST | `/doador/` | cadastra novo doador |
| GET | `/doador/{id}/` | detalhe de um doador |
| PUT | `/doador/{id}/` | atualiza doador |
| DELETE | `/doador/{id}/` | remove doador |

**filtros disponíveis:**
- `?tipo_sanguineo=1` - filtra por tipo sanguíneo
- `?ativo=true` - filtra doadores ativos
- `?search=nome` - busca por nome, email ou cpf
- `?ordering=-criado_em` - ordena por data de criação

## exemplo de requisição

```bash
# POST /tipo-sanguineo/
curl -X POST http://localhost:8000/tipo-sanguineo/ \
  -H "Content-Type: application/json" \
  -d '{"tipo": "O+"}'

# POST /doador/
curl -X POST http://localhost:8000/doador/ \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "maria silva",
    "email": "maria@email.com",
    "cpf": "123.456.789-00",
    "tipo_sanguineo": 1,
    "data_nascimento": "1990-05-15",
    "telefone": "(11) 98765-4321",
    "ativo": true
  }'

# GET /doador/?tipo_sanguineo=1
curl http://localhost:8000/doador/?tipo_sanguineo=1
```

## estrutura

```
doador/
├── api_doador/
│   ├── models.py          # TipoSanguineo, Doador
│   ├── serializers.py     # serializers com campos calculados
│   ├── views.py           # viewsets com filtros
│   ├── urls.py            # routers
│   └── admin.py           # admin customizado
└── doador/
    ├── settings.py
    └── urls.py
```

## o que aprendi

- como modelar um relacionamento foreignkey
- como o drf serializa relacionamentos (id no post, objeto no get)
- usar select_related para evitar n+1 queries
- filtrar por campo relacionado
- criar serializers diferentes para list e detail
- customizar o admin com filtros e busca

---

**parte do repositório:** [mvt - estudos de django rest framework](../)
