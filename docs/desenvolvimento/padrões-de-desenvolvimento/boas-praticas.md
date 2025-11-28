# Boas Práticas de Desenvolvimento

Este documento descreve as boas práticas adotadas no projeto Dolorestec Auth para garantir qualidade, segurança e manutenibilidade do código.

## Boas Práticas de Código

- Sempre use async/await para operações I/O.
- Use type annotations com `from __future__ import annotations`.
- Não armazene senhas em plain text; sempre hash com bcrypt.
- Use variáveis de ambiente para secrets, não hardcode.
- Siga PEP 8 para estilo de código Python.
- Mantenha funções pequenas e com responsabilidade única.

## Boas Práticas de Arquitetura

- Mantenha a separação de camadas: Domain puro, Infrastructure injetada.
- Use Dependency Injection para facilitar testes.
- Implemente validação no domínio, não na apresentação.
- Publique eventos para integração assíncrona.

## Boas Práticas de Testes

- Escreva testes primeiro (TDD).
- Cubra casos async e edge cases.
- Use fixtures para setup reutilizável.
- Mantenha cobertura >80%.

## Boas Práticas de Segurança

- Valide JWT signatures, não confie em estado.
- Implemente rate limiting para prevenir brute force.
- Log eventos de segurança estruturadamente.
- Use HTTPS em produção.

## Boas Práticas de Qualidade

- Execute linting e formatting antes de commits.
- Use pre-commit hooks para validação.
- Documente APIs com exemplos e descrições detalhadas.
- Mantenha dependências atualizadas e auditadas.
