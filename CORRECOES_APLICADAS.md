# ✅ Checklist de Correções Aplicadas

## Projeto `animal/` (CRUD com FBV)

- [x] Corrigido `{{ animal.especie }}` → `{{ animal.tutor }}` no template listar.html
- [x] Renomeado `class AppConfig` → `class AppAppConfig` em apps.py
- [x] Trocado `id` por `pk` nas views (editar_animal, deletar_animal)
- [x] Trocado `id` por `pk` nas URLs (setup/urls.py)
- [x] Configurado `LANGUAGE_CODE = 'pt-br'` e `TIME_ZONE = 'America/Sao_Paulo'`
- [x] Criado `.env.example` para documentar variáveis de ambiente
- [x] Criado `.gitignore` específico do projeto
- [x] Criado `requirements.txt` específico do projeto
- [x] Criado `README.md` específico do projeto

### ⚠️ Pendente (requer ação manual):
- [ ] Mover SECRET_KEY para .env (requer instalação de python-decouple)

---

## Projeto `animais/` (DRF com dois apps)

- [x] Adicionado `'api_animal'` ao INSTALLED_APPS em settings.py
- [x] Incluído `path('', include('api_animal.urls'))` em urls.py
- [x] Removido arquivo duplicado `api_animal/viewsets.py`
- [x] Registrado model `Talhao` no admin (api_talhao/admin.py)
- [x] Configurado `LANGUAGE_CODE = 'pt-br'` e `TIME_ZONE = 'America/Sao_Paulo'`
- [x] Criado `requirements.txt` específico do projeto
- [x] Criado `README.md` específico do projeto

### ⚠️ Pendente (requer ação manual):
- [ ] Mover SECRET_KEY para .env (requer instalação de python-decouple)
- [ ] Rodar `python manage.py makemigrations` e `python manage.py migrate` para api_animal

---

## Repositório raiz

- [x] Movido README.md (que descrevia projeto doador) para `doador/README_DOADOR.md`
- [x] Criado novo README.md principal descrevendo o repositório como caderno de estudos
- [x] Atualizado requirements.txt com comentários explicando dependências opcionais
- [x] .gitignore já estava correto (mantido)

---

## Estrutura final do repositório

```
mvt/
├── README.md                    ← novo: descreve o repositório como caderno de estudos
├── requirements.txt             ← atualizado: com comentários
├── .gitignore                   ← mantido
├── CORRECOES_APLICADAS.md      ← este arquivo
│
├── animal/                      ← projeto 01: CRUD com FBV
│   ├── README.md               ← novo
│   ├── requirements.txt        ← novo
│   ├── .gitignore              ← novo
│   └── .env.example            ← novo
│
├── animais/                     ← projeto 02: DRF com múltiplos recursos
│   ├── README.md               ← novo
│   └── requirements.txt        ← novo
│
├── doador/                      ← projeto 03: DRF com ForeignKey
│   ├── README.md               ← já existia
│   └── README_DOADOR.md        ← movido da raiz
│
├── primeiro/                    ← projeto 04: CRUD básico
│   └── (sem alterações)
│
└── telemetria/                  ← projeto 05: API com telemetria
    └── (já tinha .env, .gitignore, README.md)
```

---

## Próximos passos recomendados

### 1. Configurar variáveis de ambiente nos projetos `animal/` e `animais/`

```bash
# Em cada projeto:
pip install python-decouple
```

Depois, em `settings.py`:

```python
from decouple import config

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
```

E criar arquivo `.env`:

```
SECRET_KEY=sua-secret-key-aqui
DEBUG=True
```

### 2. Rodar migrações do api_animal

```bash
cd animais/
python manage.py makemigrations api_animal
python manage.py migrate
```

### 3. Testar todos os endpoints

- `animal/`: testar CRUD via templates
- `animais/`: testar `/animals/` e `/talhoes/`
- `doador/`: testar `/doador/` e `/tipo-sanguineo/`

### 4. Criar READMEs para `primeiro/` e revisar `telemetria/`

Os projetos `primeiro/` e `telemetria/` também merecem READMEs individuais seguindo o mesmo padrão.

---

## Resumo do que foi corrigido

| Problema | Status |
|----------|--------|
| Campo `especie` inexistente no template | ✅ Corrigido |
| Classe `AppConfig` duplicada | ✅ Corrigido |
| Uso de `id` em vez de `pk` | ✅ Corrigido |
| `api_animal` fora do INSTALLED_APPS | ✅ Corrigido |
| URLs de `api_animal` não incluídas | ✅ Corrigido |
| Arquivo `viewsets.py` duplicado | ✅ Removido |
| `Talhao` não registrado no admin | ✅ Corrigido |
| LANGUAGE_CODE e TIME_ZONE em inglês | ✅ Corrigido |
| README descrevendo projeto errado | ✅ Corrigido |
| Falta de READMEs individuais | ✅ Criados |
| requirements.txt sem contexto | ✅ Atualizado |
| SECRET_KEY exposta | ⚠️ Documentado (requer ação manual) |

---

**Data das correções:** 2025  
**Responsável:** Amazon Q Developer
