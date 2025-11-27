# Padrões de Segurança

Este documento descreve os padrões de segurança adotados no microserviço Dolorestec Auth.

## Autenticação

- **JWT Tokens**: Autenticação stateless com tokens auto-contidos, validados por assinatura.
- **Refresh Tokens**: Suporte a refresh tokens para renovação de acesso sem re-autenticação.
- **Password Grant**: Fluxo OAuth2 para login com username/password.

## Hashing e Armazenamento

- **Bcrypt**: Hashing de senhas com bcrypt para resistência a ataques.
- **Nunca Plain Text**: Senhas nunca armazenadas em texto plano.

## Proteção contra Ataques

- **Rate Limiting**: Controle de tentativas de login via cache Redis para prevenir brute force.
- **Validação de Entrada**: Validação rigorosa de inputs com Pydantic.
- **Logs de Segurança**: Logs estruturados para tentativas suspeitas.

## Comunicação Segura

- **HTTPS**: Uso obrigatório de HTTPS em produção.
- **Eventos Seguros**: Publicação de eventos de auditoria via RabbitMQ.

## Gestão de Secrets

- **Variáveis de Ambiente**: Secrets armazenados em variáveis de ambiente, não no código.
- **Configuração Segura**: Uso de Pydantic Settings para configuração.

## Monitoramento

- **Auditoria**: Registro de logins, logouts e invalidações.
- **Alertas**: Notificação de anomalias de segurança.
