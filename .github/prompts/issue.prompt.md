---
agent: agent
---

# Workflow Automatizado de Desenvolvimento por Issue

## Tarefa Geral
Automatize o processo completo de desenvolvimento para uma issue do GitHub, desde a seleção até o pull request, seguindo boas práticas de Git e desenvolvimento colaborativo.

## Requisitos Específicos
- Buscar lista de issues abertas no repositório dlrs-auth
- Selecionar a issue mais antiga (por data de criação)
- Atualizar repositório local (pull develop)
- Criar branch nomeada por tipo (feature/bugfix)/DLRS-{numero}
- Analisar descrição da issue para entender requisitos
- Implementar solução conforme padrões do projeto
- Commitar mudanças com mensagem descritiva
- Criar pull request para develop
- Retornar para branch develop

## Passos de Execução (Divididos para Clareza)
1. **Buscar Issues**: Listar issues abertas via GitHub API
2. **Filtrar Issue**: Selecionar a mais antiga por createdAt
3. **Atualizar Repositório**: git pull origin develop
4. **Criar Branch**: git checkout -b {tipo}/DLRS-{numero}
5. **Analisar Tarefa**: Ler título, descrição, labels da issue
6. **Executar Implementação**: Desenvolver código conforme requisitos
7. **Commitar**: git add . && git commit -m "feat/bug: descrição"
8. **Criar PR**: gh pr create --title "..." --body "..." --base develop
9. **Checkout Develop**: git checkout develop

## Exemplos de Verificação
- **Branch Naming**: feature/DLRS-1 para nova funcionalidade
- **Commit Message**: "feat: implement login use case" ou "fix: correct token validation"
- **PR Title**: "Implement login use case [DLRS-1]"

## Constraints
- Só trabalhar em issues abertas e não assigned
- Seguir padrões de commit (Conventional Commits)
- Não mergear PR; apenas criar
- Usar labels da issue para determinar tipo (enhancement=feature, bug=bugfix)
- Leia as documentações de referência se necessário, para tirar dúvidas.

## Critérios de Sucesso
- Branch criada corretamente
- Código implementado conforme issue
- PR criado com descrição completa
- Repositório atualizado e na develop

## Iteração
Se issue complexa, dividir em commits menores; se simples, implementar tudo de uma vez.
