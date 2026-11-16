# Matriz de acesso — cenário fictício

Esta matriz é uma proposta educacional para a aplicação fictícia descrita no [README do exercício](README.md). `Próprio` indica que a propriedade do rascunho também precisa ser verificada no servidor. As regras não foram validadas em uma aplicação real.

| Ação | Leitor | Editor | Administrador | Regra/observação |
| --- | --- | --- | --- | --- |
| Consultar relatório publicado | Permitido* | Permitido* | Permitido | *Somente conteúdo publicado e dentro do escopo de acesso definido para o usuário. |
| Criar rascunho | Negado | Permitido | Permitido | Registrar o autor no servidor; não confiar em identificador enviado pelo cliente. |
| Editar próprio rascunho | Negado | Permitido (próprio) | Permitido | Verificar papel e propriedade em cada operação. |
| Editar rascunho de outra pessoa | Negado | Negado (proposta) | Permitido | Acesso administrativo deve ter justificativa e registro apropriado. |
| Publicar relatório | Negado | Negado (provisório) | Permitido | Proposta conservadora até decisão explícita sobre aprovação por editor. |
| Gerenciar papéis | Negado | Negado | Permitido | Restringir a administradores; registrar alterações relevantes. |
| Alterar configurações globais | Negado | Negado | Permitido | Restringir a administradores; registrar alterações relevantes. |
| Ação protegida com papel ausente/desconhecido | Negado | Negado | Negado | Negar por padrão. |

## Decisões de negócio pendentes

- [ ] Confirmar se editores podem editar rascunhos alheios; proposta atual: não.
- [ ] Confirmar se editores podem publicar após aprovação; proposta atual: somente administradores publicam.
- [ ] Definir como alterações ou revogações de papel afetam sessões ativas.
- [ ] Definir quais eventos precisam de auditoria, acesso aos registros e período de retenção.
- [ ] Definir escopo de leitura dos relatórios publicados (por exemplo, organização ou equipe).

## Resumo da decisão didática

A matriz favorece menor privilégio: papéis sem permissão explícita recebem negação; editores operam seus próprios rascunhos; funções administrativas ficam restritas ao papel administrador. A política de publicação é provisória e deve ser decidida pelos responsáveis do produto.
