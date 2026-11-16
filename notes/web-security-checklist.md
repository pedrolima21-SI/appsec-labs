# Checklist de revisão web

Checklist educacional para revisão de aplicações próprias ou ambientes autorizados. Use-o como apoio, não como substituto de análise contextual.

## Escopo e dados

- [ ] Objetivo, ambiente e autorização estão registrados.
- [ ] Dados de teste são fictícios ou foram aprovados para uso.
- [ ] Nenhum segredo, token ou dado pessoal será incluído nos registros.

## Controles de aplicação

- [ ] Regras de autenticação e autorização estão documentadas separadamente.
- [ ] A aplicação aplica autorização no servidor para cada ação protegida.
- [ ] Permissões seguem o menor privilégio e o padrão para acesso não definido é seguro.
- [ ] Entradas são validadas no servidor conforme o tipo e o contexto de uso.
- [ ] Erros são tratados de modo consistente, sem expor dados ou detalhes desnecessários.
- [ ] Sessões, cookies e dados armazenados seguem as necessidades de segurança do contexto.
- [ ] Configurações e dependências têm responsáveis e processo de atualização definidos.

## Registro e conclusão

- [ ] Observações são separadas de hip��teses.
- [ ] Evidências são mínimas, reproduzíveis e sanitizadas.
- [ ] Impacto, limitações e recomendações estão explícitos.
- [ ] A revisão final não contém informações confidenciais.
