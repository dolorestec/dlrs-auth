# Lista de Tarefas para Melhorias de Qualidade e Desenvolvimento Contínuo

Baseado nas instruções do projeto Dolorestec Auth, aqui está uma lista de tarefas focadas em melhorias de qualidade e desenvolvimento contínuo:

## Melhorias de Qualidade de Código
- [ ] Executar linting com Ruff: `ruff check .` e `ruff format .`
- [ ] Verificar tipos com MyPy: `mypy .`
- [ ] Resolver warnings do MyPy sobre decorators não tipados (associar a issue #123 para rastreamento)
- [ ] Análise de segurança com Bandit: `bandit -r .`
- [ ] Verificar vulnerabilidades com Pip-audit: `pip-audit`
- [ ] Garantir anotações de tipo usando `from __future__ import annotations` em todos os módulos
- [ ] Aplicar princípios SOLID em todo o código
- [ ] Documentar APIs com FastAPI's auto-docs e garantir documentação completa no Swagger
- [ ] Atualizar pip para versão 25.3+ quando disponível (associar a issue #124 para monitoramento de releases)

## Testes e Cobertura
- [ ] Executar todos os testes: `pytest`
- [ ] Executar testes com cobertura: `pytest --cov=app --cov-report=html`
- [ ] Executar testes assíncronos: `pytest -k "async"`
- [ ] Executar testes em paralelo: `pytest -n auto`
- [ ] Executar testes de integração: `pytest -m integration`
- [ ] Implementar mais testes para aumentar cobertura (associar a issue #125 para planejamento de testes adicionais)

## Desenvolvimento Contínuo
- [ ] Executar hooks de pre-commit: `pre-commit run --all-files`
- [ ] Servir documentação com MkDocs: `mkdocs serve`
- [ ] Configurar e executar CI/CD com GitHub Actions (testes, linting, segurança em PRs)
- [ ] Revisar e atualizar dependências regularmente
- [ ] Implementar rate limiting via Redis para prevenir ataques de força bruta
- [ ] Publicar eventos para RabbitMQ para auditoria e integração
- [ ] Garantir que JWT seja usado para autenticação stateless, validando assinaturas
- [ ] Hash de senhas com bcrypt; nunca armazenar texto plano
- [ ] Escrever testes primeiro (TDD); cobrir caminhos assíncronos
- [ ] Executar suite completa de testes antes de commits/PRs
- [ ] Desenvolver Application Layer (use cases) (associar a issue #126 para expansão de lógica de negócio)
- [ ] Expandir Presentation Layer (mais endpoints) (associar a issue #127 para novos endpoints de API)
- [ ] Melhorar Integração com RabbitMQ e Redis (associar a issue #128 para otimização de mensageria e cache)

## Validação e Verificação
- [ ] Verificar que o projeto segue Clean Architecture e DDD
- [ ] Garantir uso de async/await para operações I/O
- [ ] Usar Pydantic para validação e configurações
- [ ] Log com structlog para saída estruturada
- [ ] Não hardcodar dados sensíveis; usar variáveis de ambiente para segredos
