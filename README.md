<div align="center">

<h1>⚙️ Estudos de Django REST Framework</h1>

<p>um repositório de exercícios práticos onde fui do CRUD básico até APIs REST com DRF, cada projeto um nível acima do anterior.</p>

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.x%20%2F%206.x-092E20?style=flat&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/Django%20REST%20Framework-3.16-red?style=flat)](https://www.django-rest-framework.org/)
[![SQLite](https://img.shields.io/badge/SQLite-local-003B57?style=flat&logo=sqlite&logoColor=white)]()
[![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?style=flat&logo=mysql&logoColor=white)](https://www.mysql.com/)
[![Status](https://img.shields.io/badge/status-em%20evolução-blue?style=flat)]()

</div>

---

## sobre o repositório

esse repo é meu caderno de estudos de backend com Django.

não é um projeto único, é uma linha do tempo. cada pasta aqui representa um momento diferente do meu aprendizado, começando pelo CRUD mais simples com views funcionais e chegando em APIs REST estruturadas com ViewSets, Routers e serialização automática.

guardo tudo junto de propósito. dá pra ver a evolução, e evolução é o que importa.

---

## projetos

### 01 — CRUD com Function Based Views [`/animal`]

o ponto de partida. um sistema de cadastro de animais (nome, tutor, idade, peso) feito com views funcionais, formulários Django e templates simples.

sem DRF, sem CBV, sem abstração. só o ciclo básico funcionando: request chega, view processa, banco é consultado, template renderiza, resposta sai.

**o que esse exercício treina:**
- ciclo completo de uma FBV (listar, criar, editar, deletar)
- ModelForm com validação automática
- `get_object_or_404` para tratamento de 404
- fluxo de redirect pós-formulário
- `{% csrf_token %}` nos templates

```
animal/
├── app/
│   ├── models.py       # Animal: nome, tutor, idade, peso
│   ├── forms.py        # AnimalForm com labels customizadas
│   ├── views.py        # listar, criar, editar, deletar
│   └── templates/      # listar.html, form.html, confirmar_delete.html
└── setup/
    ├── settings.py
    └── urls.py
```

---

### 02 — API REST com DRF e múltiplos recursos [`/animais`]

o salto. mesma ideia de animal, mas agora servido como API REST. e junto, um segundo recurso completamente diferente: talhão (área de plantio com nome, área em hectares e cultura plantada).

aqui o objetivo era entender como o DRF abstrai o trabalho de construir uma API: o `ModelViewSet` entrega os 5 endpoints (list, create, retrieve, update, destroy) com uma classe, o `DefaultRouter` gera as URLs automaticamente, e o `ModelSerializer` cuida da conversão entre Python e JSON.

**o que esse exercício treina:**
- `ModelViewSet` e o que ele entrega de graça
- `DefaultRouter` e registro de recursos
- `ModelSerializer` com `fields = '__all__'`
- separação em múltiplos apps dentro do mesmo projeto
- interface navegável do DRF

```
animais/
├── api_animal/
│   ├── models.py       # Animal: nome, tutor
│   ├── serializers.py  # AnimalSerializer
│   ├── views.py        # AnimalViewSet
│   └── urls.py         # router com /animals/
├── api_talhao/
│   ├── models.py       # Talhao: nome, area (DecimalField), cultura
│   ├── serializers.py  # TalhaoSerializer
│   ├── views.py        # TalhaoViewSet
│   └── urls.py         # router com /talhoes/
└── animal/
    ├── settings.py
    └── urls.py
```

**endpoints disponíveis:**

| método | endpoint | descrição |
|--------|----------|-----------|
| GET | `/animals/` | lista todos os animais |
| POST | `/animals/` | cadastra novo animal |
| GET | `/animals/{id}/` | detalhe de um animal |
| PUT | `/animals/{id}/` | atualiza animal |
| DELETE | `/animals/{id}/` | remove animal |
| GET | `/talhoes/` | lista todos os talhões |
| POST | `/talhoes/` | cadastra novo talhão |
| GET | `/talhoes/{id}/` | detalhe de um talhão |
| PUT | `/talhoes/{id}/` | atualiza talhão |
| DELETE | `/talhoes/{id}/` | remove talhão |

---

### 03 — API com relacionamento (ForeignKey) [`/doador`]

o próximo nível: dois models com ForeignKey entre eles, servidos via DRF.

modelagem de doadores de sangue com tipo sanguíneo. `TipoSanguineo` e `Doador` com relação 1:N. o serializer passa a representar o relacionamento, e a API retorna dados aninhados.

**o que esse exercício treina:**
- `ForeignKey` no model e como ela aparece na API
- serialização de relacionamentos no DRF
- filtragem por campo relacionado
- como o DRF trata o `id` de uma FK no POST vs GET

```
doador/
├── api_doador/
│   ├── models.py       # TipoSanguineo, Doador (FK)
│   ├── serializers.py  # DoadorSerializer, TipoSanguineoSerializer
│   ├── views.py        # ViewSets
│   └── urls.py         # routers
└── doador/
    ├── settings.py
    └── urls.py
```

**endpoints disponíveis:**

| método | endpoint | descrição |
|--------|----------|-----------|
| GET | `/doador/` | lista todos os doadores |
| POST | `/doador/` | cadastra novo doador |
| GET | `/doador/{id}/` | detalhe de um doador |
| PUT | `/doador/{id}/` | atualiza doador |
| DELETE | `/doador/{id}/` | remove doador |
| GET | `/tipo-sanguineo/` | lista tipos sanguíneos |
| POST | `/tipo-sanguineo/` | cadastra novo tipo |

---

### 04 — CRUD básico com templates [`/primeiro`]

exercício de modelagem simples com Django templates. foco em entender o fluxo MVT sem API.

**o que esse exercício treina:**
- padrão MVT do Django
- renderização de templates
- context processors
- estrutura básica de um app Django

```
primeiro/
├── Pessoa/
│   ├── models.py
│   ├── views.py
│   └── templates/
└── setup/
    ├── settings.py
    └── urls.py
```

---

### 05 — API com telemetria [`/telemetria`]

integração com dados de sensores. API que recebe leituras de dispositivos (temperatura, umidade, timestamp) e expõe endpoints de consulta.

**o que esse exercício treina:**
- modelagem de dados de séries temporais
- `DateTimeField` com `auto_now_add`
- filtragem por intervalo de data
- pensar em API não só como CRUD mas como pipeline de dados
- uso de variáveis de ambiente com `.env`

```
telemetria/
├── api_telemetria/
│   ├── models.py       # Leitura: sensor, temperatura, umidade, timestamp
│   ├── serializers.py  # LeituraSerializer
│   └── views.py        # LeituraViewSet
├── setup/
│   ├── settings.py
│   └── urls.py
├── .env                # variáveis de ambiente
└── .env.example        # template de configuração
```

---

## como rodar qualquer projeto

todos os projetos seguem o mesmo fluxo:

```bash
# 1. entre na pasta do projeto
cd animal   # ou animais, doador, primeiro, telemetria

# 2. crie e ative o ambiente virtual
python -m venv .venv
.venv\Scripts\activate       # windows
source .venv/bin/activate    # linux/mac

# 3. instale as dependências
pip install -r requirements.txt

# 4. rode as migrações
python manage.py migrate

# 5. (opcional) crie um superusuário
python manage.py createsuperuser

# 6. suba o servidor
python manage.py runserver
```

acesse `http://localhost:8000/` — os projetos DRF têm interface navegável habilitada.

---

## o que esse repositório mostra sobre como eu aprendo

cada projeto aqui foi feito com uma pergunta na cabeça.

no `animal/` a pergunta era: como o Django processa uma requisição do começo ao fim sem nenhuma mágica?

no `animais/` era: o que o DRF faz por mim e o que eu ainda preciso controlar?

no `doador/` era: como modelar um relacionamento e fazer a API representar isso direito?

no `telemetria/` era: como lidar com dados que chegam de dispositivos, não de formulários humanos?

não aprendo copiando tutorial. aprendo quebrando e entendendo por que quebrou.

---

## stack usada nos projetos

| tecnologia | versão | onde |
|-----------|--------|------|
| Python | 3.12+ | todos |
| Django | 5.x / 6.x | todos |
| Django REST Framework | 3.16 | animais, doador, telemetria |
| SQLite | embutido | todos (dev local) |
| MySQL | 8.0 | doador (opcional) |
| mysqlclient | 2.2.8 | doador (quando usar MySQL) |

---

## contato

feito por **Paola Soares Machado**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Paola%20Soares%20Machado-0077B5?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/paolasoaresmachado)
[![Gmail](https://img.shields.io/badge/Gmail-paolasesi351%40gmail.com-D14836?style=flat&logo=gmail&logoColor=white)](mailto:paolasesi351@gmail.com)
[![GitHub](https://img.shields.io/badge/GitHub-Paola5858-181717?style=flat&logo=github&logoColor=white)](https://github.com/Paola5858)

---

## 📄 licença

Este projeto está sob a licença MIT.

---

⭐ Se este repositório te ajudou de alguma forma, considere dar uma estrela!
