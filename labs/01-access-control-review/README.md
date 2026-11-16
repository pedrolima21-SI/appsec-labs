# 01 — Revisão de controle de acesso

## Objetivo

Praticar a definição e revisão de regras de acesso em uma aplicação fictícia, aplicando menor privilégio, negação por padrão e validação de autorização no servidor.

## Escopo e método

Exercício de especificação documental, agora complementado por uma demonstração local em Python. Não há aplicação real, serviço externo, conta real ou teste técnico executado. A matriz, o plano de teste e o simulador são propostas para discussão e precisam ser adaptados e aprovados antes de orientar um sistema real.

## Cenário fictício

Uma aplicação interna permite consultar relatórios publicados, criar e editar rascunhos, publicar relatórios e administrar papéis e configurações. Há três papéis: `leitor`, `editor` e `administrador`. A propriedade do rascunho é uma condição adicional: ser editor não concede acesso automático aos rascunhos de outras pessoas.

## Entregáveis

1. [Matriz de acesso](access-matrix.md) preenchida com uma proposta conservadora.
2. [Plano de casos de teste](test-plan.md) para validação futura em uma aplicação local.
3. [Registro de estudo](notes.md) com conclusão, decisões pendentes e limitações.
4. [Simulador local](access_control_demo.py) para demonstrar decisões de autorização em Python.

## Como executar o simulador

```bash
python access_control_demo.py
```

A saída mostra resultados esperados para cenários permitidos e negados, utilizando apenas dados fictícios.

## Princípios da proposta

- Negar ações protegidas quando não houver regra ou papel reconhecido.
- Validar a autorização no servidor em cada operação; controles de interface não substituem autorização.
- Verificar propriedade do recurso para editar rascunhos.
- Registrar ações administrativas de forma proporcional, sem registrar segredos.
- Evitar revelar conteúdo de recursos não autorizados.

## Conclusão

A proposta separa consulta, edição e administração; limita a edição de rascunhos ao autor e reserva publicação e alterações globais ao administrador até que os responsáveis definam outra política. As decisões são ilustrativas, não requisitos aprovados para um produto real.

## Limitações e próximos passos

- Cenário e permissões inteiramente fictícios.
- Não há aplicação real, execução de teste em ambiente externo ou evidência de vulnerabilidade.
- Confirmar as decisões de negócio antes de qualquer implementação real.
- Se o estudo evoluir para código, criar uma aplicação didática local e validar os casos do simulador com testes automatizados.
