# Boas Práticas de Testes

Este documento descreve as boas práticas de testes adotadas no projeto Dolorestec Auth.

## Princípios Gerais

- **TDD (Test-Driven Development)**: Escreva testes antes do código
- **Testes Independentes**: Cada teste roda isoladamente, sem dependências
- **Testes Rápidos**: Evite testes pesados; mantenha <100ms por teste
- **Nomes Descritivos**: Funções como `test_login_with_valid_credentials`

## Estrutura e Organização

- Organize testes por módulo (ex.: `tests/test_auth.py`)
- Use fixtures para setup comum (ex.: usuário mockado)
- Agrupe testes relacionados em classes

## Mocking e Isolamento

- Use mocks para dependências externas (BD, APIs)
- Evite mocks excessivos; prefira testes de integração quando possível
- Valide chamadas de mock com `assert_called_with`

## Cobertura e Qualidade

- Aime por cobertura alta, mas priorize testes significativos
- Teste casos happy path, edge cases e erros
- Inclua testes de regressão para bugs corrigidos

## Testes Assíncronos

- Marque funções async com `@pytest.mark.asyncio`
- Use `await` em asserções
- Teste timeouts e cancelamentos

## Integração Contínua

- Execute testes em cada PR
- Bloqueie merge se cobertura <80% ou testes falhando
- Use ferramentas como testcontainers para ambientes reais

## Debugging

- Use `--pdb` para debug interativo
- Logue informações relevantes em testes
- Evite prints; use asserções claras

## Manutenção

- Refatore testes junto com código
- Remova testes obsoletos
- Documente testes complexos com comentários
