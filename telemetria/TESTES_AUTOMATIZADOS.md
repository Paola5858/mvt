# 🧪 Testes Automatizados - API Telemetria

## ✅ Execução dos Testes

```bash
python manage.py test --verbosity=2
```

## 📊 Resultado

```
Found 6 test(s).
System check identified no issues (0 silenced).

test_criar_marca (api_telemetria.tests.MarcaTestCase.test_criar_marca)
Testa a criação de uma marca. ... ok

test_listar_marcas (api_telemetria.tests.MarcaTestCase.test_listar_marcas)
Testa a listagem de marcas. ... ok

test_criar_medicao_veiculo (api_telemetria.tests.MedicaoVeiculoTestCase.test_criar_medicao_veiculo)
Testa a criação de uma medição de veículo. ... ok

test_criar_modelo (api_telemetria.tests.ModeloTestCase.test_criar_modelo)
Testa a criação de um modelo. ... ok

test_criar_veiculo (api_telemetria.tests.VeiculoTestCase.test_criar_veiculo)
Testa a criação de um veículo. ... ok

test_validacao_ano_invalido (api_telemetria.tests.VeiculoTestCase.test_validacao_ano_invalido)
Testa validação de ano inválido. ... ok

----------------------------------------------------------------------
Ran 6 tests in 0.220s

OK
```

## 🎯 Cobertura de Testes

### MarcaTestCase
- ✅ Criação de marca
- ✅ Listagem de marcas

### ModeloTestCase
- ✅ Criação de modelo

### VeiculoTestCase
- ✅ Criação de veículo com FKs
- ✅ Validação de ano inválido (< 1900)

### MedicaoVeiculoTestCase
- ✅ Criação de medição de veículo com relacionamentos

## 🔍 O que é testado

1. **Endpoints funcionais** - POST, GET funcionando
2. **Validações de serializers** - Ano inválido retorna 400
3. **Relacionamentos** - ForeignKeys sendo criadas corretamente
4. **Status codes** - 201 Created, 200 OK, 400 Bad Request

## 🚀 Como rodar

```bash
# Todos os testes
python manage.py test

# Com detalhes
python manage.py test --verbosity=2

# Teste específico
python manage.py test api_telemetria.tests.VeiculoTestCase
```
