# Plano de casos de teste — controle de acesso

Casos propostos para uma futura implementação didática **local**. São resultados esperados, não testes executados nem evidência de comportamento de qualquer sistema.

| Caso | Papel e condição | Ação | Resultado esperado |
| --- | --- | --- | --- |
| T01 | Leitor autenticado | Consultar relatório publicado dentro do escopo | Permitido |
| T02 | Leitor autenticado | Criar rascunho | Negado |
| T03 | Editor autenticado | Criar rascunho | Permitido; autoria definida pelo servidor |
| T04 | Editor, autor do rascunho | Editar próprio rascunho | Permitido |
| T05 | Editor, não autor do rascunho | Editar rascunho alheio | Negado |
| T06 | Editor autenticado | Publicar relatório | Negado enquanto a política provisória não for alterada |
| T07 | Administrador autenticado | Gerenciar papéis | Permitido; evento administrativo registrado conforme política |
| T08 | Papel ausente ou desconhecido | Executar ação protegida | Negado por padrão |
| T09 | Usuário sem escopo de leitura | Consultar relatório fora do escopo | Negado sem revelar conteúdo protegido |

## Orientações de validação futura

- Implementar testes unitários ou de integração em aplicação local e isolada.
- Preparar usuários e recursos fictícios; não utilizar contas ou dados reais.
- Confirmar que autorização é aplicada no servidor para cada operação relevante.
- Verificar caminhos permitidos e negados, incluindo propriedade do recurso.
- Registrar resultados reais somente depois de executar os testes; não converter esta tabela em afirmação de teste concluído.
