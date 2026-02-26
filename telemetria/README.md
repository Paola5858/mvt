# 📡 API Telemetria de Veículos - SA1-E1

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Django](https://img.shields.io/badge/Django-5.x-green)
![DRF](https://img.shields.io/badge/DRF-3.x-red)
![MySQL](https://img.shields.io/badge/MySQL-8.x-orange)
![Swagger](https://img.shields.io/badge/Docs-Swagger-brightgreen)

API REST completa para gerenciamento de telemetria de veículos.  
Desenvolvida com Django Rest Framework + MySQL.

**Repositório da atividade:** TELEMETRIA - PBE-4 - APIs de Cadastro

---

## 🎯 Objetivo da Atividade

Criar APIs REST conforme diagrama fornecido, com:
- Modelagem de dados relacional
- CRUD completo em JSON
- Conexão com MySQL (banco `telemetria`)
- Documentação Swagger
- Testes via Django Admin

---

## 🗂️ Modelagem de Dados

### 📊 Diagrama Implementado

```
Marca (1) ──→ (N) Veiculo (1) ──→ (N) MedicaoVeiculo
Modelo (1) ──→ (N) Veiculo
UnidadeMedida (1) ──→ (N) Medicao (1) ──→ (N) MedicaoVeiculo
```

### 🚗 Marca
- `id` (PK)
- `nome` (CharField)

### 📝 Modelo
- `id` (PK)
- `nome` (CharField)

### 🚚 Veiculo
- `id` (PK)
- `descricao` (CharField)
- `marca` (FK → Marca)
- `modelo` (FK → Modelo)
- `ano` (IntegerField)
- `horimetro` (FloatField)

### 📏 UnidadeMedida
- `id` (PK)
- `nome` (CharField)

### 📊 Medicao
- `id` (PK)
- `tipo` (CharField com choices: horimetro, odometro, combustivel)
- `unidade_medida` (FK → UnidadeMedida)

### 📝 MedicaoVeiculo
- `id` (PK)
- `veiculo` (FK → Veiculo)
- `medicao` (FK → Medicao)
- `data` (DateField)
- `valor` (FloatField)

**Relacionamentos:**
- Marca → Veiculo (1:N, CASCADE)
- Modelo → Veiculo (1:N, CASCADE)
- UnidadeMedida → Medicao (1:N, CASCADE)
- Veiculo → MedicaoVeiculo (1:N, CASCADE)
- Medicao → MedicaoVeiculo (1:N, CASCADE)

---

## 🚀 Tecnologias

- Python 3.x
- Django 5.x
- Django Rest Framework 3.x
- drf-yasg (Swagger/OpenAPI)
- MySQL 8.x
- mysqlclient

---

## 🔌 Configuração do Banco

**Banco:** `telemetria`

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'telemetria',
        'USER': 'root',
        'PASSWORD': 'sua_senha',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

---

## ⚙️ Como Rodar

### 1️⃣ Clonar o repositório
```bash
git clone <url-do-repo>
cd mvt/telemetria
```

### 2️⃣ Criar ambiente virtual
```bash
python -m venv .venv
.\.venv\Scripts\Activate  # Windows
```

### 3️⃣ Instalar dependências
```bash
pip install -r requirements.txt
```

### 4️⃣ Configurar variáveis de ambiente

Copie o arquivo de exemplo e preencha com suas credenciais:

```bash
cp .env.example .env  # Linux/Mac
copy .env.example .env  # Windows
```

Edite o `.env` com sua senha do MySQL:

```env
DB_NAME=telemetria
DB_USER=root
DB_PASSWORD=sua_senha_aqui
DB_HOST=localhost
DB_PORT=3306
```

### 5️⃣ Configurar MySQL

Crie o banco de dados:

```sql
CREATE DATABASE telemetria;
```

### 6️⃣ Rodar migrações
```bash
python manage.py makemigrations
python manage.py migrate
```

### 7️⃣ Criar superusuário
```bash
python manage.py createsuperuser
```

### 8️⃣ Iniciar servidor
```bash
python manage.py runserver
```

---

## 🌐 Endpoints da API

### Marca
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/marcas/` | Lista marcas |
| POST | `/api/marcas/` | Cria marca |
| GET | `/api/marcas/{id}/` | Detalhe |
| PUT | `/api/marcas/{id}/` | Atualiza |
| DELETE | `/api/marcas/{id}/` | Remove |

### Modelo
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/modelos/` | Lista modelos |
| POST | `/api/modelos/` | Cria modelo |
| GET | `/api/modelos/{id}/` | Detalhe |
| PUT | `/api/modelos/{id}/` | Atualiza |
| DELETE | `/api/modelos/{id}/` | Remove |

### Veiculo
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/veiculos/` | Lista veículos |
| POST | `/api/veiculos/` | Cria veículo |
| GET | `/api/veiculos/{id}/` | Detalhe |
| PUT | `/api/veiculos/{id}/` | Atualiza |
| DELETE | `/api/veiculos/{id}/` | Remove |

### UnidadeMedida
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/unidades-medida/` | Lista unidades |
| POST | `/api/unidades-medida/` | Cria unidade |
| GET | `/api/unidades-medida/{id}/` | Detalhe |
| PUT | `/api/unidades-medida/{id}/` | Atualiza |
| DELETE | `/api/unidades-medida/{id}/` | Remove |

### Medicao
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/medicoes/` | Lista medições |
| POST | `/api/medicoes/` | Cria medição |
| GET | `/api/medicoes/{id}/` | Detalhe |
| PUT | `/api/medicoes/{id}/` | Atualiza |
| DELETE | `/api/medicoes/{id}/` | Remove |

### MedicaoVeiculo
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/medicoes-veiculo/` | Lista registros |
| POST | `/api/medicoes-veiculo/` | Cria registro |
| GET | `/api/medicoes-veiculo/{id}/` | Detalhe |
| PUT | `/api/medicoes-veiculo/{id}/` | Atualiza |
| DELETE | `/api/medicoes-veiculo/{id}/` | Remove |

---

## 📖 Documentação Swagger

A API está documentada seguindo o padrão OpenAPI/Swagger:

- **Swagger UI:** http://localhost:8000/swagger/
- **ReDoc:** http://localhost:8000/redoc/

Implementado com `drf-yasg`.

---

## 🖥️ Django Admin

Acesse: http://localhost:8000/admin/

**Funcionalidades:**
- ✅ Cadastro de Marcas
- ✅ Cadastro de Modelos
- ✅ Cadastro de Veículos (com FK para Marca e Modelo)
- ✅ Cadastro de Unidades de Medida
- ✅ Cadastro de Medições (com FK para UnidadeMedida)
- ✅ Cadastro de Medições de Veículo (com FKs)
- ✅ Busca e filtros customizados

**Documentação dos testes:** Ver arquivo `../PRINTS_CADASTROS.md`

---

## 🔍 Validação da Persistência

Consultas SQL executadas no banco `telemetria`:

```sql
-- Listar veículos com marca e modelo
SELECT v.*, m.nome AS marca, mo.nome AS modelo 
FROM api_telemetria_veiculo v
JOIN api_telemetria_marca m ON v.marca_id = m.id
JOIN api_telemetria_modelo mo ON v.modelo_id = mo.id;

-- Listar medições de veículos
SELECT mv.*, v.descricao, med.tipo 
FROM api_telemetria_medicaoveiculo mv
JOIN api_telemetria_veiculo v ON mv.veiculo_id = v.id
JOIN api_telemetria_medicao med ON mv.medicao_id = med.id
ORDER BY mv.data DESC;
```

**Documentação completa:** Ver arquivo `../TESTES_SQL.md`

---

## 🧪 Rodando os Testes

Execute os testes automatizados:

```bash
python manage.py test
```

Para testes com mais detalhes:

```bash
python manage.py test --verbosity=2
```

Resultado esperado:

```
Found 6 test(s).
System check identified no issues (0 silenced).

test_criar_marca ... ok
test_listar_marcas ... ok
test_criar_modelo ... ok
test_criar_veiculo ... ok
test_validacao_ano_invalido ... ok
test_criar_medicao_veiculo ... ok

----------------------------------------------------------------------
Ran 6 tests in 0.234s

OK
```

---

## 📋 Exemplos de Requisições

### POST /api/marcas/
```json
{
  "nome": "FIAT"
}
```

### POST /api/modelos/
```json
{
  "nome": "UNO"
}
```

### POST /api/veiculos/
```json
{
  "descricao": "Veículo de transporte",
  "marca": 1,
  "modelo": 1,
  "ano": 2020,
  "horimetro": 15000.0
}
```

### POST /api/unidades-medida/
```json
{
  "nome": "Horas"
}
```

### POST /api/medicoes/
```json
{
  "tipo": "horimetro",
  "unidade_medida": 1
}
```

### POST /api/medicoes-veiculo/
```json
{
  "veiculo": 1,
  "medicao": 1,
  "data": "2024-01-15",
  "valor": 15000.0
}
```

---

## ✅ Checklist da Atividade

- ✅ APIs criadas conforme diagrama (Marca, Modelo, Veiculo, UnidadeMedida, Medicao, MedicaoVeiculo)
- ✅ Modelagem com ForeignKeys corretas
- ✅ CRUD completo (Create, Read, Update, Delete)
- ✅ Formato JSON (via DRF Serializers)
- ✅ Conexão com MySQL (banco `telemetria`)
- ✅ Testes via Django Admin (ver `PRINTS_CADASTROS.md`)
- ✅ Validação SQL (ver `TESTES_SQL.md`)
- ✅ Documentação Swagger (drf-yasg)
- ✅ Repositório no GitHub
- ✅ README completo
- ✅ Testes automatizados (ver `TESTES_AUTOMATIZADOS.md`)
- ✅ Variáveis de ambiente com python-decouple
- ✅ Permissões configuradas (AllowAny)

---

## 📁 Estrutura do Projeto

```
telemetria/
├── api_telemetria/
│   ├── models.py          # Marca, Modelo, Veiculo, UnidadeMedida, Medicao, MedicaoVeiculo
│   ├── serializers.py     # Serializers DRF
│   ├── views.py           # ViewSets
│   ├── admin.py           # Config admin
│   └── migrations/
├── setup/
│   ├── settings.py        # Config MySQL + DRF
│   ├── urls.py            # Rotas + Swagger
│   └── wsgi.py
├── requirements.txt
├── manage.py
├── .env.example           # Template de variáveis
├── .env                   # Credenciais (não commitado)
├── PRINTS_CADASTROS.md    # Evidências admin
├── TESTES_SQL.md          # Validação SQL
└── TESTES_AUTOMATIZADOS.md # Testes unitários
```

---

## 🎓 Competências Demonstradas

- Modelagem relacional (1:N)
- API REST com Django Rest Framework
- Integração com banco MySQL
- Serialização JSON
- ViewSets e Routers
- Documentação OpenAPI/Swagger
- Django Admin customizado
- Validação de dados
- Versionamento Git
- Testes automatizados (TDD)
- Segurança (variáveis de ambiente)
- Boas práticas de desenvolvimento

---

## 👩💻 Autora

**Paola Soares Machado**

📎 GitHub: [github.com/Paola5858](https://github.com/Paola5858)  
📎 LinkedIn: [linkedin.com/in/paolasoaresmachado](https://linkedin.com/in/paolasoaresmachado)

---

⭐ Projeto desenvolvido como atividade avaliativa - PBE-4 - SENAI
