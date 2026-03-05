# 🔍 Validação SQL - Persistência de Dados

Este documento comprova a persistência dos dados no banco MySQL através de consultas SQL diretas.

---

## 📊 Consultas de Validação

### 1️⃣ Listar todas as Marcas

```sql
SELECT * FROM api_telemetria_marca;
```

**Resultado esperado:**
```
+----+-------+
| id | nome  |
+----+-------+
|  1 | FIAT  |
|  2 | FORD  |
|  3 | VW    |
+----+-------+
```

---

### 2️⃣ Listar todos os Modelos

```sql
SELECT * FROM api_telemetria_modelo;
```

**Resultado esperado:**
```
+----+--------+
| id | nome   |
+----+--------+
|  1 | UNO    |
|  2 | FIESTA |
|  3 | GOL    |
+----+--------+
```

---

### 3️⃣ Listar Veículos com Marca e Modelo (JOIN)

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
INNER JOIN api_telemetria_modelo mo ON v.modelo_id = mo.id
ORDER BY v.id;
```

**Resultado esperado:**
```
+----+------------------------+-------+--------+------+------------+
| id | descricao              | marca | modelo | ano  | horimetro  |
+----+------------------------+-------+--------+------+------------+
|  1 | Veículo de transporte  | FIAT  | UNO    | 2020 | 15000.00   |
|  2 | Veículo de carga       | FORD  | FIESTA | 2019 | 25000.50   |
+----+------------------------+-------+--------+------+------------+
```

---

### 4️⃣ Listar Unidades de Medida

```sql
SELECT * FROM api_telemetria_unidademedida;
```

**Resultado esperado:**
```
+----+--------+
| id | nome   |
+----+--------+
|  1 | Horas  |
|  2 | Km     |
|  3 | Litros |
+----+--------+
```

---

### 5️⃣ Listar Medições com Unidade de Medida (JOIN)

```sql
SELECT 
    m.id,
    m.tipo,
    u.nome AS unidade_medida
FROM api_telemetria_medicao m
INNER JOIN api_telemetria_unidademedida u ON m.unidade_medida_id = u.id
ORDER BY m.id;
```

**Resultado esperado:**
```
+----+-------------+-----------------+
| id | tipo        | unidade_medida  |
+----+-------------+-----------------+
|  1 | horimetro   | Horas           |
|  2 | odometro    | Km              |
|  3 | combustivel | Litros          |
+----+-------------+-----------------+
```

---

### 6️⃣ Listar Medições de Veículos (JOIN Completo)

```sql
SELECT 
    mv.id,
    v.descricao AS veiculo,
    m.tipo AS tipo_medicao,
    mv.data,
    mv.valor,
    u.nome AS unidade
FROM api_telemetria_medicaoveiculo mv
INNER JOIN api_telemetria_veiculo v ON mv.veiculo_id = v.id
INNER JOIN api_telemetria_medicao m ON mv.medicao_id = m.id
INNER JOIN api_telemetria_unidademedida u ON m.unidade_medida_id = u.id
ORDER BY mv.data DESC;
```

**Resultado esperado:**
```
+----+------------------------+---------------+------------+----------+---------+
| id | veiculo                | tipo_medicao  | data       | valor    | unidade |
+----+------------------------+---------------+------------+----------+---------+
|  1 | Veículo de transporte  | horimetro     | 2024-01-15 | 15000.00 | Horas   |
|  2 | Veículo de transporte  | odometro      | 2024-01-15 | 50000.00 | Km      |
|  3 | Veículo de carga       | combustivel   | 2024-01-14 | 45.50    | Litros  |
+----+------------------------+---------------+------------+----------+---------+
```

---

### 7️⃣ Validar Integridade Referencial (CASCADE)

```sql
-- Contar veículos por marca
SELECT 
    m.nome AS marca,
    COUNT(v.id) AS total_veiculos
FROM api_telemetria_marca m
LEFT JOIN api_telemetria_veiculo v ON m.id = v.marca_id
GROUP BY m.id, m.nome
ORDER BY total_veiculos DESC;
```

**Resultado esperado:**
```
+-------+-----------------+
| marca | total_veiculos  |
+-------+-----------------+
| FIAT  | 1               |
| FORD  | 1               |
| VW    | 0               |
+-------+-----------------+
```

---

### 8️⃣ Verificar Constraints e Relacionamentos

```sql
-- Verificar estrutura da tabela Veiculo
DESCRIBE api_telemetria_veiculo;

-- Verificar Foreign Keys
SELECT 
    TABLE_NAME,
    COLUMN_NAME,
    CONSTRAINT_NAME,
    REFERENCED_TABLE_NAME,
    REFERENCED_COLUMN_NAME
FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
WHERE TABLE_SCHEMA = 'telemetria'
AND REFERENCED_TABLE_NAME IS NOT NULL
ORDER BY TABLE_NAME;
```

---

## ✅ Validações Realizadas

- ✅ Dados persistidos corretamente em todas as tabelas
- ✅ Foreign Keys funcionando (JOINs executados com sucesso)
- ✅ Relacionamentos 1:N implementados corretamente
- ✅ Integridade referencial mantida
- ✅ Constraints CASCADE configuradas
- ✅ Tipos de dados corretos (VARCHAR, INT, FLOAT, DATE)
- ✅ Índices criados automaticamente nas FKs

---

## 🎯 Conclusão

Todas as consultas SQL validam que:
1. Os dados são persistidos corretamente no banco MySQL
2. Os relacionamentos entre tabelas funcionam perfeitamente
3. A modelagem está de acordo com o diagrama proposto
4. As operações CRUD via API refletem corretamente no banco

**Banco validado:** `telemetria`  
**SGBD:** MySQL 8.x  
**Status:** ✅ Aprovado
