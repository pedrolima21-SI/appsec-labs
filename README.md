# AppSec Labs

Repositório de estudos sobre segurança de aplicações, com exercícios defensivos em cenários fictícios, código próprio e ambientes explicitamente autorizados.

> **Status:** Em desenvolvimento. Os materiais são educacionais. Nenhum exercício autoriza testar sistemas de terceiros sem permissão explícita.

## Primeiro material: controle de acesso

O laboratório [`01 — Revisão de controle de acesso`](labs/01-access-control-review/) propõe uma matriz de permissões para uma aplicação fictícia de relatórios e, nesta etapa, também inclui uma demonstração local e reproduzível das regras de autorização.

- [Matriz de acesso preenchida](labs/01-access-control-review/access-matrix.md)
- [Plano de casos de teste](labs/01-access-control-review/test-plan.md)
- [Conclusões e limitações](labs/01-access-control-review/notes.md)
- [Demonstração local de autorização](labs/01-access-control-review/access_control_demo.py)

## Como executar a demonstração local

```bash
python labs/01-access-control-review/access_control_demo.py
```

A execução imprime os resultados esperados para cenários permitidos e negados, servindo como base didática para revisão de autorização e menor privilégio.

## Principios

- Respeitar escopo e autorização explícita.
- Preferir revisão preventiva e ambientes locais.
- Utilizar dados fictícios e sanitizados.
- Diferenciar fatos observados, hipóteses e resultados esperados.
- Não publicar credenciais, segredos ou dados pessoais.

## Licença

MIT. Consulte [`LICENSE`](LICENSE).

## Contato

[LinkedIn](https://www.linkedin.com/in/pedro-lima-sec) · [E-mail](mailto:pedrovitor.lima211@gmail.com)
