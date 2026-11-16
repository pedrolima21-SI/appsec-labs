# Registro de estudo — controle de acesso

## Contexto e escopo

- Cenário: aplicação fictícia de relatórios.
- Objetivo: propor regras de acesso por papel e explicitar decisões ambíguas.
- Método: exercício de especificação documental.
- Limites: nenhuma aplicação real ou laboratório executável foi testado.

## Papéis e ações considerados

- Papéis: leitor, editor e administrador.
- Ações: consultar relatórios publicados, criar e editar rascunhos, publicar relatórios, gerenciar papéis e alterar configurações globais.
- Condição adicional: editor só pode editar rascunho próprio, conforme proposta.

## Observações da análise documental

| Observação | Base | Implicação no cenário |
| --- | --- | --- |
| Consulta, edição e administração são ações distintas | Matriz proposta | Não conceder permissões por conveniência ou apenas por visibilidade na interface. |
| Edição depende da propriedade do rascunho | Regra proposta | Verificar papel e propriedade no servidor. |
| Política de publicação não foi definida pelo cenário | Decisão pendente | Manter negação para editor até que a regra seja aprovada. |
| Papel ausente ou desconhecido precisa de comportamento explícito | Princípio de negação por padrão | Negar ação protegida. |

## Conclusão

Para o cenário didático, a proposta segue menor privilégio e nega por padrão: leitores consultam conteúdo publicado dentro do escopo; editores criam e editam apenas os próprios rascunhos; administradores executam operações administrativas. A publicação por editor permanece negada provisoriamente até decisão de negócio. Estas são regras propostas, não resultados observados em software.

## Recomendações

- Aplicar autorização no servidor em cada ação protegida.
- Verificar propriedade do recurso separadamente do papel.
- Definir e documentar escopo de leitura e política de publicação.
- Criar testes locais para acessos permitidos e negados.
- Registrar alterações administrativas sem coletar segredos ou dados desnecessários.

## Próximos passos

1. Confirmar as decisões pendentes do cenário.
2. Se desejado, implementar uma aplicação didática isolada.
3. Executar os casos do [plano de teste](test-plan.md) e registrar os resultados reais em nova revisão.

## Limitações

Cenário fictício; sem implementação, teste executado, achado real ou avaliação de risco de produto. Os resultados esperados não devem ser apresentados como evidência de validação.
