# API Security Lab

Laboratório local e didático de uma API fictícia de relatórios. Demonstra autenticação, autorização por papel, propriedade e escopo, além de uma reprodução controlada de BOLA/IDOR. Todos os usuários e conteúdos são sintéticos; não representam dados reais.

## Arquitetura e estrutura

A aplicação usa FastAPI, SQLAlchemy e SQLite. A implementação segura (`app.main:app`) aplica políticas centralizadas; `app.vulnerable:app` é uma demonstração intencionalmente insegura, opcional e somente para execução local.

```text
labs/02-api-security/
├── app/                 # API, autenticação, configuração, modelos e políticas
├── tests/               # testes de autenticação, autorização e demonstração BOLA/IDOR
├── data/                # arquivo SQLite local (não usar dados reais)
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Configuração

Python 3.12+ é necessário para execução local; Docker Compose é opcional. A aplicação exige `JWT_SECRET` com pelo menos 32 caracteres. Gere uma chave local; não a committe:

```bash
export JWT_SECRET="$(python -c 'import secrets; print(secrets.token_urlsafe(48))')"
```

`APP_DB_PATH` define o arquivo SQLite e `DEFAULT_SCOPE_ID` define o escopo que o servidor atribui aos usuários cadastrados. `VULNERABLE_MODE` deve continuar `false` para a execução normal. `.env.example` contém apenas nomes e valores indicativos, não um segredo de produção.

## Execução local — API segura

```bash
cd labs/02-api-security
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
export JWT_SECRET="$(python -c 'import secrets; print(secrets.token_urlsafe(48))')"
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

A documentação OpenAPI fica em `http://127.0.0.1:8000/docs`. O banco de demonstração poderá ser inicializado pela aplicação com contas sintéticas indicadas abaixo.

## Credenciais fictícias

| Usuário | Senha fictícia | Papel | Escopo |
| --- | --- | --- | --- |
| `alice` | `alice12345` | reader | team-a |
| `bob` | `bob12345` | editor | team-a |
| `carol` | `carol12345` | editor | team-b |
| `admin` | `admin12345` | administrator | org-global |
| `inactive` | `inactive12345` | reader inativo | team-a |

Estas credenciais servem somente ao laboratório local. Não as reutilize nem as exponha em serviços reais.

## Modo vulnerável — somente demonstração local

A API vulnerável é desativada por padrão. Habilite-a explicitamente e faça bind somente ao loopback do host:

```bash
export JWT_SECRET="$(python -c 'import secrets; print(secrets.token_urlsafe(48))')"
export VULNERABLE_MODE=true
uvicorn app.vulnerable:app --host 127.0.0.1 --port 8001
```

O modo demonstra acesso indevido a relatórios de outros proprietários (BOLA/IDOR). Não o exponha à internet, rede compartilhada ou dados reais. O seu comportamento inseguro é intencional e não deve ser interpretado como recomendação.

## Endpoints

| Método | Caminho | Finalidade |
| --- | --- | --- |
| POST | `/auth/register` | Cadastro público de leitor; papel e escopo são definidos no servidor |
| POST | `/auth/token` | Login e emissão de token |
| GET | `/auth/me` | Identidade autenticada |
| GET | `/api/reports` | Listagem filtrada pela política de acesso |
| POST | `/api/reports` | Criação de rascunho por papel autorizado |
| GET | `/api/reports/{report_id}` | Consulta autorizada de relatório |
| PATCH | `/api/reports/{report_id}` | Edição de campos permitidos, sujeita à política |
| POST | `/api/reports/{report_id}/publish` | Publicação explícita por administrador autorizado |

## Permissões da implementação segura

- **Reader:** lê relatórios publicados do próprio escopo; não cria nem edita.
- **Editor:** cria rascunhos no próprio escopo e edita somente seus próprios rascunhos.
- **Administrator:** consulta recursos segundo a política administrativa e publica rascunhos por operação explícita.
- Cadastro não aceita papel ou escopo fornecidos pelo cliente. Criação e PATCH não aceitam campos de proprietário, escopo ou estado de publicação.
- Contas inativas e papéis desconhecidos são negados. A autorização deve usar o usuário atual do banco, não claims de papel fornecidas pelo cliente.

## Testes

Instale as dependências no ambiente virtual e execute:

```bash
cd labs/02-api-security
python -m pytest -q
```

Os testes usam dados sintéticos e devem manter bancos separados dos bancos locais de demonstração. A suíte cobre autenticação, tentativa de Mass Assignment, controle de função/propriedade/escopo e a comparação entre a API segura e a reprodução vulnerável. Não considere resultados esperados como resultados executados: registre a saída real do comando.

## Docker Compose

Gere `JWT_SECRET` como descrito acima. Os serviços fazem bind em `0.0.0.0` dentro dos containers, enquanto as portas do host são publicadas apenas em `127.0.0.1`. Cada serviço usa caminho de banco separado.

```bash
cd labs/02-api-security
docker compose config
docker compose up --build secure-api
```

A API segura ficará disponível em `http://127.0.0.1:8000`. Para a demonstração vulnerável, habilite o perfil opcional explicitamente:

```bash
VULNERABLE_MODE=true docker compose --profile vulnerable-lab up --build vulnerable-api
```

Ela ficará disponível somente localmente em `http://127.0.0.1:8001`. Encerre o serviço após a demonstração.

## Limitações e recomendações

Este é um laboratório educacional, sintético e não revisado para produção. Não use dados ou credenciais reais. Mantenha o modo vulnerável isolado e desativado fora da demonstração. Use segredos fortes e exclusivos fora de testes locais, proteja arquivos de banco e execute a suíte antes de considerar qualquer alteração validada.
