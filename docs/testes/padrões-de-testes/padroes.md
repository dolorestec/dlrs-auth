# Padrões de Testes

Este documento descreve os padrões de testes adotados no projeto Dolorestec Auth.

## Framework de Testes

- **pytest**: Framework principal para testes unitários e integração
- **pytest-asyncio**: Suporte a testes assíncronos
- **pytest-cov**: Medição de cobertura de código

## Tipos de Testes

- **Unitários**: Testam unidades isoladas (funções, classes) com mocks
- **Integração**: Testam interações entre componentes (BD, cache, mensageria)
- **Funcionais**: Cenários end-to-end de autenticação

## Estrutura de Testes

- Diretório `tests/` espelhando `app/`
- Arquivos nomeados `test_*.py`
- Funções nomeadas `test_*`
- Fixtures para setup reutilizável

## Cobertura

- Meta: >80% de cobertura de código
- Exclusões: código de configuração, dependências externas

## Mocking e Stubbing

- **unittest.mock**: Para isolamento de dependências
- Mocks para BD, Redis, RabbitMQ em testes unitários
- Testcontainers para testes de integração reais

## Testes Assíncronos

- Uso de `pytest.mark.asyncio` para funções async
- Validação de operações I/O não bloqueantes

## Relatórios

- Relatórios HTML de cobertura
- Integração com CI/CD para execução automática
