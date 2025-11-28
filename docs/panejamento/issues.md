# Issues para Finalizar o MVP do Projeto Dolorestec Auth

Este documento lista todas as issues necessárias para completar o Minimum Viable Product (MVP) do microserviço de autenticação Dolorestec Auth, baseado nos arquivos de gestão de projeto.

## Issues do MVP Core (Essenciais)

### 1. Implementar Use Case de Login

- **Descrição**: Criar use case de login com validação de credenciais, geração de tokens JWT, rate limiting e publicação de eventos.
- **Labels**: enhancement, backend, authentication
- **Milestone**: MVP Core
- **Estimativa**: 4h

### 2. Implementar Adapter PostgreSQL para Usuários

- **Descrição**: Criar adapter para operações de usuário no PostgreSQL usando asyncpg.
- **Labels**: enhancement, backend, database
- **Milestone**: MVP Core
- **Estimativa**: 6h

### 3. Implementar Adapter RabbitMQ para Eventos

- **Descrição**: Criar adapter para publicar eventos de autenticação via RabbitMQ.
- **Labels**: enhancement, backend, messaging
- **Milestone**: MVP Core
- **Estimativa**: 4h

### 4. Criar Endpoints de Autenticação

- **Descrição**: Implementar endpoints REST para login, refresh, validate e logout.
- **Labels**: enhancement, backend, api
- **Milestone**: MVP Core
- **Estimativa**: 6h

### 5. Implementar Use Case de Validação de Token

- **Descrição**: Criar use case para validar tokens JWT.
- **Labels**: enhancement, backend, authentication
- **Milestone**: MVP Core
- **Estimativa**: 3h

### 6. Implementar Use Case de Refresh Token

- **Descrição**: Criar use case para renovar tokens de acesso.
- **Labels**: enhancement, backend, authentication
- **Milestone**: MVP Core
- **Estimativa**: 3h

## Issues de Qualidade (Paralelas ao MVP)

### 7. Implementar Testes Unitários

- **Descrição**: Criar testes unitários abrangentes com cobertura >80%.
- **Labels**: testing, backend
- **Milestone**: Quality Assurance
- **Estimativa**: 8h

### 8. Implementar Testes de Integração

- **Descrição**: Criar testes end-to-end para fluxos de autenticação.
- **Labels**: testing, backend, integration
- **Milestone**: Quality Assurance
- **Estimativa**: 6h

## Issues Pós-MVP (Para Produção)

### 9. Implementar Rate Limiting

- **Descrição**: Adicionar rate limiting aos endpoints de autenticação.
- **Labels**: enhancement, backend, security
- **Milestone**: Security Features
- **Estimativa**: 4h

### 10. Configurar Documentação MkDocs

- **Descrição**: Configurar documentação técnica com MkDocs.
- **Labels**: documentation, devops
- **Milestone**: Documentation
- **Estimativa**: 4h

### 11. Adicionar Logs Estruturados

- **Descrição**: Implementar logging estruturado com structlog.
- **Labels**: enhancement, backend, observability
- **Milestone**: Observability
- **Estimativa**: 3h

### 12. Implementar Health Checks Avançados

- **Descrição**: Expandir health checks para incluir verificações de conectividade.
- **Labels**: enhancement, backend, monitoring
- **Milestone**: Observability
- **Estimativa**: 2h

### 13. Implementar OAuth2 Client Credentials

- **Descrição**: Adicionar suporte ao fluxo OAuth2 client credentials.
- **Labels**: enhancement, backend, oauth2
- **Milestone**: Advanced Features
- **Estimativa**: 5h

### 14. Implementar Revogação de Tokens

- **Descrição**: Adicionar funcionalidade para revogar tokens.
- **Labels**: enhancement, backend, security
- **Milestone**: Advanced Features
- **Estimativa**: 4h

### 15. Adicionar Métricas e Monitoramento

- **Descrição**: Integrar com Prometheus para métricas e alertas.
- **Labels**: enhancement, devops, monitoring
- **Milestone**: Production Ready
- **Estimativa**: 6h

## Dependências Críticas

- Issues 2 e 3 devem ser implementadas antes das 1, 5, 6
- Issues 1, 5, 6 devem ser implementadas antes da 4
- Issue 4 deve ser implementada antes da 9
- Issues 7 e 8 podem ser desenvolvidas paralelamente

## Critérios de Aceitação do MVP

- Todos os endpoints de autenticação funcionais
- Testes unitários com cobertura >80%
- Documentação Swagger completa
- Logs estruturados implementados
- Rate limiting básico ativo
- Performance <100ms para operações de auth
- Segurança: JWT válido, validação de input, rate limiting
