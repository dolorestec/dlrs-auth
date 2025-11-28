---
agent: agent
---

# Análise de Conformidade com Padrões de Desenvolvimento

## Tarefa Geral
Realize uma análise abrangente do código do projeto Dolorestec Auth para verificar a conformidade com os padrões estabelecidos de arquitetura, código, segurança e qualidade. Identifique desvios, sugira correções e gere um relatório detalhado.

## Requisitos Específicos
- Leia toda a documentação de padrões localizada em `docs/desenvolvimento/padrões-de-desenvolvimento/` e `docs/segurança/padrões-de-segurança/`
- Analise o código fonte em `app/` para conformidade arquitetural (Clean Architecture, DDD, SOLID)
- Verifique uso correto de Python 3.14+, async/await, type annotations
- Valide implementação de segurança (JWT, bcrypt, rate limiting)
- Avalie qualidade (testes >80%, linting, documentação)
- Examine integrações (PostgreSQL, Redis, RabbitMQ)

## Passos de Análise (Divididos para Clareza)
1. **Leitura da Documentação**: Acesse e compreenda todos os arquivos de padrões
2. **Análise Arquitetural**: Verifique camadas (Presentation, Application, Domain, Infrastructure)
3. **Análise de Código**: Confirme padrões Python, imports, estrutura
4. **Análise de Segurança**: Valide autenticação, hashing, proteção contra ataques
5. **Análise de Testes**: Verifique conformidade com boas práticas de testes (TDD, pytest, cobertura, mocking)
6. **Análise de Qualidade**: Testes, linting, cobertura
7. **Análise de Integração**: Adaptadores e conexões
8. **Relatório**: Liste conformidades, desvios e recomendações

## Exemplos de Verificação
- **Arquitetura**: Código em `app/domain/` deve ser puro, sem dependências externas
- **Segurança**: Todas as senhas devem usar `bcrypt` via `passlib`
- **Qualidade**: Funções devem ter type hints e docstrings
- **Testes**: Use pytest com nomes descritivos, mocks para isolamento, cobertura >80%

## Constraints
- Não modifique o código; apenas analise e reporte
- Use ferramentas de busca para localizar arquivos relevantes
- Foque em padrões documentados, ignore convenções não especificadas
- Leia as documentações de referência se necessário, para tirar dúvidas.

## Critérios de Sucesso
- Relatório completo com seções por categoria
- Identificação de pelo menos 80% dos possíveis desvios
- Sugestões acionáveis para correções
- Tempo de análise < 30 minutos

## Iteração
Se encontrar ambiguidades, refine a análise focando em áreas críticas primeiro.
