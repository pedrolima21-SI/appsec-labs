# API Security Lab

Este laboratório local simula um sistema fictício de gerenciamento de relatórios para estudo de autenticação, autorização e controle de acesso em APIs REST.

## Objetivo

Demonstrar, em ambiente controlado e local:
- autenticação por token
- perfis de usuário (`reader`, `editor`, `administrator`)
- autorização por usuário, escopo e propriedade do recurso
- reprodução didática de BOLA/IDOR em modo vulnerável
- correção das permissões em modo seguro

## Arquitetura

- FastAPI para a API REST
- SQLite local para persistência
- SQLAlchemy para ORM
- Pytest para testes automatizados
- Docker para execução local em localhost

## Estrutura

```text
labs/02-api-security/
├── README.md
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── app/
│   ├── __init__.py
│   ├── auth.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── policies.py
│   ├── schemas.py
│   ├── main.py
│   └── vulnerable.py
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_secure_reports.py
│   └── test_vulnerable_demo.py
└── data/
    └── .gitkeep
```

## Credenciais fictícias de demonstração

| Usuário | Senha | Papel | Escopo |
| --- | --- | --- | --- |
| alice | alice123 | reader | team-a |
| bob | bob123 | editor | team-a |
| carol | carol123 | editor | team-b |
| admin | admin123 | administrator | org-global |

## Endpoints principais

- `POST /auth/register`
- `POST /auth/token`
- `GET /auth/me`
- `GET /api/reports`
- `POST /api/reports`
- `GET /api/reports/{report_id}`
- `PATCH /api/reports/{report_id}`
- `POST /api/reports/{report_id}/publish`

## Política didática

- `reader`: só lê relatórios do próprio escopo e publicados; não cria nem edita.
- `editor`: cria relatórios e edita apenas os próprios, no mesmo escopo.
- `administrator`: executa somente ações explícitas, como publicar ou consultar em escopo administrativo.
- papéis e ações desconhecidos são negados por padrão.

## Modo vulnerável

A implementação em `app/vulnerable.py` foi criada para reprodução didática de BOLA/IDOR. Ela mantém autenticação, mas não valida corretamente propriedade do recurso.

A execução do modo vulnerável deve ser explícita e restrita a localhost.

## Execução local

```bash
cd labs/02-api-security
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

Modo vulnerável:

```bash
uvicorn app.vulnerable:app --host 127.0.0.1 --port 8001 --reload
```

## Testes

```bash
python -m pytest -q
```

## Limitações

- ambiente local, fictício e isolado
- dados sintéticos e não reais
- sem exposição externa
- não representa ambiente de produção
- resultados de exploração são didáticos e não devem ser tratados como evidência de vulnerabilidade em sistema real

## Aviso

Este laboratório tem objetivo educacional e defensivo. Ele não deve ser executado em sistemas externos sem autorização explícita.
