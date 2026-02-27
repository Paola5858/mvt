# boas práticas rest aplicadas

este repositório segue os princípios rest conforme definidos por roy fielding e as melhores práticas da indústria.

## 1. urls bem estruturadas

### ✅ o que fizemos certo

- **substantivos no plural**: `/animals/`, `/doadores/`, `/talhoes/`
- **sem verbos**: não usamos `/getAnimals/` ou `/createDoador/`
- **minúsculas e hífens**: `/tipos-sanguineos/` (não `/TiposSanguineos/`)
- **hierarquia clara**: recursos organizados de forma lógica

### exemplos

```
GET    /v1/doadores/           # lista doadores
POST   /v1/doadores/           # cria doador
GET    /v1/doadores/1/         # detalhe do doador 1
PUT    /v1/doadores/1/         # atualiza doador 1
DELETE /v1/doadores/1/         # remove doador 1
```

## 2. métodos http corretos

cada método tem um propósito específico e é usado corretamente:

| método | uso | idempotente | safe |
|--------|-----|-------------|------|
| GET | buscar dados | ✅ | ✅ |
| POST | criar recurso | ❌ | ❌ |
| PUT | atualizar completo | ✅ | ❌ |
| PATCH | atualizar parcial | ✅ | ❌ |
| DELETE | remover recurso | ✅ | ❌ |

### idempotência

- **GET, PUT, PATCH, DELETE**: fazer a mesma requisição N vezes produz o mesmo resultado
- **POST**: cada requisição cria um novo recurso

exemplo: deletar um recurso que já foi deletado retorna `204 No Content`, não `404 Not Found`. o objetivo foi atingido.

## 3. status codes apropriados

o drf já retorna os códigos corretos por padrão, mas aqui está o que cada endpoint retorna:

### sucesso

- `200 OK`: GET, PUT, PATCH bem-sucedidos
- `201 Created`: POST bem-sucedido (recurso criado)
- `204 No Content`: DELETE bem-sucedido

### erro do cliente

- `400 Bad Request`: dados inválidos no body
- `404 Not Found`: recurso não existe
- `409 Conflict`: conflito (ex: email duplicado)

### erro do servidor

- `500 Internal Server Error`: erro não tratado no servidor

## 4. paginação

todas as listagens têm paginação para evitar sobrecarga:

```json
GET /v1/doadores/?page=2&page_size=20

{
  "count": 150,
  "next": "http://localhost:8000/v1/doadores/?page=3",
  "previous": "http://localhost:8000/v1/doadores/?page=1",
  "results": [...]
}
```

**configuração:**
- padrão: 10 itens por página
- máximo: 100 itens por página
- customizável via `?page_size=`

## 5. filtros e busca

### filtros por campo

```
GET /v1/doadores/?tipo_sanguineo=1&ativo=true
```

### busca textual

```
GET /v1/doadores/?search=maria
```

### ordenação

```
GET /v1/doadores/?ordering=-criado_em
GET /v1/doadores/?ordering=nome
```

## 6. versionamento

apis versionadas para evitar breaking changes:

```
/v1/doadores/
/v1/tipos-sanguineos/
```

quando houver mudanças incompatíveis, criamos `/v2/` e depreciamos `/v1/` gradualmente.

## 7. relacionamentos

### foreignkey

quando um recurso referencia outro, usamos o id na criação:

```json
POST /v1/doadores/
{
  "nome": "maria",
  "tipo_sanguineo": 1
}
```

mas retornamos o objeto completo na leitura:

```json
GET /v1/doadores/1/
{
  "id": 1,
  "nome": "maria",
  "tipo_sanguineo": {
    "id": 1,
    "tipo": "O+"
  }
}
```

### evitando urls aninhadas desnecessárias

❌ **errado**: `/companies/1/users/` (usuários não são sub-conjunto de empresa)

✅ **certo**: `/users/?company=1` (filtro por empresa)

usamos sub-paths apenas quando há relação É-UM, não TEM-UM.

## 8. otimização de queries

### select_related

usado em foreignkeys para evitar n+1 queries:

```python
queryset = Doador.objects.select_related('tipo_sanguineo').all()
```

uma query em vez de N+1.

## 9. serializers inteligentes

### serializers diferentes para list e detail

- **list**: campos resumidos, mais rápido
- **detail**: todos os campos, relacionamentos expandidos

```python
def get_serializer_class(self):
    if self.action == 'list':
        return DoadorListSerializer
    return DoadorSerializer
```

### campos calculados

```python
total_doadores = serializers.SerializerMethodField()

def get_total_doadores(self, obj):
    return obj.doadores.filter(ativo=True).count()
```

## 10. documentação

### swagger/openapi

projeto telemetria tem documentação completa:

- `/swagger/` - interface interativa
- `/redoc/` - documentação limpa

cada endpoint documentado com:
- descrição
- parâmetros
- exemplos de request/response
- códigos de status possíveis

## 11. segurança

### validações

- campos únicos (email, cpf)
- choices para campos limitados (tipo sanguíneo)
- campos obrigatórios vs opcionais

### proteção contra xss

- nunca retornar dados não sanitizados em httpresponse
- usar redirect em vez de exibir dados do usuário diretamente

## 12. consistência

### padrões mantidos em todos os projetos

- nomenclatura: snake_case nos campos, kebab-case nas urls
- estrutura: models, serializers, views, urls, admin
- filtros: sempre com django-filter quando aplicável
- busca: sempre com search_fields
- ordenação: sempre com ordering_fields

## checklist rest

ao criar uma nova api, verificar:

- [ ] urls no plural
- [ ] sem verbos nas urls
- [ ] métodos http corretos
- [ ] status codes apropriados
- [ ] paginação configurada
- [ ] filtros implementados
- [ ] busca funcional
- [ ] ordenação disponível
- [ ] versionamento definido
- [ ] relacionamentos bem modelados
- [ ] queries otimizadas (select_related)
- [ ] serializers eficientes
- [ ] documentação completa
- [ ] validações implementadas

## referências

- [REST API Best Practices](https://restfulapi.net/rest-api-best-practices/)
- [Roy Fielding - Architectural Styles](https://www.ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm)
- [Django REST Framework](https://www.django-rest-framework.org/)

---

**resultado**: apis profissionais, escaláveis e fáceis de manter. prontas para produção.
