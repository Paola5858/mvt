# 🩸 API - Sistema de Doadores de Sangue

Sim.  
É uma API completa.  
Conectada ao MySQL.  
Com Django Rest Framework.  
E funcionando 100%.

Esse projeto foi desenvolvido como prática avançada de backend,
com foco em modelagem de dados, API REST e integração com banco relacional.

---

## 🚀 Tecnologias Utilizadas

- Python 3.14
- Django 6.0.2
- Django Rest Framework 3.16.1
- MySQL
- Git
- Arquitetura MVT

---

## 🧠 Sobre o Projeto

A ideia é simples, mas a implementação é sólida:

Gerenciar doadores de sangue e seus respectivos tipos sanguíneos,
usando uma API REST estruturada e conectada a um banco MySQL real.

### Modelagem aplicada:

#### 🧬 TipoSanguineo
- `tipo` (CharField)

#### 🧑‍⚕️ Doador
- `nome` (CharField)
- `data_nascimento` (DateField)
- `tipo_sanguineo` (ForeignKey)

Relacionamento 1:N entre TipoSanguineo e Doador.

---

## 🏗️ Arquitetura

O projeto segue o padrão MVT do Django:

- **Model** → Estrutura do banco
- **ViewSet** → Lógica da API
- **Router** → Endpoints automáticos
- **Serializer** → Conversão JSON

Organização clara e separação de responsabilidades.

---

## 📁 Estrutura do Projeto

```
mvt/
├── doador/                 # App principal
│   ├── migrations/         # Migrações do banco
│   ├── models.py          # Modelos TipoSanguineo e Doador
│   ├── serializers.py     # Serializers DRF
│   ├── views.py           # ViewSets da API
│   └── admin.py           # Configuração do admin
├── setup/                  # Configurações do projeto
│   ├── settings.py        # Configurações gerais
│   ├── urls.py            # Rotas principais
│   └── wsgi.py
├── .venv/                  # Ambiente virtual
├── .gitignore             # Arquivos ignorados
├── requirements.txt       # Dependências
└── manage.py              # CLI do Django
```

---

## 🔌 Configuração do Banco (MySQL)

No `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'seu_banco',
        'USER': 'root',
        'PASSWORD': 'sua_senha',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

---

## ⚙️ Como rodar o projeto

### 1️⃣ Criar ambiente virtual:

```bash
python -m venv .venv
```

### 2️⃣ Ativar:

**Windows:**
```bash
.\.venv\Scripts\Activate
```

**Linux/Mac:**
```bash
source .venv/bin/activate
```

### 3️⃣ Instalar dependências:

```bash
pip install -r requirements.txt
```

### 4️⃣ Configurar banco MySQL:

Edite o arquivo `setup/settings.py` com suas credenciais do MySQL.

### 5️⃣ Rodar migrações:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6️⃣ Iniciar servidor:

```bash
python manage.py runserver
```

Acesse: `http://localhost:8000/`

---

## 🌐 Endpoints da API

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/doador/` | Lista todos os doadores |
| POST | `/doador/` | Cria novo doador |
| GET | `/doador/{id}/` | Detalhes de um doador |
| PUT | `/doador/{id}/` | Atualiza doador |
| DELETE | `/doador/{id}/` | Remove doador |
| GET | `/tipo-sanguineo/` | Lista tipos sanguíneos |
| POST | `/tipo-sanguineo/` | Cria novo tipo |

### Exemplo de requisição POST:

```json
{
  "nome": "Maria Silva",
  "data_nascimento": "1990-05-15",
  "tipo_sanguineo": 1
}
```

Interface navegável do DRF habilitada em todos os endpoints.

---

## 💡 O que esse projeto demonstra

✔ Modelagem relacional  
✔ Uso de ForeignKey  
✔ API REST estruturada  
✔ Integração Django + MySQL  
✔ Organização de código  
✔ Versionamento com Git  
✔ Boas práticas de desenvolvimento  
✔ Serialização de dados  
✔ ViewSets e Routers automáticos  

---

## 👩‍💻 Sobre mim

Sou desenvolvedora em formação,
com foco em backend e estrutura de sistemas.

Gosto de entender o que está acontecendo por trás,
não só fazer funcionar.

Se quiser conversar sobre código, projetos ou oportunidades:

📎 **GitHub:** [github.com/Paola5858](https://github.com/Paola5858)  
📎 **LinkedIn:** [linkedin.com/in/paolasoaresmachado](https://linkedin.com/in/paolasoaresmachado)

---

## 📄 Licença

Este projeto está sob a licença MIT.

---

⭐ Se este projeto te ajudou de alguma forma, considere dar uma estrela!
