# Gap Analysis — arv-crm
> Avalia o estado real do protótipo vs requisitos da Fase 1A/1B do diagnóstico.
> Data: 2026-05-07 · Modo: read-only · Autor: gap analysis agent

---

## 0. Sumário executivo

- **Estado geral:** o protótipo é um CRM de pré-vendas básico (5 etapas, 1 funil) — está MUITO abaixo do que `travas.txt` e `dashboards.txt` exigem (15 etapas, dois funis pré-vendas/vendas, 9 dashboards). É "esqueleto pronto, requisito real ausente".
- **% pronto da Fase 1A:** **~25-30%**. O que o diagnóstico indicou como "70% pronto" é o **scaffolding** (auth, CRUD de empresas/contatos/leads, kanban, SLA worker rodando, layout). O **domínio de negócio** (etapas reais, travas reais, dashboards reais, distinção pré-vendas/vendas) está praticamente ausente.
- **5 buracos mais críticos:**
  1. **Funil tem 5 etapas no código vs 15 na trava.** Modelo `Lead.etapa` aceita apenas `prospeccao | primeiro_contato | qualificacao | qualificado | descartado`. Não existe `estimativa`, `estimativa_em_conversao`, `projecao_orcamentaria`, `proposta_enviada`, etc. Refazer schema + UI + seed.
  2. **Distinção pré-vendas vs vendas é ESTRUTURAL e não existe.** Não há campo `papel` no `User`, não há `responsavel_pre_vendas_id` vs `responsavel_vendas_id` no `Lead`, não há etapa de handoff. SLA config usa origem (passiva/ativa-vendas/ativa-pre_vendas) mas não diferencia o **dono do lead**.
  3. **Travas só existem como cálculo de "completude" informativo.** O `LeadService.change_stage` (`backend/services/lead_service.py:75`) NÃO valida campos obrigatórios — qualquer transição passa. `COMPLETUDE_MAP` cobre 4 etapas das 15 e está desatualizado.
  4. **Dashboard único e raso.** `dashboard_service.py` retorna 4 KPIs + alertas SLA + summary de atividades. Os 9 dashboards de `dashboards.txt` (Check-in, Saúde do Funil, Tração, etc.) **não existem como rota nem componente**.
  5. **Importer de PIPELINE.xlsx / DADOS-VENDAS.xlsx não existe.** Sem isso, demo da semana 5 fica com dados sintéticos.
- **Estimativa Fase 1A:** **120-180h** de execução focada (3-5 sem em 30-40h/sem) — assumindo refazer schema do funil, criar 3 dashboards reais, importer XLSX, travas mínimas em 4-5 transições, deploy staging.
- **Estimativa Fase 1B:** **+200-300h** — completar 6 dashboards restantes, 11 travas restantes, killchain, migração 10 users.
- **Riscos descobertos:**
  - Migration 003 não tem `ON DELETE`/RESTRICT no FK `empresa_id` da `leads` (apenas implícito, sem cascade) — pode dar inconsistência em soft delete.
  - `data_entrada` é usada como "tempo na etapa atual" tanto no SLA quanto no card (`KanbanCard.tsx:24`) — está errado: deveria ser `created_at` da última `HistoricoEtapa`. Bug funcional.
  - `Atividade.responsavel_id` não tem cascade configurado — se deletar user, atividades ficam órfãs.
  - Não há índices criados nas migrations (apenas PKs/FKs implícitos). Queries do dashboard vão degradar com 1.875 leads importados.
  - Tudo assume single-tenant; não há `team_id` ou multi-tenancy. OK pra ARV, mas amarra para sempre.
  - Frontend não tem nenhum gerenciamento de erro global além de `try/catch` solto. `globalThis.fetch` direto, sem retry.
  - `migrations` numeradas `001-004` mas com `Create Date: 2024-01-01` (datas mock). OK, só notar.

---

## 1. Estrutura geral

### 1.1 Backend

**Stack confirmada:**
- FastAPI (com `slowapi` rate limiter), uvicorn
- SQLAlchemy 2 async + asyncpg + Postgres 15
- Alembic (migrations rodam no `lifespan` do FastAPI — `main.py:23`)
- Redis (sessões + cache CNPJ + violations SLA)
- APScheduler em processo separado (`run_workers.py`)
- httpx (CNPJ enrichment via receitaws.com.br)
- bcrypt + JWT (HS256, 8h)
- pydantic-settings, gzip middleware, CORS

**Models implementados** (`backend/models/`):
- `User` — id, email, password_hash, name, **role** (apenas `admin`/`user` — não há "papel comercial: pre_vendas/vendas/tecnico").
- `Empresa` — completo: nome_fantasia, razao_social, cnpj, segmento, num_funcionarios, num_plantas, distancia_arv_km, cidade/estado/cep, telefone, site, status_conta (prospect/com_oportunidade/cliente_ativo/inativo), responsavel_id, observacoes, ativo.
- `Contato` — empresa_id (CASCADE), nome, cargo, departamento, **nivel_influencia** (operacional/influenciador/decisor), email, whatsapp, linkedin, ativo.
- `Atividade` — lead_id (CASCADE), responsavel_id, tipo (string livre), descricao, data_prevista, data_conclusao, concluida.
- `Origem` — tipo, sub_tipo, descricao. Seed na migration 002 inclui `passiva/site`, `passiva/indicacao_cliente`, `ativa/pre_vendas`, `ativa/vendas`, `ativa/linkedin`, etc.
- `ScoringResposta` — lead_id, criterio, valor, pontos. Tabela existe mas sem UI dedicada além do "Recalcular".
- `HistoricoEtapa` — lead_id, etapa_anterior, etapa_nova, **tempo_na_etapa_segundos**, usuario_id.
- `Lead` — etapa default `"prospeccao"`, sub_status, temperatura, produto_interesse, area_atuacao, tipo_entrega, lead_score, classificacao (A/B/C/D), valor_estimado, motivo_descarte, data_entrada, data_qualificacao, prox_atividade, data_prox_atividade, ativo. **NÃO tem:** responsavel_pre_vendas_id, responsavel_vendas_id, responsavel_tecnico_id, dados de "Foi apresentado", "Foi enviado", "Aprovada internamente", "Visita técnica realizada", aba meta de vendas etc.

**Routers expostos** (todos sob `/api`, autenticados):
- `auth`: POST `/auth/register`, POST `/auth/login`, GET `/auth/me`, POST `/auth/users` (admin), POST `/auth/logout`.
- `empresas`: GET, POST, GET/{id}, PUT/{id}, DELETE/{id} (soft), POST `/{id}/enrich-cnpj`.
- `contatos`: GET, POST, GET/{id}, PUT/{id}, DELETE/{id} (soft).
- `origens`: GET (apenas list).
- `leads`: GET `/kanban`, GET, POST, GET/{id}, PUT/{id}, DELETE/{id} (soft), POST `/{id}/change-stage`, GET `/{id}/completude`, GET `/{id}/historico`, POST `/{id}/calculate-score`.
- `atividades`: GET, POST, POST `/{id}/complete`. Sem PUT/DELETE.
- `dashboard`: GET `/` (retorna kpis + sla_alerts + activity_summary). **Apenas 1 endpoint, retorno único.**
- Health: GET `/api/health`.

**Services implementados:**
- `LeadService` (lead_service.py) — `create_lead` (gera lead_id sequencial L-NNNN), `change_stage` (cria HistoricoEtapa, calcula tempo_na_etapa_segundos), `calculate_completude` (informativo, NÃO bloqueia), `get_kanban`. Lógica real funcional.
- `DashboardService` (dashboard_service.py) — `get_kpis` (leads_novos_mes, por_etapa, valor_pipeline, taxa_conversao, por_temperatura), `get_sla_alerts` (linear scan de todos leads), `get_activity_summary` (atividades hoje/atrasadas/semana, leads sem atividade/sem prox). Funcional, mas é só 1 dashboard.
- `ScoringService` (scoring_service.py) — calcula score de 0 a ~95 baseado em segmento, num_funcionarios, num_plantas, distancia_arv_km. Classifica A/B/C/D em thresholds 70/50/30. Hardcoded; sem UI editável.
- `cnpj_service` — receitaws.com.br + cache Redis 24h.
- `session` — Redis SET com TTL 8h, lookup por user_id.

**Workers:**
- `sla_scheduler.check_sla_violations` — single job a cada 1h. Itera todos leads ativos e checa contra `SLA_RULES` (apenas 7 regras, 3 etapas: prospeccao, primeiro_contato, qualificacao). Persiste violations no Redis com chave `sla:violations:YYYY-MM-DD` TTL 24h. **BUG:** usa `lead.data_entrada` como referência de tempo na etapa atual (linha 56 `sla_scheduler.py`, linha 89 `dashboard_service.py`); deveria usar `created_at` da última `HistoricoEtapa`. Funciona para etapa inicial; quebra ao mudar etapa.

**Migrations** (`backend/migrations/versions/`):
- `001_initial_users.py` — tabela users (id, email, password_hash, name, role, created_at).
- `002_empresas_contatos_origens.py` — empresas, contatos, origens. **Inclui seed de 9 origens** (passiva: site/indicacao_cliente/indicacao_parceiro · ativa: pre_vendas/vendas/linkedin · indicacao: cliente/parceiro/colaborador).
- `003_leads_atividades_historico_scoring.py` — sequence `lead_id_seq`, leads, atividades, historico_etapas, scoring_respostas.
- `004_add_ativo_fields.py` — adiciona `ativo` em empresas e leads.

Sem índices explícitos; sem migration de "etapas estendidas"; sem migration para campos pré-vendas/vendas.

### 1.2 Frontend

**Stack confirmada:** Next 15 (App Router), React 19, Tailwind 4, TypeScript. Auth via Context + apiClient com Bearer token. Material Icons via classes CSS.

**Páginas implementadas:**
- `/` (login) — `app/page.tsx`
- `/register` — `app/register/page.tsx`
- `/dashboard` — KPIs + alertas SLA + atividades summary (1 dashboard genérico)
- `/dashboard/empresas` — DataTable + filtros + modal create
- `/dashboard/empresas/[id]` — detalhe da empresa
- `/dashboard/contatos` — DataTable básica (sem CRUD na lista; só leitura)
- `/dashboard/pipeline` — Kanban 5 colunas com filtros temperatura/search
- `/dashboard/pipeline/[id]` — detalhe lead com tabs (resumo, empresa, atividades, scores, histórico) + StageProgress + Completude

**Componentes:**
- Layout: `Sidebar`, `Topbar` (referenciado no layout, não inspecionado)
- Data: `DataTable`, `KanbanBoard`, `KanbanCard`, `ActivityTimeline`, `StageProgress`
- Form: `EmpresaForm`, `ContatoForm`, `CreateLeadModal`
- Display: `KpiCard`, `AlertCard`, `ActivityCard`, `CompletudeBadge`, `FilterBar`

**Estado:**
- `AuthContext` + `ToastContext` (Context API). Sem store global (Redux/Zustand). Sem SWR/React Query — `apiClient` puro com `fetch`. Token em memória via `apiClient.setToken` (provavelmente persistido em localStorage no AuthContext, não inspecionei).

**Tipos compartilhados (`lib/types.ts`):** cobre User, Empresa, Contato, Origem, Lead, LeadDetail, Kanban, Completude, HistoricoEtapa, Atividade, DashboardKpis/SlaAlert/ActivitySummary/DashboardData. **`LeadEtapa` é apenas `"prospeccao" | "primeiro_contato" | "qualificacao" | "qualificado" | "descartado"`** — espelha o backend incompleto.

### 1.3 Distinção pré-vendas vs vendas

**Existe? PARCIAL — apenas no nível de `Origem`.**

- Existe na origem: `Origem.sub_tipo` aceita `pre_vendas` e `vendas`, e o seed da migration 002 cria essas duas. SLA config (`sla_config.py:5-13`) tem regras diferentes para `("prospeccao", "ativa", "vendas")=15d` vs `("prospeccao", "ativa", "pre_vendas")=7d`. **Isso cobre apenas "de onde veio o lead", não "quem é o dono atual e em qual fase do funil".**
- **NÃO existe no User:** `User.role` é apenas `admin/user`. Não há `papel_comercial` (pré-vendas, vendas, técnico). `Sidebar.tsx` exibe role como "Administrador" / "Usuário" texto livre.
- **NÃO existe no Lead:** apenas `responsavel_id` único. O dashboard "Saúde do Funil" pede "Oportunidades por Vendedor e Pré-Vendedor"; "Tração e Performance Pré-Vendas e Vendas" pede distribuição por responsável comercial; "Tração Técnica" pede responsável técnico. **Tudo isso é impossível com 1 só FK.**
- **NÃO existe a etapa "Passagem Pré-vendas → Vendas":** `dashboards.txt` linha 49 explicita "Passagem Pré-vendas – Vendas: gráfico de barras com SLA de 7 dias". O modelo de etapas atual não tem essa etapa nem evento de handoff.
- **NÃO existe a noção de "fases" macro do funil:** `travas.txt` agrupa implicitamente:
  - Pré-vendas: QUALIFICAÇÃO INICIAL → QUALIFICAÇÃO DA OPORTUNIDADE → ESTIMATIVA → ESTIMATIVA EM CONVERSÃO
  - Handoff: passagem pré-vendas → vendas (SLA 7d)
  - Vendas: PROJEÇÃO ORÇAMENTÁRIA → PROJEÇÃO EM CONVERSÃO → DESENVOLVIMENTO DE PROPOSTA → PROPOSTA ENVIADA → PROPOSTA EM ANÁLISE TÉCNICA → PROPOSTA EM ANÁLISE COMERCIAL → PROPOSTA EM NEGOCIAÇÃO → EMISSÃO DO PEDIDO DE COMPRA → PEDIDO CONVERTIDO EM VENDA

**Impacto na Fase 1A:** ESTRUTURAL. Sem isso, dashboards "Saúde do Funil" e "Tração Pré-Vendas e Vendas" não conseguem segmentar como pedido. É decisão de schema (precisa de migration 005+006) e impacta toda UI.

---

## 2. Cobertura travas.txt (15 etapas)

> Backend hoje só tem `prospeccao | primeiro_contato | qualificacao | qualificado | descartado`. Nenhuma das 15 etapas reais está implementada por nome. Nenhuma é validada em transição (apenas `change_stage` confere se a etapa-alvo está na lista de 5).
>
> "Validação na transição" hoje é APENAS o check de etapa válida em `lead_service.py:83`. NÃO há leitura do COMPLETUDE_MAP nem bloqueio.

| # | Etapa (travas.txt) | Campos exigidos | Backend tem etapa? | Backend tem campos? | Backend bloqueia transição? | Frontend bloqueia? | Status |
|---|---|---|---|---|---|---|---|
| 1 | QUALIFICAÇÃO INICIAL | nome empresa, origem, sub-origem, cnpj, telefone fixo, nome contato, telefone/whatsapp, email | ⚠️ existe `prospeccao` (nome diferente) | ✅ todos campos existem em Empresa/Contato/Origem | ❌ não bloqueia | ⚠️ exibe completude no detail, mas botão de transição não trava | ⚠️ Parcial |
| 2 | QUALIFICAÇÃO DA OPORTUNIDADE | produto, área de atuação | ⚠️ existe `primeiro_contato` (nome diferente) | ✅ `Lead.produto_interesse`, `Lead.area_atuacao` | ❌ | ❌ | ⚠️ Parcial |
| 3 | ESTIMATIVA | tipo de entrega "estimativa", opportunity score preenchido | ❌ etapa não existe | ⚠️ `Lead.tipo_entrega` é string livre, sem enum; `lead_score` existe | ❌ | ❌ | ❌ Faltando |
| 4 | ESTIMATIVA EM CONVERSÃO | foi apresentado SIM, foi enviado ao cliente SIM, data envio | ❌ etapa não existe | ❌ campos `foi_apresentado`, `foi_enviado_cliente`, `data_envio` não existem | ❌ | ❌ | ❌ Faltando |
| 5 | PROJEÇÃO ORÇAMENTÁRIA | tipo de entrega "projeção" | ❌ | ⚠️ tipo_entrega é livre | ❌ | ❌ | ❌ Faltando |
| 6 | PROJEÇÃO EM CONVERSÃO | reunião agendada SIM, aprovada internamente SIM | ❌ | ❌ | ❌ | ❌ | ❌ Faltando |
| 7 | DESENVOLVIMENTO DE PROPOSTA | data reunião passagem de bastão, infos técnicas SIM, infos comerciais SIM | ❌ | ❌ | ❌ | ❌ | ❌ Faltando |
| 8 | PROPOSTA ENVIADA | aba meta de vendas preenchida (preencher 0 quando vazio) | ❌ | ❌ | ❌ | ❌ | ❌ Faltando |
| 9 | PROPOSTA EM ANÁLISE TÉCNICA | proposta enviada SIM, cliente confirmou recebimento SIM, prazo avaliação técnica preenchido | ❌ | ❌ | ❌ | ❌ | ❌ Faltando |
| 10 | PROPOSTA EM ANÁLISE COMERCIAL | visita técnica realizada SIM, solução técnica aprovada SIM, prazo análise comercial, email enviado ao comprador SIM | ❌ | ❌ | ❌ | ❌ | ❌ Faltando |
| 11 | PROPOSTA EM NEGOCIAÇÃO | prazo retorno negociação, valor dentro expectativa SIM, visita comercial realizada SIM | ❌ | ❌ | ❌ | ❌ | ❌ Faltando |
| 12 | EMISSÃO DO PEDIDO DE COMPRA | condições comerciais aceitas SIM, intenção de compra SIM, prazo emissão pedido, prazo atendimento SIM | ❌ | ❌ | ❌ | ❌ | ❌ Faltando |
| 13 | PEDIDO CONVERTIDO EM VENDA | pedido recebido SIM, conferido SIM, pasta atualizada SIM, número OS preenchido | ❌ | ❌ | ❌ | ❌ | ❌ Faltando |
| 14 | LEADS DESCARTADOS | motivo descarte preenchido | ✅ existe `descartado` | ✅ `Lead.motivo_descarte` | ⚠️ frontend exige `prompt()` mas backend aceita vazio | ⚠️ valida via prompt JS no frontend (`pipeline/[id]/page.tsx:48`), backend NÃO valida | ⚠️ Parcial |
| 15 | PASSAGEM PRÉ-VENDAS → VENDAS | (implícita em dashboards.txt — SLA 7d) | ❌ | ❌ | ❌ | ❌ | ❌ Faltando |

**Resumo cobertura travas.txt:** 0 etapas totalmente implementadas, 3 parciais (mapeadas para nomes diferentes), 12 ausentes (incluindo handoff).

---

## 3. Cobertura dashboards.txt (9 dashboards)

> Hoje o backend tem **1 endpoint**: `GET /api/dashboard` retornando kpis genéricos + sla_alerts + activity_summary. **Nenhum dos 9 dashboards descritos está implementado individualmente.**

| Dashboard | Métrica principal | Endpoint backend? | Componente frontend? | Status | Fase |
|---|---|---|---|---|---|
| **Check-in** | Tarefas Concluídas por Usuário (Mês) | ❌ (precisa agregação por user × mês) | ❌ | ❌ | 1A |
| Check-in | Tarefas Atrasadas por Usuário | ⚠️ existe `atividades_atrasadas` total, sem split por user | ❌ | ⚠️ | 1A |
| Check-in | Tarefas para Concluir Essa Semana | ⚠️ existe `atividades_semana` total, sem split por user | ❌ | ⚠️ | 1A |
| Check-in | Lead sem Atividade por Responsável | ⚠️ existe count agregado, sem split por user | ❌ | ⚠️ | 1A |
| Check-in | Lead sem Próxima Atividade por Responsável | ⚠️ idem | ❌ | ⚠️ | 1A |
| Check-in | Lead com Reunião Interna Essa Semana | ❌ `Atividade.tipo` é string livre, busca por "Reunião Interna" possível mas não exposta | ❌ | ❌ | 1A |
| Check-in | Planejamento de Trabalho (bolhas, 15/dia) | ❌ | ❌ | ❌ | 1A |
| **Planejamento de Visita** | Visitas Planejadas/Agendadas/Realizadas (mês) | ❌ não há entidade/tipo dedicado de "visita"; só Atividade.tipo livre | ❌ | ❌ | 1B |
| Planejamento de Visita | Visitas por Vendedor/Zona SP/Estado | ❌ | ❌ | ❌ | 1B |
| **Entrada de Leads** | Entrou em Lead Inicial Ativa Pré/Vendas (meta 40/usuário) | ❌ não existe meta nem agregação por user × origem | ❌ | ❌ | 1B |
| Entrada de Leads | SLA Lead Inicial — Origem Passiva (3d) | ⚠️ regra existe em `sla_config.py`, falta UI | ❌ | ⚠️ | 1B |
| Entrada de Leads | SLA Lead Inicial — Ativa Vendas (15d) | ⚠️ regra existe | ❌ | ⚠️ | 1B |
| Entrada de Leads | SLA Lead Inicial — Ativa Pré-Vendas (7d) | ⚠️ regra existe | ❌ | ⚠️ | 1B |
| Entrada de Leads | SLA Qualificação Inicial — Passiva (7d) | ⚠️ idem | ❌ | ⚠️ | 1B |
| Entrada de Leads | SLA Qualif Inicial — Ativa Vendas (30d) | ⚠️ idem | ❌ | ⚠️ | 1B |
| Entrada de Leads | SLA Qualif Inicial — Ativa Pré-Vendas (20d) | ⚠️ idem | ❌ | ⚠️ | 1B |
| Entrada de Leads | SLA Qualif Oportunidade — 15d | ⚠️ regra `("qualificacao", None, None): 15` existe | ❌ | ⚠️ | 1B |
| Entrada de Leads | Leads Mês por Origem (meta 300) | ⚠️ count(leads) por origem é trivial; falta meta + UI | ❌ | ⚠️ | 1B |
| Entrada de Leads | Leads Mês por Sub-Origem | ⚠️ idem | ❌ | ⚠️ | 1B |
| Entrada de Leads | Quantidade/Qualidade ICP (leadscore) | ⚠️ `lead_score` existe; falta agregação | ❌ | ⚠️ | 1B |
| Entrada de Leads | Qtd/Motivo Descartados | ⚠️ `motivo_descarte` existe; falta agregação | ❌ | ⚠️ | 1B |
| Entrada de Leads | Etapa Atual dos Leads do Mês | ⚠️ trivial groupby | ❌ | ⚠️ | 1B |
| **Topo de Funil** | Análise Interna SLA 5d | ❌ etapa `analise_interna` não existe | ❌ | ❌ | 1B |
| Topo de Funil | Estimativa Orçamentária SLA 5d | ❌ etapa não existe | ❌ | ❌ | 1B |
| Topo de Funil | Estimativa em Conversão SLA 20d | ❌ | ❌ | ❌ | 1B |
| Topo de Funil | Qtd Tarefas em Estimativa em Conversão | ❌ | ❌ | ❌ | 1B |
| Topo de Funil | Tempo entre atividades (Estimativa em Conversão) | ❌ | ❌ | ❌ | 1B |
| Topo de Funil | Passagem Pré-vendas → Vendas SLA 7d | ❌ etapa de handoff não existe | ❌ | ❌ | 1B |
| **Meio de Funil** | Projeção Orçamentária SLA 15d | ❌ | ❌ | ❌ | 1B |
| Meio de Funil | Qtd tarefas + tempo entre tarefas em Projeção | ❌ | ❌ | ❌ | 1B |
| Meio de Funil | Projeção em Conversão SLA 30d | ❌ | ❌ | ❌ | 1B |
| **Fundo de Funil** | Desenvolvimento Proposta SLA 15d | ❌ | ❌ | ❌ | 1B |
| Fundo de Funil | Proposta Enviada SLA 3d | ❌ | ❌ | ❌ | 1B |
| Fundo de Funil | Qtd tarefas + tempo entre tarefas | ❌ | ❌ | ❌ | 1B |
| **Saúde do Funil** | Entradas no Mês × Meta por etapa (8 etapas) | ❌ não existe estrutura de Meta | ❌ | ❌ | **1A** |
| Saúde do Funil | Volume Atual por Etapa | ⚠️ existe `kpis.leads_por_etapa` (rasa) | ⚠️ exibido só como chave-valor, sem visualização | ⚠️ | **1A** |
| Saúde do Funil | Temperatura Comercial × Técnica | ❌ existe `Lead.temperatura` (1 só) — não há temperatura técnica vs comercial | ❌ | ❌ | **1A** |
| Saúde do Funil | Por Vendedor e Pré-Vendedor | ❌ não há esses 2 papéis no schema | ❌ | ❌ | **1A** |
| Saúde do Funil | Por Origem | ⚠️ trivial | ❌ | ⚠️ | **1A** |
| **Tração Pré-Vendas e Vendas** | Cards entrada/evolução mês × meta | ❌ | ❌ | ❌ | **1A** |
| Tração Pré-Vendas/Vendas | Pizza por usuário (volume) | ❌ | ❌ | ❌ | **1A** |
| Tração Pré-Vendas/Vendas | Pizza por usuário (valor R$) | ❌ | ❌ | ❌ | **1A** |
| **Tração Técnica** | Projeção em Conversão / Propostas — volume | ❌ não há `responsavel_tecnico_id` | ❌ | ❌ | 1B |
| Tração Técnica | Por responsável técnico — valor R$ | ❌ | ❌ | ❌ | 1B |
| **Meta de Vendas** | Resultado Previsto (%), Vendas Previstas R$ | ❌ não há entidade Meta | ❌ | ❌ | 1B |
| Meta de Vendas | Antecipações Previstas/Confirmadas | ❌ | ❌ | ❌ | 1B |
| **Resultado Anual** | Medição, Meta Anual, Atingida, Previsão Anual | ❌ não há entidade Meta nem snapshot anual | ❌ | ❌ | 1B |

**Resumo:** dos 9 dashboards, **0 implementados completos**, **1 (dashboard único genérico) parcial**, **8 ausentes**. Os 3 priorizados pelo diagnóstico para Fase 1A (Check-in, Saúde do Funil, Tração) estão **0% prontos**.

---

## 4. Buracos críticos

1. **Funil curto (5 etapas vs 15 reais).**
   - Onde: `backend/services/lead_service.py:13` `ETAPAS_ORDER`; `backend/services/dashboard_service.py:13` (não existe lista de etapas reais); `frontend/src/lib/types.ts:105` `LeadEtapa`; `frontend/src/components/StageProgress.tsx:3` `STAGES`; `frontend/src/components/KanbanBoard.tsx:5` `ETAPA_LABELS`.
   - Impacto: nenhum dashboard "por etapa real" funciona; não dá pra demonstrar funnel completo; travas das etapas reais não rodam.
   - Estimativa: **8-16h** (criar enum compartilhado, migration 005 alter `Lead.etapa` + reseed, atualizar UI Kanban + StageProgress + types + COMPLETUDE_MAP).

2. **Distinção pré-vendas / vendas / técnico ausente no schema.**
   - Onde: `backend/models/user.py:18` (só admin/user); `backend/models/lead.py:22` (`responsavel_id` único); `backend/sla_config.py` usa `sub_tipo` da Origem como proxy.
   - Impacto: dashboards "Saúde do Funil — Por Vendedor e Pré-Vendedor", "Tração Pré-Vendas e Vendas — por usuário", "Tração Técnica — por responsável técnico" são impossíveis. Etapa "Passagem Pré-Vendas → Vendas" não modelável.
   - Estimativa: **8-12h** (BLOCKER de design — decidir 2 FKs separadas em Lead OU tabela `lead_responsabilidade(lead_id, user_id, papel)`; criar migration 006; ajustar schemas, services, UI).

3. **Travas (stage gates) NÃO bloqueiam transição.**
   - Onde: `backend/services/lead_service.py:75 change_stage` apenas valida que etapa está em `ETAPAS_ORDER`; `calculate_completude` é informativo. Frontend valida só descarte (com `window.prompt`).
   - Impacto: usuário pode pular etapa sem ter campos preenchidos. Funil sem disciplina, dashboards mentem.
   - Estimativa: **12-20h** (criar `validate_stage_transition(lead, nova_etapa) -> raise HTTPException(422)` com mapa de campos exigidos; criar `STAGE_GATES_MAP` espelhando `travas.txt`; UI exibir lista de campos faltantes + bloquear botão).

4. **Dashboards reais (9) ausentes; só existe `/api/dashboard` genérico.**
   - Onde: `backend/routers/dashboard.py` tem 1 endpoint; `backend/services/dashboard_service.py` tem 3 funções.
   - Impacto: a entrega da Fase 1A pede "Check-in, Saúde do Funil, Tração" — todos zerados em backend e frontend.
   - Estimativa: **40-80h** (3 dashboards × 12-25h cada incluindo backend agregação + endpoints + componentes Recharts/similar + roteamento Next).

5. **Sem importer de XLSX (`PIPELINE.xlsx`, `DADOS-VENDAS.xlsx`).**
   - Onde: não existe nenhum script. Diagnóstico (linha 122) prevê "Importar PIPELINE.xlsx + DADOS-VENDAS.xlsx" como primeira ação da Fase 1A.
   - Impacto: demo da semana 5 sem dados reais. Sem isso, dashboards são vazios.
   - Estimativa: **12-24h** (script Python `scripts/import_pipeline.py` mapeando 183 colunas Monday → Empresa/Contato/Lead/Atividade; tratamento de duplicatas por CNPJ; relatório de erros). **DEPENDE de mapping documentado** (Fase 0 — dry-run).

6. **Bug `data_entrada` usada como "tempo na etapa atual".**
   - Onde: `backend/services/dashboard_service.py:89`, `backend/workers/sla_scheduler.py:56`, `frontend/src/components/KanbanCard.tsx:24`.
   - Impacto: SLA fica errado para qualquer lead que mudou de etapa pelo menos uma vez. KPI de "dias na etapa" sempre mostra dias desde entrada no funil. Critical pra demo: SLA do dashboard SEMPRE estará errado depois das primeiras transições.
   - Estimativa: **3-6h** (passar a calcular `now - max(HistoricoEtapa.created_at where lead_id=X and etapa_nova=lead.etapa)`).

7. **Sem entidade Meta / metas mensais.**
   - Onde: não existe.
   - Impacto: 4 dashboards (Saúde do Funil, Tração Pré-Vendas, Meta de Vendas, Resultado Anual) referenciam "comparação com meta". Sem entidade Meta, todos virariam mock.
   - Estimativa: **8-16h** (model `Meta(periodo, etapa, papel, valor_qtd, valor_rs)`, CRUD admin, migration 007, integração nos endpoints de dashboards).

8. **Atividade.tipo é string livre — relatórios "Reunião Interna esta semana", "Visita Realizada" dependem de filtros frágeis.**
   - Onde: `backend/models/atividade.py:17` `tipo: Mapped[str] = mapped_column(String(50), nullable=False)`.
   - Impacto: queries por tipo dependem de string match exato; usuários podem criar tipos divergentes.
   - Estimativa: **3-6h** (enum + validador no schema; migration leve para padronizar dados existentes).

9. **Sem campo de "valor financeiro" diferenciado para Projeção em Conversão / Proposta — `valor_estimado` é único.**
   - Onde: `Lead.valor_estimado` é genérico.
   - Impacto: dashboard "Tração Técnica — Projeção (R$) vs Proposta (R$)" precisa diferenciar valor por etapa.
   - Estimativa: **4-8h** (campos `valor_projecao`, `valor_proposta` ou audit trail por etapa).

10. **Sem deploy staging configurado (Docker/Traefik/Portainer pendente).**
    - Onde: existe `docker-compose.prod.yml` mas não há labels Traefik nem stack pronta para Portainer (pelas convenções globais).
    - Impacto: demo precisa URL HTTPS no Hostinger.
    - Estimativa: **4-8h** (escrever stack Portainer com labels Traefik para `crm-staging.arvsystems.cloud`, configurar GHCR, primeiro deploy manual).

---

## 5. Plano Fase 1A (MVP-demo) — tasks com estimativa

> Ordem importa. Tarefas BLOCKER de design devem ser decididas antes do código.
>
> Categoria: **S** = 1-3h · **M** = 4-12h · **L** = 12-40h · **BLOCKER-D** = decisão de design

| # | Task | Arquivo principal | Pré-req | Categoria | Estimativa |
|---|---|---|---|---|---|
| 1 | **DECISÃO:** modelar pré-vendas/vendas como (a) 2 FKs `responsavel_pre_vendas_id`/`responsavel_vendas_id` em Lead + campo `papel` em User, OU (b) tabela `lead_responsabilidade` muitos-para-muitos | — | — | BLOCKER-D | 1-2h discussão |
| 2 | **DECISÃO:** etapas reais — usar 15 do `travas.txt` 1:1 ou agrupar em "fase macro" + "sub-status"? | — | — | BLOCKER-D | 1-2h |
| 3 | Migration 005: estender `Lead.etapa` enum/check para 15 etapas; adicionar etapa `passagem_pre_vendas_vendas` | `backend/migrations/versions/005_funil_completo.py` | #2 | M | 4-6h |
| 4 | Migration 006: schema pré-vendas/vendas (conforme decisão #1); adicionar `User.papel_comercial` | `backend/migrations/versions/006_papeis.py` | #1 | M | 4-6h |
| 5 | Migration 007: campos por etapa (foi_apresentado, foi_enviado_cliente, data_envio, reuniao_agendada, aprovada_internamente, data_passagem_bastao, infos_tecnicas_ok, infos_comerciais_ok, prazo_avaliacao_tecnica, visita_tecnica_realizada, valor_proposta, ...) | `backend/migrations/versions/007_campos_travas.py` | #3 | M | 6-10h |
| 6 | Atualizar `Lead`/`User` models, schemas Pydantic e `lib/types.ts` para refletir 005-007 | `backend/models/lead.py`, `backend/schemas/lead.py`, `frontend/src/lib/types.ts` | #3-5 | M | 4-8h |
| 7 | Implementar `STAGE_GATES_MAP` espelhando `travas.txt`; criar `validate_stage_transition` em `LeadService.change_stage`; retornar 422 com lista de campos faltantes | `backend/services/lead_service.py` | #6 | M | 6-10h |
| 8 | Frontend: bloquear botão de etapa quando `completude.missing.length > 0`; substituir `prompt()` de descarte por modal | `frontend/src/components/StageProgress.tsx`, `pipeline/[id]/page.tsx` | #7 | S | 3-4h |
| 9 | Atualizar Kanban para 15 colunas (ou agrupar visualmente em fases macro) | `frontend/src/components/KanbanBoard.tsx`, `pipeline/page.tsx` | #6 | M | 4-8h |
| 10 | **Bug fix:** `data_entrada` → calcular tempo na etapa via última `HistoricoEtapa.created_at` | `backend/workers/sla_scheduler.py:56`, `dashboard_service.py:89`, `KanbanCard.tsx:24` | #6 | S | 3-6h |
| 11 | Estender `SLA_RULES` em `sla_config.py` para cobrir todas as etapas e SLAs do `dashboards.txt` (15 SLAs) | `backend/sla_config.py` | #3 | S | 2-3h |
| 12 | Importer PIPELINE.xlsx → Empresa/Contato/Lead/Atividade. Detectar duplicatas por CNPJ; relatório de erros; modo `--dry-run` | `backend/scripts/import_pipeline.py` (criar) | #6 | L | 12-24h |
| 13 | Importer DADOS-VENDAS.xlsx → histórico de leads convertidos + valores reais (alimentar dashboards de tração) | `backend/scripts/import_vendas.py` (criar) | #12 | M | 8-12h |
| 14 | Backend: endpoint `/api/dashboard/saude-funil` — retornar entradas mês × meta por etapa, volume atual, temperatura, distribuição vendedor/pré-vendedor/origem | `backend/routers/dashboard.py`, novo `services/saude_funil_service.py` | #4, #6 | L | 12-20h |
| 15 | Frontend: página `/dashboard/saude-funil` com gráficos (lib? `recharts` ou `chart.js`) — cards meta/volume + barras + pizzas | `frontend/src/app/dashboard/saude-funil/page.tsx` (criar) | #14 | L | 12-20h |
| 16 | Backend: endpoint `/api/dashboard/check-in` — tarefas por user (mês), atrasadas por user, semana por user, leads sem atividade/sem prox por user, "Reunião Interna esta semana" por user | `backend/routers/dashboard.py`, novo `services/checkin_service.py` | #6 | M | 8-12h |
| 17 | Frontend: página `/dashboard/check-in` com gráficos | `frontend/src/app/dashboard/check-in/page.tsx` | #16 | M | 8-12h |
| 18 | Backend: endpoint `/api/dashboard/tracao` — entrada/qualif/estimativa/projeção/proposta no mês × meta + por user (volume e R$) | `backend/routers/dashboard.py`, novo `services/tracao_service.py` | #4, #7 | L | 12-20h |
| 19 | Frontend: página `/dashboard/tracao` | `frontend/src/app/dashboard/tracao/page.tsx` | #18 | L | 12-16h |
| 20 | Entidade Meta: model + migration + CRUD admin (mínimo seed manual via SQL) | `backend/models/meta.py`, `migrations/008_metas.py`, `routers/metas.py` | — | M | 8-12h |
| 21 | Atualizar `Sidebar` com 3 links de dashboards | `frontend/src/components/Sidebar.tsx` | #15, #17, #19 | S | 1-2h |
| 22 | `Atividade.tipo` virar enum (`Ligação`/`Email`/`Reunião`/`Visita`/`Reunião Interna`/`Follow-up`/`Outro`); validador Pydantic; padronizar dados existentes | `backend/models/atividade.py`, `schemas/atividade.py` | #12 | S | 2-3h |
| 23 | Adicionar índices em campos de query frequente: `leads(etapa, ativo)`, `leads(responsavel_id, ativo)`, `historico_etapas(lead_id, created_at desc)`, `atividades(lead_id, concluida)`, `atividades(responsavel_id, data_prevista)` | `migrations/009_indexes.py` | #6 | S | 2-3h |
| 24 | Configurar deploy staging: stack `docker-compose.prod.yml` ajustada com labels Traefik para `crm-staging.arvsystems.cloud`; build/push GHCR `ghcr.io/brunerars/arv-crm-backend:latest`, `arv-crm-frontend:latest`; criar stack no Portainer; primeiro deploy manual | `docker-compose.prod.yml`, `.github/workflows/*` (criar) | #15, #17, #19 | M | 6-10h |
| 25 | Onboarding piloto: criar 2-3 users, sessão de feedback estruturada, documento de bugs/wishlist | — | #24 | S | 2-4h |

**Total Fase 1A: 130-220h** — chute médio **~175h** considerando fricção de decisões e retrabalho. Em 30-40h/sem dedicadas, **4-6 semanas**, alinhado com janela "sem 3-5" do roadmap mas com risco se decisões #1 e #2 demorarem.

---

## 6. Plano Fase 1B — tasks adicionais

> Tudo o que falta entre 1A → 1B (6 dashboards restantes, 11 travas restantes, killchain, deploy prod).

| # | Task | Categoria | Estimativa |
|---|---|---|---|
| 26 | Dashboard "Planejamento de Visita" (entidade ou tipo dedicado de Atividade=Visita; campos planejada/agendada/realizada; geo SP/Estados via `Empresa.estado` e `cidade`) | L | 16-30h |
| 27 | Dashboard "Entrada de Leads" (13 métricas: SLA por origem×sub_tipo, volume, motivos descarte, etapa atual, ICP/leadscore distribuição) | L | 16-25h |
| 28 | Dashboard "Topo de Funil" (Análise Interna, Estimativa, Estimativa em Conversão, Passagem Pré-vendas → Vendas) | M | 10-16h |
| 29 | Dashboard "Meio de Funil" (Projeção, Projeção em Conversão, qtd tarefas, tempo entre atividades) | M | 10-16h |
| 30 | Dashboard "Fundo de Funil" (Desenvolvimento Proposta, Proposta Enviada, qtd tarefas, tempo entre atividades) | M | 10-16h |
| 31 | Dashboard "Tração Técnica" (responsável técnico — depende de #1 ter previsto papel `tecnico`) | M | 8-14h |
| 32 | Dashboard "Meta de Vendas" (Resultado Previsto, Vendas Previstas, Antecipações Previstas/Confirmadas) — depende de entidade Meta + lógica de previsão | L | 16-30h |
| 33 | Dashboard "Resultado Anual" (Medição, Meta Anual, Atingida, Previsão) | M | 8-14h |
| 34 | Travas restantes 11 etapas (Estimativa/EstimativaConversao/Projecao/ProjecaoConversao/DesProposta/PropostaEnviada/AnaliseTecnica/AnaliseComercial/Negociacao/EmissaoPedido/PedidoConvertido) | L | 16-32h |
| 35 | Histórico de campos de trava (audit log: quem preencheu "foi_apresentado=SIM" e quando) — opcional mas pedido implicitamente | M | 8-12h |
| 36 | Webhook Make `USER-MONDAY` para enriquecer leads vindos de canais antigos | M | 6-10h |
| 37 | Migração assistida: 10 users do Comercial 💰 → arv-crm (auth, mapping de papéis, transferência de leads) | L | 12-20h |
| 38 | Killchain Comercial 💰: arquivar/desligar workspace Monday | S | 2-4h |
| 39 | Contrato de eventos de saída (webhooks pra futuros consumers arv-framework, arv-pm) — payload v1, signature, retry | M | 8-12h |
| 40 | Deploy produção `crm.arvsystems.cloud` + GitHub Actions CD para `:prod` tag | M | 4-8h |
| 41 | Backups Postgres automatizados + monitoramento (sentry ou similar) | M | 6-10h |
| 42 | Refinamentos UX pós-feedback piloto (provavelmente 10-20% do total) | L | 12-20h |

**Total Fase 1B: 168-289h** — chute médio **~220h** ≈ **5-7 semanas**.

---

## 7. Bugs e dívida técnica encontrados

- **`data_entrada` ≠ "tempo na etapa".** `dashboard_service.py:89`, `sla_scheduler.py:56`, `KanbanCard.tsx:24`. CRITICAL.
- **`change_stage` não valida campos do COMPLETUDE_MAP**, embora a lógica exista. Inconsistência intencional? Pelo plano da Fase 1A faz sentido virar travas reais.
- **`COMPLETUDE_MAP` cobre 4 etapas (das 5 atuais)**, e os labels não batem com `travas.txt` (ex: trava pede "Telefone fixo" e "Telefone/WhatsApp" como dois campos separados; código une `contato_principal.whatsapp`).
- **`Lead.tipo_entrega` é `String(50)` livre**; `travas.txt` exige valores específicos `"estimativa"`, `"projeção"`. Sem validador.
- **Atividade.tipo string livre.** Mesmo problema.
- **Soft-delete só na empresa e lead**, não em contatos (apesar de existir `Contato.ativo`, o router de contatos faz `contato.ativo = False` sem refresh — `routers/contatos.py:104`).
- **`get_sla_alerts` faz scan linear de todos leads ativos** sem paginação/limite — degrada com 1.875 leads.
- **`run_workers.py` usa `time.sleep` infinito** — não tem `await` adequado para `Ctrl+C`. Funciona mas feio.
- **Migrations rodam no `lifespan` do FastAPI** (`main.py:23`). OK pra dev, mas em multi-replica produção causa race. Aceitável Fase 1A.
- **Sem migration de seed de admin user.** Primeiro registro precisa do `ADMIN_SECRET=arv-admin-setup-2024` (default público no `.env.example`).
- **`JWT_SECRET=change-me-in-production-use-openssl-rand-hex-32`** — flag óbvia para prod, mas precisa garantir que é trocada via env Portainer.
- **Frontend: `KanbanCard.tsx` exibe `lead.responsavel_nome`** mas backend não retorna esse campo no `LeadResponse`. UI sempre fallback para etapa. Bug cosmético.
- **`Sidebar.tsx`** tem link `/dashboard/contatos` mas página é só leitura (sem create). Inconsistente.
- **`requirements.txt` e `package.json` não inspecionados** mas há indicação de Recharts ausente (não vi import). Sem libs de gráfico, dashboards 1A precisam adicionar dependência.
- **Sem testes unitários** no backend; `test_api.py`/`test_api.sh` parecem smoke tests via HTTP do servidor rodando.
- **`schemas/__init__.py` e `models/__init__.py`** não inspecionados; assumi que apenas re-exportam.
- **`responsavel_id` na Empresa** existe mas nunca é setado no `CreateEmpresa` form (não vi).

---

## 8. Decisões pendentes que descobri durante a leitura

1. **Modelagem pré-vendas/vendas:** 2 FKs separadas em `Lead` (`responsavel_pre_vendas_id`, `responsavel_vendas_id`, `responsavel_tecnico_id`) ou tabela `lead_responsabilidade(lead_id, user_id, papel)`?
   - Recomendação implícita pelos requisitos: 3 FKs separadas — mais simples, queries diretas, alinhado com como dashboards descrevem ("por vendedor e pré-vendedor").

2. **Estrutura de etapas:** 15 etapas planas vs hierarquia 2 níveis (fase macro `pre_vendas|handoff|vendas` × etapa)?
   - Recomendação implícita: hierarquia 2 níveis — facilita filtros de dashboard ("oportunidades pré-vendas") e mantém Kanban legível (5 colunas macro + drilldown).

3. **Etapa "Análise Interna":** dashboards.txt menciona, travas.txt NÃO. Alinhar nomenclatura: é "Qualificação de Oportunidade" ou "Análise Interna"? São a mesma coisa?

4. **Meta:** quem cadastra? admin único ou cada user define sua meta individual? Periodicidade (mensal/trimestral)? Granularidade (por etapa? por origem? por user?).

5. **Temperatura:** `dashboards.txt` distingue "temperatura comercial" e "temperatura técnica"; modelo atual tem só `Lead.temperatura`. Adicionar `Lead.temperatura_tecnica` ou usar tabela aparte?

6. **Visita como entidade:** dashboard "Planejamento de Visita" trata visita como conceito de primeira classe (planejada/agendada/realizada). Manter como `Atividade.tipo='Visita'` com sub_status, ou criar tabela `Visita` própria com geo?

7. **Lib de gráficos:** Recharts (mais usado em React), Chart.js, ou Tremor (dashboards prontos)? Decisão impacta tempo de implementação dos dashboards.

8. **15 etapas no Kanban:** caber 15 colunas é ruim de UX. Manter Kanban macro (5 fases) + view de tabela com drill em sub-etapa?

9. **Importer XLSX:** modo de tratamento de duplicatas — sobrescrever, ignorar, criar versão? Logging de discrepâncias.

10. **`Origem.tipo`:** seed tem `passiva | ativa | indicacao` mas SLA config trata só `passiva | ativa`. `indicacao` cai em qual SLA? Decisão de regra.

---

**Fim do gap analysis.**
