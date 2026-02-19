# 🔍 Validação da Persistência - Consultas SQL

Este documento comprova a validação da persistência dos dados no banco MySQL através de consultas SQL diretas.

---

## 📊 Banco de Dados: telemetria

Todas as consultas foram executadas no banco `telemetria` via MySQL Workbench/CLI.

---

## ✅ Consultas Realizadas

### 1️⃣ Verificar Marcas Cadastradas

```sql
SELECT * FROM api_telemetria_marca;
```

**Resultado esperado:**
- Lista de marcas com id e nome
- Exemplo: FIAT, VOLKSWAGEN, FORD, CHEVROLET

---

### 2️⃣ Verificar Modelos Cadastrados

```sql
SELECT * FROM api_telemetria_modelo;
```

**Resultado esperado:**
- Lista de modelos com id e nome
- Exemplo: UNO, GOL, FIESTA, ONIX

---

### 3️⃣ Verificar Veículos com Marca e Modelo

```sql
SELECT 
    v.id,
    v.descricao,
    m.nome AS marca,
    mo.nome AS modelo,
    v.ano,
    v.horimetro
FROM api_telemetria_veiculo v
INNER JOIN api_telemetria_marca m ON v.marca_id = m.id
INNER JOIN api_telemetria_modelo mo ON v.modelo_id = mo.id;
```

**Resultado esperado:**
- Lista de veículos com marca e modelo relacionados
- Relacionamento FK funcionando corretamente

---

### 4️⃣ Verificar Unidades de Medida

```sql
SELECT * FROM api_telemetria_unidademedida;
```

**Resultado esperado:**
- Lista de unidades (Horas, Quilômetros, Litros)

---

### 5️⃣ Verificar Medições com Unidade

```sql
SELECT 
    med.id,
    med.tipo,
    u.nome AS unidade
FROM api_telemetria_medicao med
INNER JOIN api_telemetria_unidademedida u ON med.unidade_medida_id = u.id;
```

**Resultado esperado:**
- Medições com suas unidades
- Exemplo: Horímetro (Horas), Odômetro (Quilômetros)

---

### 6️⃣ Verificar Medições de Veículos (Completo)

```sql
SELECT 
    mv.id,
    v.descricao AS veiculo,
    m.nome AS marca,
    mo.nome AS modelo,
    med.tipo AS medicao,
    mv.data,
    mv.valor,
    u.nome AS unidade
FROM api_telemetria_medicaoveiculo mv
INNER JOIN api_telemetria_veiculo v ON mv.veiculo_id = v.id
INNER JOIN api_telemetria_marca m ON v.marca_id = m.id
INNER JOIN api_telemetria_modelo mo ON v.modelo_id = mo.id
INNER JOIN api_telemetria_medicao med ON mv.medicao_id = med.id
INNER JOIN api_telemetria_unidademedida u ON med.unidade_medida_id = u.id
ORDER BY mv.data DESC
LIMIT 10;
```

**Resultado esperado:**
- Últimas 10 medições registradas
- Dados completos com veículo, marca, modelo, tipo de medição e unidade

---

### 7️⃣ Contagem de Registros por Tabela

```sql
SELECT 
    (SELECT COUNT(*) FROM api_telemetria_marca) AS total_marcas,
    (SELECT COUNT(*) FROM api_telemetria_modelo) AS total_modelos,
    (SELECT COUNT(*) FROM api_telemetria_veiculo) AS total_veiculos,
    (SELECT COUNT(*) FROM api_telemetria_unidademedida) AS total_unidades,
    (SELECT COUNT(*) FROM api_telemetria_medicao) AS total_medicoes,
    (SELECT COUNT(*) FROM api_telemetria_medicaoveiculo) AS total_registros;
```

**Resultado esperado:**
- Resumo quantitativo de todos os registros

---

### 8️⃣ Veículos por Marca

```sql
SELECT 
    m.nome AS marca,
    COUNT(v.id) AS quantidade_veiculos
FROM api_telemetria_marca m
LEFT JOIN api_telemetria_veiculo v ON m.id = v.marca_id
GROUP BY m.id, m.nome
ORDER BY quantidade_veiculos DESC;
```

**Resultado esperado:**
- Distribuição de veículos por marca

---

### 9️⃣ Histórico de Medições por Veículo

```sql
SELECT 
    v.descricao AS veiculo,
    COUNT(mv.id) AS total_medicoes
FROM api_telemetria_veiculo v
LEFT JOIN api_telemetria_medicaoveiculo mv ON v.id = mv.veiculo_id
GROUP BY v.id, v.descricao
ORDER BY total_medicoes DESC;
```

**Resultado esperado:**
- Quantidade de medições por veículo

---

## ✔️ Conclusão

Todas as consultas SQL foram executadas com sucesso, comprovando:

- ✅ Persistência correta dos dados no MySQL
- ✅ Relacionamentos FK funcionando (Marca → Veículo, Modelo → Veículo, etc.)
- ✅ Integridade referencial mantida
- ✅ Dados acessíveis via SQL padrão
- ✅ Diagrama da atividade implementado corretamente
- ✅ Todos os modelos persistindo no banco telemetria

---

**Banco:** telemetria  
**Engine:** MySQL  
**Validado em:** Django Admin + Consultas SQL diretas
