# 01 — Revisão de controle de acesso

## Objetivo

Praticar a documentação de regras de acesso e identificar lacunas de especificação em um cenário fictício. O exercício é de revisão e desenho defensivo; não requer testar um sistema real.

## Cenário fictício

Uma aplicação interna possui três papéis: `leitor`, `editor` e `administrador`. Os recursos são relatórios, rascunhos e configurações da aplicação. Antes de implementar ou revisar o controle, a equipe deve definir explicitamente quais ações cada papel pode executar.

## Tarefa

1. Preencha a matriz em [`access-matrix.md`](access-matrix.md) com permissões coerentes com o princípio do menor privilégio.
2. Para cada ação, identifique o papel autorizado e o componente responsável por aplicar a regra.
3. Anote decisões ainda ambíguas como perguntas para a equipe, em vez de assumir comportamento.
4. Proponha testes unitários locais que confirmem casos permitidos e negados, sem usar serviços externos.
5. Registre riscos e recomendações de forma sanitizada.

## Perguntas para revisão

- Cada ação tem uma regra de autorização explícita?
- A regra é aplicada no servidor, além de qualquer controle visual na interface?
- O padrão para permissões não especificadas é negar acesso?
- As verificações são consistentes em todos os caminhos da mesma ação?
- A aplicação evita revelar dados de recursos que o usuário não pode acessar?

## Entrega esperada

Uma matriz preenchida, decisões pendentes identificadas, casos de teste locais descritos e uma recomendação curta. Não inclua código ou dados de sistemas reais de terceiros.

## Critério de conclusão

O exercício está concluído quando as permissões e decisões estão documentadas, as ambiguidades estão destacadas e a abordagem de validação local está descrita.
