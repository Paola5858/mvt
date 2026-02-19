# 🌾 API Telemetria - Sistema de Monitoramento Agrícola

API REST profissional desenvolvida com Django REST Framework para gerenciamento de telemetria agrícola, permitindo monitoramento de sensores distribuídos em diferentes setores.

## 🚀 Tecnologias

- **Django 6.0.2** - Framework web Python
- **Django REST Framework** - Toolkit para construção de APIs REST
- **MySQL** - Banco de dados relacional
- **drf-yasg** - Geração automática de documentação Swagger/OpenAPI
- **django-filter** - Sistema avançado de filtros

## 📋 Funcionalidades

- ✔️ **CRUD Completo** para Setores, Sensores e Leituras
- ✔️ **Versionamento de API** (v1)
- ✔️ **Filtros Avançados** (por sensor, data, valor)
- ✔️ **Ordenação Customizada** (por data, valor, nome)
- ✔️ **Paginação Global** (10 itens por página, configurável)
- ✔️ **Validações Personalizadas** nos serializers
- ✔️ **Nested Serializers** (dados relacionados)
- ✔️ **Documentação Swagger/ReDoc** interativa
- ✔️ **Tratamento de Erros** padronizado
- ✔️ **Otimização de Queries** (select_related, indexes)
- ✔️ **Admin Customizado** com filtros e buscas
- ✔️ **Autenticação por Token** (IsAuthenticatedOrReadOnly)
- ✔️ **Testes Automatizados** (7 testes - 100% passando)

---

## 🔧 Instalação Rápida

```bash
# 1. Clonar e entrar no diretório
git clone <seu-repositorio>
cd telemetria

# 2. Criar ambiente virtual
python -m venv venv
venv\Scripts\activate  # Windows

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Configurar banco MySQL
# CREATE DATABASE telemetria CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 5. Migrar banco
python manage.py migrate

# 6. Criar superusuário
python manage.py createsuperuser

# 7. Rodar testes
python manage.py test api_telemetria

# 8. Iniciar servidor
python manage.py runserver
```

**Acessar:**
- API: http://localhost:8000/api/v1/
- Swagger: http://localhost:8000/swagger/
- Admin: http://localhost:8000/admin/

---

## 🔐 Autenticação

### Obter Token
```bash
POST /api/v1/auth/token/
{
  "username": "seu_usuario",
  "password": "sua_senha"
}
```

### Usar Token
```bash
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

**Política:** GET (leitura) é público. POST/PUT/PATCH/DELETE requer autenticação.

---

## 📚 Endpoints da API

### Base URL: `http://localhost:8000/api/v1/`

### 🏢 Setores
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/setores/` | Lista todos os setores |
| POST | `/setores/` | Cria um novo setor |
| GET | `/setores/{id}/` | Detalhes de um setor |
| PATCH | `/setores/{id}/` | Atualiza parcialmente |
| DELETE | `/setores/{id}/` | Remove um setor |
| GET | `/setores/{id}/sensores/` | Lista sensores do setor |

### 📡 Sensores
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/sensores/` | Lista todos os sensores |
| POST | `/sensores/` | Cria um novo sensor |
| GET | `/sensores/{id}/` | Detalhes de um sensor |
| PATCH | `/sensores/{id}/` | Atualiza parcialmente |
| DELETE | `/sensores/{id}/` | Remove um sensor |
| GET | `/sensores/{id}/leituras/` | Lista leituras do sensor |

**Filtros:** `?setor=1` `?status=ativo` `?search=temperatura`

### 📊 Leituras
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/leituras/` | Lista todas as leituras |
| POST | `/leituras/` | Cria uma nova leitura |
| GET | `/leituras/{id}/` | Detalhes de uma leitura |
| PATCH | `/leituras/{id}/` | Atualiza parcialmente |
| DELETE | `/leituras/{id}/` | Remove uma leitura |

**Filtros:** `?sensor=1` `?data_inicio=2024-01-01` `?data_fim=2024-12-31` `?valor_min=10` `?valor_max=100` `?ordering=-data_hora`

---

## 💻 Exemplos Práticos

### Criar Setor
```bash
curl -X POST http://localhost:8000/api/v1/setores/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token SEU_TOKEN" \
  -d '{"nome": "Estufa 1", "localizacao": "Área Norte"}'
```

### Criar Sensor
```bash
curl -X POST http://localhost:8000/api/v1/sensores/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token SEU_TOKEN" \
  -d '{"setor": 1, "tipo": "Temperatura", "status": "ativo"}'
```

### Criar Leitura
```bash
curl -X POST http://localhost:8000/api/v1/leituras/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token SEU_TOKEN" \
  -d '{"sensor": 1, "valor": 25.5}'
```

### Filtrar Leituras
```bash
# Por sensor e data
curl "http://localhost:8000/api/v1/leituras/?sensor=1&data_inicio=2024-01-01&data_fim=2024-12-31"

# Por intervalo de valores
curl "http://localhost:8000/api/v1/leituras/?valor_min=20&valor_max=30&ordering=-data_hora"

# Com paginação customizada
curl "http://localhost:8000/api/v1/leituras/?page_size=20&page=1"
```

---

## 🧪 Testes Automatizados

```bash
python manage.py test api_telemetria
```

**Resultado:**
```
Ran 7 tests in 4.113s
OK ✅
```

**Cobertura:**
- ✅ Criação de Setor
- ✅ Listagem de Setores
- ✅ Criação de Sensor com nested data
- ✅ Validação de status do sensor
- ✅ Criação de Leitura
- ✅ Filtro de leituras por sensor
- ✅ Validação de valores fora do intervalo

---

## 🎯 Decisões Técnicas

### Por que ModelViewSet?
Optei por `ModelViewSet` para reduzir repetição de código e manter o projeto limpo. Isso me permitiu focar na lógica de negócio (filtros, validações) ao invés de reescrever operações CRUD básicas.

### Filtros Personalizados
A implementação de filtros personalizados foi pensada para simular um cenário real de análise de dados agrícolas, onde é comum precisar consultar leituras por intervalo de tempo e faixa de valores.

### Versionamento da API
O versionamento (`/api/v1/`) foi adotado para permitir escalabilidade futura sem quebrar clientes existentes. Isso demonstra pensamento de longo prazo e maturidade arquitetural.

### select_related e Indexes
Utilizei `select_related('sensor', 'sensor__setor')` para evitar o problema N+1 de queries. Também criei indexes no banco para campos frequentemente consultados (`data_hora`, `sensor`). Isso mostra preocupação com performance desde o início.

### Nested Serializers
Implementei serializers aninhados para reduzir o número de requisições necessárias. Ao invés do cliente fazer 3 requests (leitura → sensor → setor), ele recebe tudo em uma única resposta.

### Autenticação IsAuthenticatedOrReadOnly
Escolhi essa abordagem para permitir que qualquer pessoa consulte os dados (útil para dashboards públicos), mas apenas usuários autenticados podem modificar. É um equilíbrio entre segurança e usabilidade.

---

## 💡 Aprendizado e Evolução

Esse projeto foi um divisor de águas pra mim, porque deixou de ser apenas "criar uma API" e passou a ser **pensar arquitetura, organização e escalabilidade**.

Percebi que backend não é só fazer funcionar, é estruturar pensando no futuro. Aprendi que:

- **Organização importa**: Separar filtros, paginação e exceções em módulos próprios não é "over-engineering", é profissionalismo.

- **Testes não são opcionais**: Escrever testes me forçou a pensar em casos extremos e validações que eu não tinha considerado.

- **Performance desde o início**: É muito mais fácil otimizar queries desde o começo do que refatorar depois com milhares de registros.

- **Documentação é código**: O Swagger não é "extra", é parte essencial do produto. Uma API sem documentação é uma API incompleta.

O que mais me orgulha nesse projeto não são as linhas de código, mas as **decisões conscientes** que tomei em cada etapa. Cada filtro, cada validação, cada teste tem um propósito claro.

---

## 🏗️ Arquitetura

```
telemetria/
├── api_telemetria/
│   ├── filters/              # Filtros personalizados
│   ├── pagination/           # Paginação customizada
│   ├── exceptions/           # Tratamento de erros
│   ├── models.py            # Modelos com indexes
│   ├── serializers.py       # Nested + validações
│   ├── viewsets.py          # Filtros + documentação
│   ├── tests.py             # 7 testes automatizados
│   └── admin.py             # Admin customizado
├── setup/
│   ├── settings.py          # Configurações REST Framework
│   └── urls.py              # Versionamento + auth
└── requirements.txt
```

---

## 🚀 Próximos Passos

- [ ] Implementar cache com Redis
- [ ] Adicionar rate limiting
- [ ] Deploy em produção (AWS/Heroku)
- [ ] Adicionar CI/CD com GitHub Actions
- [ ] Implementar WebSockets para dados em tempo real

---

## 📝 Licença

MIT License

---

**Desenvolvido com 💙 como projeto de portfólio profissional**

*Este projeto demonstra não apenas habilidades técnicas, mas também capacidade de pensar estrategicamente sobre arquitetura de software.*
