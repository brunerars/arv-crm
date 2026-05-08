# arv-crm — Instruções pro Claude

CRM próprio da ARV Systems. Substitui Monday `Comercial 💰` (~R$1.300/mês de R$5.500 total). Pré-vendas + vendas + handoff pra `arv-pm` via evento.

---

## Fonte da verdade

**`SPEC.md` é canônico.** Toda decisão arquitetural foi tomada pelo Bruno em 2026-05-08 e está congelada lá.

Antes de propor qualquer mudança estrutural (novo campo, nova entidade, mudança de enum, mudança de fluxo), **leia o SPEC inteiro** e cheque se a decisão já foi tomada. Se sim, siga. Se não, **flag pro Bruno** antes de implementar — não invente.

Documentos de apoio (referência, não canônica):
- `docs/sources/` — entrada original que virou SPEC (travas, dashboards, manual)
- `docs/discovery/` — análise dos sistemas legados (Monday CRM, gap analysis)
- `docs/ui-mockups/` — 11 telas HTML + design_system + excalidraw
- `data/` — datasets XLSX do Monday legado (input do importer WIP)

---

## Stack

| Camada | Tecnologia |
|---|---|
| Backend | FastAPI 0.115, SQLAlchemy 2 async, Pydantic 2.10 |
| DB | Postgres (asyncpg), Alembic 1.14 |
| Cache/Queue | Redis 5.2 |
| Auth | jose + bcrypt |
| Worker | APScheduler 3.10 |
| HTTP client | httpx 0.28 |
| Rate limit | slowapi 0.1.9 |
| Frontend | Next 15, React 19, TypeScript 5.7, Tailwind 4 |
| Deploy | Docker Swarm + Traefik + Portainer + GHCR |

`backend/requirements.txt` é canônico. `frontend/package.json` idem. Não trocar dependências sem confirmar.

---

## Estado atual

Estado: ~25-30% pronto pela Fase 1A do SPEC. Detalhes em `docs/discovery/ARV-CRM-GAP.md`.

Estimativa restante Fase 1A: 170-286h (5-8 semanas em 30-40h/sem). Detalhe em `SPEC.md` §13.

Migrations aplicadas: `001_initial_users`, `002_empresas_contatos_origens`, `003_leads_atividades_historico_scoring`, `004_add_ativo_fields`. Migrations 005-019 a aplicar (lista em `SPEC.md` §12).

---

## Convenções de deploy (globais ARV)

- Imagem: `ghcr.io/brunerars/arv-crm:latest`
- Network: `network_public` (overlay, external — nunca recriar)
- Traefik entrypoint: `websecure` + `letsencryptresolver`
- Cloudflare: DNS-only (cinza), nunca proxied
- Env vars: definidas no Portainer, nunca no Actions
- Deploy: stack criada manualmente no Portainer no primeiro deploy, depois CD via GitHub Actions
- Repo: `github.com/brunerars/arv-crm` (a criar quando subir)

Template Traefik labels:
```yaml
labels:
  - traefik.enable=true
  - traefik.http.routers.arv-crm.rule=Host(`crm.arvsystems.cloud`)
  - traefik.http.routers.arv-crm.entrypoints=websecure
  - traefik.http.routers.arv-crm.tls.certresolver=letsencryptresolver
  - traefik.http.services.arv-crm.loadbalancer.server.port=8000
networks:
  - network_public
```

---

## Domínio (resumo do SPEC)

15 entidades canônicas. Os blocos críticos:

- **Funil em 2 estágios:** `Lead` (5 etapas pré-vendas) → conversão → `Oportunidade` (8 etapas vendas). Decisão SPEC §1.1.
- **3 papéis:** `pre_vendas | vendas | tecnico` (+ admin). Decisão SPEC §1.2.
- **Orçamento como entidade própria, versionado** (1 Oportunidade : N Orçamentos). SPEC §1.3.
- **Conta = flag `is_cliente` em Empresa** (Fase 1A); refatora pra entidade `Conta` na Fase 2. SPEC §1.4.
- **Score híbrido:** ICP função pura sobre Empresa; Técnico/Oportunidade hardcoded em `scoring_catalog.py`. Mudar perguntas = 1 PR. SPEC §1.5.

15 etapas total (5 lead + 8 oportunidade + conversão + descarte/perda) com travas (`SPEC.md` §4) e SLAs (§6).

---

## Contrato de eventos com arv-pm (CRÍTICO)

`arv-crm` e `arv-pm` rodam em apps separados. Comunicam por webhooks HMAC + retry APScheduler.

**Eventos saída arv-crm:**
- `LEAD_CREATED`, `LEAD_QUALIFIED`
- `OPPORTUNITY_CREATED`, `OPPORTUNITY_PROPOSAL_REQUESTED`
- `PROPOSAL_GENERATED` (após arv-framework gerar proposta)
- `OPPORTUNITY_WON` ← **trigger principal** que faz arv-pm criar Projeto
- `OPPORTUNITY_LOST`

**Eventos entrada arv-crm (do arv-pm):**
- `PROJECT_CREATED` — anota `oportunidade.projeto_id_pm`
- `PROJECT_DELIVERED` — marca `Empresa.is_cliente=true`

Schema completo em `SPEC.md` §9. **Não alterar payload sem coordenar com arv-pm.** Se precisar adicionar campo ao evento, é PR coordenado nos 2 apps.

---

## O que NÃO fazer

- ❌ Inventar entidade fora do SPEC
- ❌ Alterar enum de etapas (5 lead, 8 oportunidade) — congelado
- ❌ Adicionar `Conta` como entidade na Fase 1A (decisão SPEC §1.4: flag em Empresa por enquanto)
- ❌ Tocar em `../arv-pm/` ou `../arv-framework/` — outros apps, outros terminais Claude
- ❌ Criar app de pricing/proposta — vai pro `arv-framework` separado (Fase 3)
- ❌ Criar gestão de projeto pós-venda — vai pro `arv-pm` separado
- ❌ Migrar histórico do Pipeline (1.856 leads) — só WIP migra (decisão SPEC §11)
- ❌ Reverter decisões 1B-5B (SPEC §1) sem alinhar com Bruno
- ❌ Skipar hooks (--no-verify), --no-gpg-sign, force-push em main — sem permissão explícita
- ❌ Usar Make/n8n como cola lógica nova — só o que já funciona em produção fica
- ❌ Adicionar dependências em `requirements.txt` sem motivo claro — Bruno preza por simples > elegante
- ❌ Over-engineering: abstração prematura, factory pra 2 casos, decoradores genéricos. ROI primeiro.

---

## O que fazer

- ✅ Ler SPEC antes de codar qualquer entidade ou rota
- ✅ Atomic commits — 1 commit por feature funcional
- ✅ Testes pra cada router novo (vide `tests/test_api.py` como baseline)
- ✅ Migrations Alembic ordenadas por número (`SPEC.md` §12 lista 005-019)
- ✅ Português brasileiro nos campos UI e mensagens (Bruno e equipe ARV)
- ✅ Inglês nos identificadores de código (snake_case Python, camelCase TS)
- ✅ Comentar somente o "por quê" — nunca o "o quê" (CLAUDE.md global)
- ✅ Quando dúvida entre duas abordagens válidas: perguntar ao Bruno antes de escolher
- ✅ Testar UI no navegador (golden path + edge cases) antes de declarar feito

---

## Comunicação

Bruno responde em PT-BR direto. Sem rodeios, ROI primeiro. Reportar:
- O que está pronto (1 frase)
- Onde travou (se travou)
- Próximo passo proposto (1 frase)

Se uma decisão não está no SPEC e tem >1 caminho válido: parar e perguntar com 2-3 opções claras, recomendação primeiro.

---

## Próximos passos sugeridos

Quando começar, sugestão de ordem (refletindo `SPEC.md` §13.2):

1. **Migrations 005-019** — schema base alinhado ao SPEC (16-32h)
2. **Refactor Lead** — 5 etapas + responsáveis 3 papéis + descarte/reativação (12-20h)
3. **Criar Oportunidade** — entidade + serviços + endpoints + 8 etapas (16-28h)
4. **Orçamento versionado** — entidade nova + cálculo de impostos em % (16-24h)
5. **Score híbrido** — `scoring_catalog.py` + endpoints + recálculo automático (12-20h)
6. **Travas (stage gates)** — validação por transição (`SPEC.md` §4) (8-16h)
7. **3 dashboards Fase 1A** — Saúde do Funil, Tração Pré-Vendas e Vendas, Check-in (24-40h)
8. **Importer WIP** — `backend/scripts/import_monday_wip.py` idempotente (12-20h)
9. **Eventos saída** — webhook emitter + retry + tabela `event_log` (16-24h)
10. **Bugfix `data_entrada`** — substituir por consulta ao histórico (4-8h, migration 019)

Bruno **não vai usar GSD**. Trabalha direto com Claude Code, eventualmente com skills herdadas. Manter overhead mínimo.
