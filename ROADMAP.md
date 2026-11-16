# Roadmap de estudos — AppSec Labs

Plano inicial de quatro semanas. Ajuste o ritmo conforme seu tempo e registre o que foi realmente concluído. Os exercícios são defensivos e devem usar aplicações próprias, código didático ou laboratórios autorizados.

## Semana 1 — Fundamentos e controle de acesso

**Estudar:** autenticação versus autorização, papéis, menor privilégio e validação de permissões no servidor.

**Prática:** revisar a matriz de acesso de uma aplicação local simples; conferir se cada ação tem um papel e uma regra documentados.

**Entrega:** matriz de acesso preenchida e notas do exercício [`labs/01-access-control-review/`](labs/01-access-control-review/).

## Semana 2 — Validação de dados e erros

**Estudar:** validação no servidor, codificação contextual, mensagens de erro seguras e tratamento consistente de entradas inválidas.

**Prática:** revisar código próprio ou um exemplo didático, localizar validações ausentes e propor correções. Não testar serviços públicos.

**Entrega:** checklist com observações, correções propostas e casos de teste benignos.

## Semana 3 — Sessões e proteção de dados

**Estudar:** ciclo de vida de sessão, proteção de cookies, armazenamento seguro de segredos e minimização de dados.

**Prática:** revisar configurações de uma aplicação local e escrever uma lista de melhorias, sem utilizar contas ou dados reais de terceiros.

**Entrega:** checklist de revisão e notas sobre limitações do ambiente.

## Semana 4 — Modelagem de ameaças e comunicação

**Estudar:** ativos, limites de confiança, casos de uso, ameaças e mitigação; comunicação técnica baseada em evidências.

**Prática:** modelar uma aplicação fictícia ou própria e priorizar melhorias preventivas.

**Entrega:** diagrama simples de fluxo de dados e um registro de achado sanitizado usando o template de [`reporting-templates`](https://github.com/pedrolima21-SI/reporting-templates).

## Critérios para considerar um módulo concluído

- Objetivo, escopo e ambiente estão registrados.
- A atividade foi feita em contexto local ou autorizado.
- Há uma conclusão sustentada por observações, sem dados sensíveis.
- A correção ou melhoria recomendada está descrita.
- Limitações e próximos passos estão explícitos.

## Próximos módulos possíveis

Após concluir a base, adicionar exercícios de revisão de dependências, configuração segura, logging sem dados sensíveis e práticas de desenvolvimento seguro. Cada novo módulo deve priorizar prevenção, correção e validação controlada.
