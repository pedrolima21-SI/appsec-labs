# API Security Lab

Laboratório local, didático e fictício para estudar autenticação, autorização e controle de acesso em APIs REST.

## Objetivo

Demonstrar, em ambiente controlado, as diferenças entre:
- autenticação por token
- autorização por papel
- autorização por propriedade do recurso
- autorização por escopo
- reprodução intencional de BOLA/IDOR em modo vulnerável
- correção efetiva em modo seguro

Os dados e as credenciais são sintéticos e não representam usuários, organizações ou sistemas reais.

## Arquitetura

- Python 3.12+
- FastAPI
- SQLite
- SQLAlchemy
- Pytest + HTTPX
- Docker Compose

Estrutura principal:

```text
labs/02-api-security/
├── app/
│   ├── auth.py
│   ├── config.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── policies.py
│   ├── schemas.py
│   └── vulnerable.py
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_secure_reports.py
│   └── test_vulnerable_demo.py
├── README.md
├── docker-compose.yml
├── requirements.txt
└── data/
```

## Configuração

Defina um segredo forte para JWT antes de iniciar a aplicação:

```bash
export JWT_SECRET="$(python -c 'import secrets; print(secrets.token_urlsafe(48))')"
```

Também é possível usar `APP_DB_PATH` para alterar o caminho do SQLite.

## Usuários fictícios de demonstração

| Usuário | Senha | Papel | Escopo |
| --- | --- | --- | --- |
| alice | alice12345 | reader | team-a |
| bob | bob12345 | editor | team-a |
| carol | carol12345 | editor | team-b |
| admin | admin12345 | administrator | org-global |
| inactive | inactive12345 | reader | team-a |

## Endpoints

- `POST /auth/register`
- `POST /auth/token`
- `GET /auth/me`
- `GET /api/reports`
- `POST /api/reports`
- `GET /api/reports/{report_id}`
- `PATCH /api/reports/{report_id}`
- `POST /api/reports/{report_id}/publish`

## Matriz de permissões

- reader: lê apenas relatórios publicados do mesmo escopo; não cria nem edita.
- editor: cria rascunhos no próprio escopo; edita somente os próprios rascunhos.
- administrator: publica relatórios em rascunho e tem acesso administrativo explícito.
- ações fora do conjunto permitido são negadas por padrão.

## Execução local segura

```bash
cd labs/02-api-security
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
export JWT_SECRET="$(python -c 'import secrets; print(secrets.token_urlsafe(48))')"
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

## Execução do modo vulnerável

O modo vulnerável permanece desabilitado por padrão e requer ativação explícita:

```bash
cd labs/02-api-security
export JWT_SECRET="$(python -c 'import secrets; print(secrets.token_urlsafe(48))')"
export VULNERABLE_MODE=true
uvicorn app.vulnerable:app --host 127.0.0.1 --port 8001
```

Ele deve ser executado somente em localhost e em laboratório local.

## Testes

```bash
cd labs/02-api-security
python -m pytest -q
```

## Docker

```bash
cd labs/02-api-security
export JWT_SECRET="$(python -c 'import secrets; print(secrets.token_urlsafe(48))')"
docker compose up --build secure-api
```

Para ativar a API vulnerável, use o perfil dedicado:

```bash
export JWT_SECRET="$(python -c 'import secrets; print(secrets.token_urlsafe(48))')"
docker compose --profile vulnerable-lab up --build
```

## Vulnerabilidade demonstrada

`app/vulnerable.py` reproduz, de forma didática e intencional, um cenário de BOLA/IDOR:
- um usuário autenticado consegue ler e alterar recursos de outro usuário
- o servidor não valida propriedade nem escopo antes da operação

Isto não é evidência de uma aplicação segura; é um laboratório de exploração controlada.

## Correções implementadas

- cadastro público sempre cria `reader`
- remoção de `role` e `scope_id` do payload do cliente
- relatórios criados com `draft` e escopo do usuário autenticado
- `PATCH` sem suporte para alterar status ou escopo
- autorização centralizada em `app/policies.py`
- verificação de usuário ativo em `get_current_user`
- senha armazenada com hash seguro
- JWT com segredo obrigatório de ambiente
- modo vulnerável desativado por padrão
- testes de regressão isolados por fixture e banco temporário

## Limitações

- laboratório didático e sintético
- foco educacional e defensivo
- não substitui revisão de segurança em sistema de produção
- o modo vulnerável não deve ser exposto a redes públicas ou ambientes compartilhados
- o resultado esperado de exploração não equivale a vulnerabilidade real em ambiente externo

## Aviso

Este laboratório não deve ser executado em sistemas externos sem autorização explícita. Os dados são fictícios e a execução deve permanecer restrita a localhost.
