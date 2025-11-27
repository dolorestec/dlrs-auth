# Dolorestec Auth - Plano de Desenvolvimento

## Visão Geral

Microserviço de autenticação seguro com JWT, seguindo Clean Architecture e DDD.

## Fases de Desenvolvimento

### 1. Análise e Planejamento

- [x] Definir requisitos de autenticação
- [x] Modelar domínio DDD
- [x] Arquitetura Clean Architecture
- [ ] **Integração GitHub Copilot**: Configurar instruções personalizadas para otimizar sugestões de código e agentes

### 2. Design e Configuração

- [x] Ambiente UV e dependências
- [x] Estrutura de projeto
- [x] Configuração BD/Cache
- [ ] **Prompts Copilot**: Criar prompts reutilizáveis para tarefas comuns (ex.: criar entidade, use case)

### 3. Implementação e Desenvolvimento

- [x] Entidades domínio (User, Token)
- [ ] Use cases auth
- [ ] Infraestrutura JWT/Redis/RabbitMQ
- [ ] **Agentes Copilot**: Usar coding agent para gerar PRs iniciais, revisar código

### 4. Testes e Qualidade

- [ ] Testes pytest (unitários, integração)
- [ ] Validação mypy/ruff
- [ ] **Code Review Copilot**: Habilitar revisões automáticas em PRs

### 5. Documentação e Deployment

- [ ] Docs MkDocs
- [ ] CI/CD
- [ ] Monitoramento
- [ ] **Customização Copilot**: Ajustar instruções baseadas em feedback do desenvolvimento

## Integração GitHub Copilot

### Instruções Personalizadas

- Arquivo `.github/copilot-instructions.md` criado com overview, arquitetura, comandos build/test, dependências
- Foca em padrões: async/await, Clean Architecture, JWT stateless, testes TDD

### Uso de Agentes

- Coding Agent: Para gerar código boilerplate (entidades, adapters)
- Code Review: Para validações de segurança e padrões

### Prompts e Context

- Fornecer contexto via chat: anexar arquivos README, pyproject.toml
- Usar `/prompt` para tarefas repetitivas

### MCP Servers

- Memory: Para armazenar conhecimento do projeto
- Sequential Thinking: Para planejamento complexo
- Melhorias: Adicionar server para busca semântica no código, ou integração com docs externas

## Melhorias Sugeridas para PLAN.md

- Adicionar seção dedicada a IA/Assistentes (Copilot, agentes)
- Incluir checklist de configuração Copilot
- Documentar prompts customizados
- Planejar testes de integração com Copilot (ex.: validar sugestões seguem padrões)
- Monitorar eficácia: tempo economizado, qualidade de código

## Extensões VS Code Recomendadas

- GitHub Copilot: Para sugestões inline
- GitHub Copilot Chat: Para consultas contextuais
- Python: Para suporte linguagem
- Ruff: Para linting rápido
- Pylance: Para intellisense
- Melhorias MCP: Adicionar servers para GitHub issues, ou análise de segurança

## Próximos Passos

1. Implementar entidades domínio
2. Configurar infraestrutura
3. Testar integração Copilot em desenvolvimento
