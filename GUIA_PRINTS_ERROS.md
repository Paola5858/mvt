# 📸 GUIA - Como Tirar Prints de Erros de Validação

## 🎯 Validações Implementadas

### 1️⃣ Marca
- Nome vazio → ERRO
- Nome com menos de 2 caracteres → ERRO
- Nome válido → Converte para MAIÚSCULAS

### 2️⃣ Modelo
- Nome vazio → ERRO
- Nome com menos de 2 caracteres → ERRO
- Nome válido → Converte para MAIÚSCULAS

### 3️⃣ Veículo
- Descrição vazia → ERRO
- Ano menor que 1900 ou maior que 2030 → ERRO
- Horímetro negativo → ERRO
- Horímetro maior que 999999 → ERRO

### 4️⃣ Medição de Veículo
- Valor negativo → ERRO
- Valor maior que 9999999 → ERRO

---

## 📋 Como Tirar Prints de Erros

### Opção 1: Via Interface Navegável do DRF

1. Acesse: http://127.0.0.1:8000/api/marcas/
2. Clique em "POST" (formulário HTML aparece)
3. Deixe o campo "nome" vazio
4. Clique em "POST"
5. **TIRE PRINT** do erro: "O nome da marca não pode ser vazio."

### Opção 2: Via Swagger

1. Acesse: http://127.0.0.1:8000/swagger/
2. Expanda "POST /api/marcas/"
3. Clique em "Try it out"
4. No JSON, coloque:
```json
{
  "nome": ""
}
```
5. Clique em "Execute"
6. **TIRE PRINT** da resposta com erro 400

### Opção 3: Via Postman/Insomnia

1. Crie requisição POST para http://127.0.0.1:8000/api/marcas/
2. Body (JSON):
```json
{
  "nome": ""
}
```
3. Envie
4. **TIRE PRINT** do erro

---

## 🧪 Exemplos de Requisições que Geram Erros

### ❌ Marca com nome vazio
```
POST /api/marcas/
{
  "nome": ""
}
```
**Erro esperado:** "O nome da marca não pode ser vazio."

---

### ❌ Marca com 1 caractere
```
POST /api/marcas/
{
  "nome": "F"
}
```
**Erro esperado:** "O nome da marca deve ter pelo menos 2 caracteres."

---

### ❌ Veículo com ano inválido
```
POST /api/veiculos/
{
  "descricao": "Teste",
  "marca": 1,
  "modelo": 1,
  "ano": 1800,
  "horimetro": 1000
}
```
**Erro esperado:** "O ano deve estar entre 1900 e 2030."

---

### ❌ Veículo com horímetro negativo
```
POST /api/veiculos/
{
  "descricao": "Teste",
  "marca": 1,
  "modelo": 1,
  "ano": 2020,
  "horimetro": -100
}
```
**Erro esperado:** "O horímetro não pode ser negativo."

---

### ❌ Medição com valor negativo
```
POST /api/medicoes-veiculo/
{
  "veiculo": 1,
  "medicao": 1,
  "data": "2024-01-15",
  "valor": -50
}
```
**Erro esperado:** "O valor não pode ser negativo."

---

## 📸 Sequência Recomendada de Prints

1. **Print 1:** Erro de marca vazia (via DRF interface)
2. **Print 2:** Erro de ano inválido (via Swagger)
3. **Print 3:** Erro de horímetro negativo (via DRF interface)
4. **Print 4:** Sucesso após corrigir (mostrando status 201)

---

## ✅ Exemplo de Sucesso (para comparar)

```
POST /api/marcas/
{
  "nome": "FIAT"
}
```
**Resposta esperada:**
```json
{
  "id": 1,
  "nome": "FIAT"
}
```
Status: 201 Created

---

## 🎯 Dica Pro

No Swagger, você pode ver TODOS os erros de uma vez:

1. Acesse http://127.0.0.1:8000/swagger/
2. Teste cada endpoint com dados inválidos
3. Tire print da tela mostrando múltiplos erros
4. Isso demonstra que a validação está funcionando!

---

**Agora reinicie o servidor para aplicar as validações:**

```bash
python manage.py runserver
```
