# Padrões de Desenvolvimento

Este documento descreve os padrões arquiteturais, de código e de projeto adotados no microserviço Dolorestec Auth.

## Arquitetura

- **Clean Architecture**: Separação clara entre camadas (Presentation, Application, Domain, Infrastructure) para facilitar testes e manutenção.
- **Domain-Driven Design (DDD)**: Modelagem focada no domínio de autenticação, com bounded contexts.
- **SOLID Principles**: Princípios para design orientado a objetos: Single Responsibility, Open-Closed, Liskov Substitution, Interface Segregation, Dependency Inversion.
- **Dependency Injection**: Injeção de dependências para desacoplar componentes.

## Linguagem e Framework

- **Python 3.14+**: Suporte nativo a async.
- **FastAPI**: Framework para APIs REST/async com Pydantic.
- **Async Programming**: Uso de async/await para operações I/O não bloqueantes.

## Segurança

- **JWT Authentication**: Autenticação stateless baseada em tokens JWT seguros.
- **Password Hashing**: Uso de bcrypt para armazenamento seguro de credenciais.
- **Rate Limiting**: Controle de tentativas via cache Redis.

## Qualidade de Código

- **Type Annotations**: Sempre usar `from __future__ import annotations` para evitar dependências em runtime.
- **Linting**: Ruff para linting e formatting.
- **Testing**: Pytest com suporte a async, cobertura >80%.
- **Pre-commit Hooks**: Validação antes de commits.

## Padrões de Design

- **Strategy**: Para diferentes algoritmos de autenticação.
- **Chain of Responsibility**: Para validação em cadeia.
- **Singleton**: Para configurações globais e conexões compartilhadas.

## Integração

- **Event-Driven**: Publicação de eventos via RabbitMQ para auditoria.
- **Caching**: Redis para sessões e rate limiting.
