# Dolorestec Auth - Lista de Issues para Desenvolvimento

## Issues Prioritárias (MVP Core)

### 1. Implementar Use Case de Login

**Título:** Implement login use case with password validation and token generation  
**Descrição:**  
Criar use case `app/use_cases/auth.py` com classe `LoginUseCase` que:  

- Recebe email/senha  
- Valida credenciais via adapter PostgreSQL  
- Gera tokens JWT (access + refresh)  
- Implementa rate limiting via Redis  
- Publica evento de login no RabbitMQ  
- Retorna tokens ou erro  

**Labels:** enhancement, backend, authentication  
**Assignee:** TBD  
**Milestone:** MVP Core  
**Estimativa:** 4h  

### 2. Implementar Adapter PostgreSQL para Usuários

**Título:** Create PostgreSQL adapter for user operations  
**Descrição:**  
Criar `app/infrastructure/postgres_adapter.py` com interface `IUserRepository`:  

- Métodos: get_by_email, create_user, update_user, delete_user  
- Usar asyncpg para queries assíncronas  
- Implementar connection pooling  
- Tratamento de erros de BD  
- Configuração via settings  

**Labels:** enhancement, backend, database  
**Assignee:** TBD  
**Milestone:** MVP Core  
**Estimativa:** 6h  

### 3. Implementar Adapter RabbitMQ para Eventos

**Título:** Implement RabbitMQ adapter for authentication events  
**Descrição:**  
Criar `app/infrastructure/rabbitmq_adapter.py` com interface `IEventPublisher`:  

- Publicar eventos: user_logged_in, token_revoked, password_changed  
- Usar aio-pika para comunicação assíncrona  
- Configuração de exchange/queue  
- Reconexão automática  
- Logging de eventos  

**Labels:** enhancement, backend, messaging  
**Assignee:** TBD  
**Milestone:** MVP Core  
**Estimativa:** 4h  

### 4. Criar Endpoints de Autenticação

**Título:** Create authentication API endpoints  
**Descrição:**  
Criar `app/api/v1/endpoints/auth.py` com endpoints:  

- POST /login - Login com email/senha  
- POST /refresh - Refresh access token  
- POST /validate - Validar token  
- POST /logout - Revogar tokens  
- Documentação Swagger completa com exemplos  
- Tratamento de erros HTTP apropriado  

**Labels:** enhancement, backend, api  
**Assignee:** TBD  
**Milestone:** MVP Core  
**Estimativa:** 6h  

### 5. Implementar Use Case de Validação de Token

**Título:** Implement token validation use case  
**Descrição:**  
Adicionar `ValidateTokenUseCase` em `app/use_cases/auth.py`:  

- Recebe token JWT  
- Valida assinatura e expiração  
- Verifica se token foi revogado (via Redis)  
- Retorna claims ou erro  
- Integra com rate limiting  

**Labels:** enhancement, backend, authentication  
**Assignee:** TBD  
**Milestone:** MVP Core  
**Estimativa:** 3h  

### 6. Implementar Use Case de Refresh Token

**Título:** Implement refresh token use case  
**Descrição:**  
Adicionar `RefreshTokenUseCase` em `app/use_cases/auth.py`:  

- Recebe refresh token  
- Valida refresh token  
- Gera novo par access/refresh  
- Invalida refresh token antigo  
- Publica evento de refresh  

**Labels:** enhancement, backend, authentication  
**Assignee:** TBD  
**Milestone:** MVP Core  
**Estimativa:** 3h  

## Issues Secundárias (Qualidade e Testes)

### 7. Implementar Testes Unitários

**Título:** Create comprehensive unit tests  
**Descrição:**  
Criar estrutura `tests/` com:  

- Testes para domain entities (User, Token)  
- Testes para use cases (mocks para adapters)  
- Testes para adapters (com testcontainers ou mocks)  
- Cobertura >80%  
- Testes assíncronos com pytest-asyncio  

**Labels:** testing, backend  
**Assignee:** TBD  
**Milestone:** Quality Assurance  
**Estimativa:** 8h  

### 8. Implementar Testes de Integração

**Título:** Create integration tests for auth flow  
**Descrição:**  
Testes end-to-end:  

- Login completo com BD real  
- Validação de tokens  
- Refresh token flow  
- Rate limiting  
- Usar testcontainers para PostgreSQL/Redis/RabbitMQ  
- Testes de API com httpx  

**Labels:** testing, backend, integration  
**Assignee:** TBD  
**Milestone:** Quality Assurance  
**Estimativa:** 6h  

### 9. Implementar Rate Limiting

**Título:** Add rate limiting to authentication endpoints  
**Descrição:**  
Implementar middleware ou decorator:  

- Limite por IP/usuário  
- Configurável via settings  
- Armazenamento em Redis  
- Headers de rate limit (X-RateLimit-*)  
- Logging de violações  

**Labels:** enhancement, backend, security  
**Assignee:** TBD  
**Milestone:** Security Features  
**Estimativa:** 4h  

### 10. Configurar Documentação MkDocs

**Título:** Set up MkDocs documentation  
**Descrição:**  

- Instalar e configurar MkDocs  
- Criar estrutura de docs: architecture, api, deployment  
- Integrar com GitHub Pages  
- Documentar APIs com exemplos  
- Adicionar diagramas (Mermaid)  

**Labels:** documentation, devops  
**Assignee:** TBD  
**Milestone:** Documentation  
**Estimativa:** 4h  

### 11. Adicionar Logs Estruturados

**Título:** Implement structured logging throughout the service  
**Descrição:**  

- Configurar structlog em todos os módulos  
- Logs para: auth attempts, token operations, errors  
- Níveis apropriados (INFO, WARNING, ERROR)  
- Contexto: user_id, request_id, ip  
- Formato JSON para produção  

**Labels:** enhancement, backend, observability  
**Assignee:** TBD  
**Milestone:** Observability  
**Estimativa:** 3h  

### 12. Implementar Health Checks Avançados

**Título:** Add comprehensive health checks  
**Descrição:**  
Expandir endpoint /health:  

- Verificar conectividade PostgreSQL  
- Verificar Redis  
- Verificar RabbitMQ  
- Métricas básicas (uptime, requests)  
- Status detalhado por componente  

**Labels:** enhancement, backend, monitoring  
**Assignee:** TBD  
**Milestone:** Observability  
**Estimativa:** 2h  

## Issues Futuras (Features Avançadas)

### 13. Implementar OAuth2 Client Credentials

**Título:** Add OAuth2 client credentials flow  
**Descrição:**  

- Suporte a client_id/client_secret  
- Validação de clients no BD  
- Geração de access tokens para APIs  
- Endpoint /token para client credentials  

**Labels:** enhancement, backend, oauth2  
**Assignee:** TBD  
**Milestone:** Advanced Features  
**Estimativa:** 5h  

### 14. Implementar Revogação de Tokens

**Título:** Add token revocation functionality  
**Descrição:**  

- Endpoint para revogar tokens específicos  
- Revogação em lote (logout all devices)  
- Armazenamento de tokens revogados em Redis  
- Validação contra lista negra  

**Labels:** enhancement, backend, security  
**Assignee:** TBD  
**Milestone:** Advanced Features  
**Estimativa:** 4h  

### 15. Adicionar Métricas e Monitoramento

**Título:** Add metrics and monitoring  
**Descrição:**  

- Integração com Prometheus  
- Métricas: logins/s, tokens issued, errors  
- Dashboards Grafana  
- Alertas para falhas de auth  

**Labels:** enhancement, devops, monitoring  
**Assignee:** TBD  
**Milestone:** Production Ready  
**Estimativa:** 6h  

## Critérios de Aceitação Gerais

- Código segue Clean Architecture e SOLID
- Testes unitários com cobertura >80%
- Documentação Swagger completa
- Logs estruturados
- Tratamento adequado de erros
- Performance: <100ms para auth operations
- Segurança: JWT seguro, rate limiting, input validation

## Dependências entre Issues

- 2 (PostgreSQL) deve ser implementado antes de 1, 5, 6
- 3 (RabbitMQ) deve ser implementado antes de 1, 5, 6  
- 1, 5, 6 devem ser implementados antes de 4
- 7 deve ser implementado paralelamente ao desenvolvimento
- 8 depende de 1, 4, 5, 6
- 9 pode ser implementado após 4
- 10 pode ser implementado a qualquer momento
- 11 pode ser implementado incrementalmente</content>
<parameter name="filePath">/home/lucas/dolorestec/dlrs-auth/issues.md
