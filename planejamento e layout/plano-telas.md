# Plano de Implementação — Telas do CRM ARV Systems
> Design System: Fluke × Monday.com (Inter Tight, paleta almost-black + red accent)
> Formato: HTML standalone por tela, usando tokens do design_system.html
> Gerado em: 2026-03-16

---

## Mapa Completo de Telas

### Navegação (Sidebar fixa)
```
[Logo ARV]
─────────────────
◆ Dashboard
◆ Pipeline
◆ Empresas
◆ Contatos
◆ Propostas & Orçamentos
◆ Visitas
◆ Metas de Vendas
◆ Dashboard de Funil
─────────────────
⚙ Configurações
```

---

## Inventário de Telas (10 telas)

| # | Tela | Arquivo | Prioridade | Complexidade |
|---|---|---|---|---|
| 01 | Sidebar + Layout Shell | `01_layout.html` | P0 | Média |
| 02 | Dashboard (Home) | `02_dashboard.html` | P0 | Alta |
| 03 | Pipeline — Kanban PRÉ VENDAS | `03_pipeline_prevendas.html` | P0 | Alta |
| 04 | Pipeline — Kanban VENDAS | `04_pipeline_vendas.html` | P0 | Alta |
| 05 | Detalhe do Deal (Drawer/Page) | `05_deal_detail.html` | P0 | Alta |
| 06 | Empresas (Lista + Detalhe 360°) | `06_empresas.html` | P1 | Média |
| 07 | Contatos (Lista + Detalhe) | `07_contatos.html` | P1 | Baixa |
| 08 | Propostas & Orçamentos | `08_propostas.html` | P0 | Alta |
| 09 | Visitas (Calendário) | `09_visitas.html` | P1 | Média |
| 10 | Metas de Vendas | `10_metas.html` | P0 | Alta |
| 11 | Dashboard de Funil (Analytics) | `11_dashboard_funil.html` | P0 | Alta |

---

## Detalhamento por Tela

### 01 — Layout Shell (`01_layout.html`)
**Objetivo:** Sidebar de navegação + estrutura de layout reutilizável por todas as telas.

**Componentes:**
- Sidebar fixa esquerda (240px) com logo, menu items, avatar do usuário
- Topbar com breadcrumb + busca global + notificações + perfil
- Área de conteúdo principal (fluid)
- Dark mode toggle (usa `.ds-section.dark`)

**Interações:**
- Menu item ativo com indicador visual (barra lateral vermelha)
- Sidebar colapsável (ícones only) em telas menores
- Busca global com overlay (busca leads, empresas, contatos, oportunidades)

---

### 02 — Dashboard Home (`02_dashboard.html`)
**Objetivo:** Visão executiva do CRM. Primeiro contato do vendedor ao abrir o sistema.

**Seções:**

```
┌─────────────────────────────────────────────────────────┐
│  KPI CARDS (grid-4)                                     │
│  [Leads Novos] [Oport. Abertas] [Valor no Pipe] [Win%] │
├────────────────────────────┬────────────────────────────┤
│  DEALS QUE PRECISAM DE     │  MEU FORECAST MENSAL       │
│  AÇÃO (lista priorizada)   │  (gauge + projeção)        │
│  - Parados > 7 dias        │                            │
│  - Follow-up atrasado      │                            │
│  - Score alto sem ação      │                            │
├────────────────────────────┼────────────────────────────┤
│  ATIVIDADES DO DIA          │  RANKING VENDEDORES        │
│  (timeline vertical)        │  (barras horizontais       │
│  - Reuniões                 │   meta vs real)            │
│  - Follow-ups               │                            │
│  - Visitas agendadas        │                            │
└────────────────────────────┴────────────────────────────┘
```

**Componentes do Design System usados:**
- `.ds-card` para KPI cards com `.badge` de variação (↑12% / ↓5%)
- Grid helpers `.grid-4`, `.grid-2`
- Badges: `.badge-success`, `.badge-warning`, `.badge-error` para status
- Botões: `.btn-ghost` para ações secundárias

**Dados mocados:**
- 47 leads novos (mês), 23 oportunidades abertas, R$ 2.4M no pipe, 34% win rate
- 8 deals precisando ação
- 5 atividades do dia

---

### 03 — Pipeline PRÉ VENDAS (`03_pipeline_prevendas.html`)
**Objetivo:** Kanban visual do funil de pré-vendas. Resolve: task-centric, burocrático.

**Colunas do Kanban:**
```
| Prospecção | Primeiro Contato | Qualificação | Qualificado ✅ | Descartado ❌ |
|    (12)    |       (8)        |     (5)      |      (3)       |     (15)      |
```

**Card do Kanban:**
```
┌──────────────────────┐
│ 🟡 Morno         3d  │  ← temperatura (badge) + dias na etapa
│ Empresa XYZ S.A.     │  ← nome da empresa
│ Automação Industrial │  ← produto de interesse
│ R$ 150.000           │  ← valor estimado
│ ────────────────     │
│ 👤 Mariana    LS: 72 │  ← responsável + lead score
└──────────────────────┘
```

**Interações:**
- Drag & drop entre colunas (com validação de gate)
- Click → abre drawer lateral (Tela 05)
- Header da coluna mostra: contagem + valor total
- Filtros no topo: responsável, temperatura, produto, período
- Toggle para alternar com Tela 04 (VENDAS)

**Sistemas do Excalidraw implementados aqui:**
- **Leadscore** — exibido no card, ordena cards dentro da coluna
- **FUP 3/7/10 dias** — indicador visual no card (ícone de alerta quando atrasado)
- **Enriquecimento de Leads** — botão no card "Enriquecer" (chama API CNPJ)

---

### 04 — Pipeline VENDAS (`04_pipeline_vendas.html`)
**Objetivo:** Kanban do funil de vendas, pós-qualificação.

**Colunas do Kanban:**
```
| Qualif. | Análise  | Dev.     | Proposta | Negociação | Fechamento | Convertido | Perdido |
| Oport.  | Interna  | Proposta | Enviada  |            |            |    🚀      |   ❌    |
|  (4)    |   (3)    |   (5)    |   (7)    |    (4)     |    (2)     |   (12)     |  (8)    |
```

**Card do Kanban (mais rico que pré-vendas):**
```
┌──────────────────────────┐
│ 🔴 Quente          12d   │
│ Empresa ABC Ltda.        │
│ Projeto: Linha Robótica  │
│ R$ 450.000    →  78%     │  ← valor + probabilidade
│ ──────────────────       │
│ 👤 Saulo  📋 2/5 ✅      │  ← resp + checklist da fase
│ ST: 85  SO: 72           │  ← score técnico + oportunidade
└──────────────────────────┘
```

**Sistemas do Excalidraw implementados aqui:**
- **Score Técnico** — exibido no card (ST: XX)
- **Opportunity Score** — exibido no card (SO: XX)
- **Geração de Orçamento/Proposta** — botão de ação no card ("Criar Proposta")
- **Cross & Up Sell** — badge no card quando IA identifica oportunidade

---

### 05 — Detalhe do Deal (`05_deal_detail.html`)
**Objetivo:** Todas as informações do lead/oportunidade em uma interface limpa.

**Layout:**
```
┌─────────────────────────────────────────────────────────────────────┐
│ HEADER                                                              │
│ [← Voltar]  Empresa XYZ  |  R$ 450.000  |  🔴 Quente  |  Vendas   │
│ Etapa: Proposta Enviada ──●────────────●─────○─────○─────○──        │
│                          (progress bar visual do funil)              │
├───────────────────────────────────────────────┬─────────────────────┤
│ TABS                                          │ SIDEBAR DIREITA     │
│                                               │                     │
│ [Resumo] [Empresa] [Contatos] [Atividades]   │ PRÓXIMA AÇÃO        │
│ [Propostas] [Scores] [Histórico]              │ ☐ Enviar proposta   │
│                                               │ ☐ Agendar reunião   │
│ ┌─────────────────────────────────────────┐   │ ☐ Confirmar receipt │
│ │ Conteúdo da tab ativa                   │   │                     │
│ │                                         │   │ CHECKLIST DA FASE   │
│ │ (campos aparecem conforme a fase        │   │ ✅ Comitê aprovado  │
│ │  atual — progressive disclosure)        │   │ ✅ Proposta criada  │
│ │                                         │   │ ☐ Enviada ao client │
│ │                                         │   │ ☐ Confirmou receb.  │
│ │                                         │   │                     │
│ │                                         │   │ SCORES              │
│ │                                         │   │ LS: ████████░░ 72   │
│ │                                         │   │ ST: █████████░ 85   │
│ │                                         │   │ SO: ███████░░░ 68   │
│ └─────────────────────────────────────────┘   │                     │
└───────────────────────────────────────────────┴─────────────────────┘
```

**Tabs detalhadas:**

| Tab | Conteúdo |
|---|---|
| **Resumo** | Campos essenciais da fase atual only. Muda conforme a etapa. |
| **Empresa** | Dados da empresa (CNPJ, segmento, plantas, endereço). Botão "Enriquecer CNPJ". |
| **Contatos** | Lista de contatos vinculados. Add/remove. Nível de influência visual. |
| **Atividades** | Timeline cronológica: chamadas, e-mails, reuniões, notas, follow-ups. Criar nova atividade. |
| **Propostas** | Lista de orçamentos vinculados. Criar nova proposta. Ver valores, revisões, status. |
| **Scores** | 3 gauges visuais (Lead Score, Score Técnico, Score Oportunidade). Botão recalcular. Detalhamento das respostas. |
| **Histórico** | Audit trail: mudanças de etapa, quem, quando, tempo em cada fase. |

---

### 06 — Empresas (`06_empresas.html`)
**Objetivo:** Master data de empresas. Visão 360° da conta.

**Lista:**
- Tabela com colunas: Nome, CNPJ, Segmento, Status, Cidade/UF, Responsável, Valor Total, Última Compra
- Filtros: segmento, status da conta, responsável, estado
- Busca por nome ou CNPJ

**Detalhe 360°:**
```
┌──────────────────────────────────────────────────┐
│ EMPRESA XYZ S.A.    CNPJ: 12.345.678/0001-90    │
│ Cliente Ativo  |  Segmento: Automotivo           │
├──────────────────────────────────────────────────┤
│ [Dados] [Contatos(4)] [Leads(3)] [Oport.(2)]    │
│ [Visitas(8)] [Propostas(5)] [Histórico]          │
│                                                  │
│ ┌───────────────────────────────────────────┐    │
│ │ KPIs da conta:                            │    │
│ │ Valor total comprado: R$ 1.2M             │    │
│ │ Última compra: 15/01/2026                 │    │
│ │ Oportunidades abertas: 2 (R$ 380K)        │    │
│ │ NPS: 8.5                                  │    │
│ └───────────────────────────────────────────┘    │
└──────────────────────────────────────────────────┘
```

---

### 07 — Contatos (`07_contatos.html`)
**Objetivo:** Cadastro e gestão de contatos vinculados a empresas.

- Tabela: Nome, Empresa, Cargo, Departamento, Influência, WhatsApp, E-mail, Ativo
- Filtros: empresa, nível de influência, departamento
- Badge visual: 🔴 Decisor | 🟡 Influenciador | ⚪ Operacional
- Click → detalhe com histórico de interações

---

### 08 — Propostas & Orçamentos (`08_propostas.html`)
**Objetivo:** Gestão centralizada de todas as propostas comerciais. **Tela nova — não existia como board separado.**

**Seções:**

```
┌─────────────────────────────────────────────────────────────────┐
│ HEADER: Propostas & Orçamentos              [+ Nova Proposta]   │
├─────────────────────────────────────────────────────────────────┤
│ FILTROS: Status | Vendedor | Período | Valor min-max            │
├─────────────────────────────────────────────────────────────────┤
│ KPI CARDS (grid-4)                                              │
│ [Propostas    ] [Valor Total   ] [Ticket     ] [Taxa de       ] │
│ [Enviadas: 23 ] [R$ 3.8M       ] [Médio:165K ] [Conversão:34%] │
├─────────────────────────────────────────────────────────────────┤
│ TABELA DE PROPOSTAS                                             │
│                                                                 │
│ # │ Empresa      │ Projeto        │ Valor    │ Rev │ Status    │
│───┼──────────────┼────────────────┼──────────┼─────┼───────────│
│ 1 │ ABC Ltda     │ Linha Robótica │ R$ 450K  │ v3  │ 🟡 Enviad│
│ 2 │ XYZ S.A.     │ Retrofit CLP   │ R$ 180K  │ v1  │ 🟢 Aceita│
│ 3 │ DEF Ind.     │ Automação Pack │ R$ 320K  │ v2  │ 🔴 Recusa│
│ 4 │ GHI Corp     │ Integração     │ R$ 95K   │ v1  │ ⚪ Rascun│
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Detalhe da Proposta (modal ou page):**
```
┌─────────────────────────────────────────────────────────────────┐
│ PROPOSTA #2024-047  |  v3  |  Empresa ABC  |  Oport: Linha Rob │
├────────────────────────────┬────────────────────────────────────┤
│ VALORES                    │ COMPOSIÇÃO DE CUSTOS               │
│                            │                                    │
│ Valor Estimado: R$ 450.000 │ CMV:          R$ 180.000  (40%)   │
│ Valor Final:    R$ 420.000 │ Mão de Obra:  R$  85.000  (19%)   │
│ Antecipação:    R$  84.000 │ Terceiros:    R$  45.000  (10%)   │
│                            │ Custo Fixo:   R$  30.000   (7%)   │
│ IMPOSTOS                   │ Custo Financ: R$  12.000   (3%)   │
│ IR:    R$ 6.300            │ Comissão:     R$  21.000   (5%)   │
│ CSLL:  R$ 3.780            │ Markup:       R$  67.000  (16%)   │
│ ICMS:  R$ 50.400           │                                    │
│ ISS:   R$ 21.000           │ Proposta c/ Imp: R$ 501.480       │
│ PIS:   R$ 6.930            │ Proposta s/ Imp: R$ 420.000       │
│ COFINS:R$ 31.920           │                                    │
├────────────────────────────┼────────────────────────────────────┤
│ TIMELINE                   │ CHECKLIST                          │
│ ● Criada: 01/03            │ ✅ Orçamento interno aprovado     │
│ ● Revisão v2: 05/03        │ ✅ Comitê validou                 │
│ ● Revisão v3: 10/03        │ ✅ Enviada ao cliente             │
│ ● Enviada: 11/03           │ ☐ Cliente confirmou recebimento   │
│ ○ Prazo resposta: 25/03    │ ☐ Análise técnica aprovada        │
└────────────────────────────┴────────────────────────────────────┘
```

---

### 09 — Visitas (`09_visitas.html`)
**Objetivo:** Calendário de visitas com geolocalização.

**Layout:**
```
┌─────────────────────────────────────────────────────────┐
│ HEADER: Visitas          [Mês ▼] [Semana ▼] [Dia ▼]    │
│ FILTROS: Vendedor | Perfil | Status                     │
├─────────────────────────────────────────────────────────┤
│ KPIs: Agendadas(8) | Concluídas(45) | Canceladas(3)    │
├─────────────────────────────────────────────────────────┤
│              MARÇO 2026                                 │
│  Seg   Ter   Qua   Qui   Sex                           │
│  ...   ...   ...   ...   ...                           │
│  16    17    18    19    20                              │
│  ┌──┐  ┌──┐                ┌──┐                        │
│  │NPS│  │PV│                │FUP│                       │
│  │XYZ│  │ABC│               │DEF│                      │
│  └──┘  └──┘                └──┘                        │
│  23    24    25    26    27                              │
│        ┌──┐                                             │
│        │CS│                                             │
│        │GHI│                                            │
│        └──┘                                             │
└─────────────────────────────────────────────────────────┘
```

**Perfis de visita (cores):**
- 🟢 Pré Vendas
- 🟡 FUP de Proposta
- 🔴 NPS
- 🔵 Reativação
- 🟣 Prospecção
- 🟤 Alinhamento Técnico
- 🟠 Cross Sell

---

### 10 — Metas de Vendas (`10_metas.html`)
**Objetivo:** Gestão e acompanhamento de metas comerciais por vendedor, equipe e período.

**Layout:**
```
┌─────────────────────────────────────────────────────────────────┐
│ HEADER: Metas de Vendas          [2026 ▼]  [Mensal|Trimestral] │
├─────────────────────────────────────────────────────────────────┤
│ KPIs GLOBAIS (grid-4)                                           │
│ [Meta Anual    ] [Realizado    ] [Delta       ] [% Atingimento]│
│ [R$ 12.000.000 ] [R$ 3.200.000 ] [-R$ 800.000 ] [   73%      ]│
├─────────────────────────────────────────────────────────────────┤
│ VISÃO POR VENDEDOR                                              │
│                                                                 │
│ Vendedor     │ Meta Mês │ Real    │ %    │ Progresso            │
│──────────────┼──────────┼─────────┼──────┼──────────────────────│
│ 👤 Mariana   │ R$ 200K  │ R$ 180K │ 90%  │ ████████████████░░  │
│ 👤 Saulo     │ R$ 250K  │ R$ 190K │ 76%  │ ████████████████░░░ │
│ 👤 Lilian    │ R$ 180K  │ R$ 210K │ 117% │ ████████████████████│
│ 👤 Santiago  │ R$ 200K  │ R$ 120K │ 60%  │ ████████████░░░░░░░ │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│ GRÁFICO: Meta vs Real (barras agrupadas por mês, Jan-Dez)      │
│                                                                 │
│  R$300K ┤                                                       │
│  R$250K ┤   ██                                                  │
│  R$200K ┤   ██ ░░  ██     ██                                   │
│  R$150K ┤   ██ ░░  ██ ░░  ██ ░░                                │
│  R$100K ┤   ██ ░░  ██ ░░  ██ ░░                                │
│         └───Jan────Fev────Mar────                               │
│             ██ Meta  ░░ Real                                    │
├─────────────────────────────────────────────────────────────────┤
│ VISÃO TRIMESTRAL                                                │
│ Q1: R$ 720K / R$ 900K (80%)  ████████████████░░░░              │
│ Q2: R$ 580K / R$ 900K (64%)  █████████████░░░░░░░              │
│ Q3: —                                                           │
│ Q4: —                                                           │
└─────────────────────────────────────────────────────────────────┘
```

**Funcionalidades:**
- Edição inline de metas mensais por vendedor
- Drill-down: clicar no vendedor → lista de deals que compõem o real
- Filtro por equipe (PME / Médio Porte / Corporativo) e função (AE / AM)
- Indicador de forecast: projeção baseada no pipeline aberto × probabilidade

---

### 11 — Dashboard de Funil / Analytics (`11_dashboard_funil.html`)
**Objetivo:** Análise estratégica do funil. **Tela nova — não existia no Monday.** Resolve: pouco estratégico.

**Layout:**
```
┌─────────────────────────────────────────────────────────────────┐
│ HEADER: Dashboard de Funil    [Pré Vendas|Vendas|Ambos]        │
│ FILTROS: Período | Vendedor | Segmento | Produto               │
├─────────────────────────────────────────────────────────────────┤
│ FUNIL VISUAL (horizontal, com taxas de conversão)               │
│                                                                 │
│ Prospecção ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 120 leads     │
│                          ↓ 65%                                  │
│ Primeiro Contato ━━━━━━━━━━━━━━━━━━━━━━━━━ 78 leads            │
│                          ↓ 42%                                  │
│ Qualificação ━━━━━━━━━━━━━━━━━ 33 leads                        │
│                          ↓ 73%                                  │
│ Qualificado ━━━━━━━━━━━━ 24 leads                              │
│                          ↓ 58%                                  │
│ Proposta Enviada ━━━━━━━ 14 oportunidades                      │
│                          ↓ 50%                                  │
│ Negociação ━━━━━ 7 oportunidades                               │
│                          ↓ 71%                                  │
│ Convertido ━━━ 5 vendas  │  Valor: R$ 1.8M                     │
│                                                                 │
├────────────────────────────┬────────────────────────────────────┤
│ MÉTRICAS DE VELOCIDADE     │ ANÁLISE DE PERDAS                  │
│                            │                                    │
│ Ciclo médio de venda: 47d  │ Motivos de perda (pizza):          │
│ Tempo médio por etapa:     │ ● Preço: 35%                      │
│  • Prospecção: 5d          │ ● Prazo: 22%                      │
│  • Qualificação: 8d        │ ● Concorrência: 18%               │
│  • Dev. Proposta: 12d      │ ● Projeto cancelado: 15%          │
│  • Negociação: 15d         │ ● Outros: 10%                     │
│                            │                                    │
│ Ticket médio: R$ 165K      │                                    │
│ Deals/mês: 4.2             │                                    │
│ Win rate: 34%              │                                    │
├────────────────────────────┼────────────────────────────────────┤
│ TENDÊNCIA MENSAL           │ FORECAST                           │
│ (gráfico de linha)         │                                    │
│                            │ Deals no pipe: 23                  │
│ Leads ───── ╱──            │ Valor ponderado: R$ 1.2M           │
│ Oport. ─── ╱───           │ (valor × probabilidade)            │
│ Vendas ── ╱────           │                                    │
│           J F M A          │ Previsão próx 30d: R$ 380K        │
│                            │ Previsão próx 90d: R$ 1.1M        │
├────────────────────────────┴────────────────────────────────────┤
│ COMPARATIVO POR VENDEDOR                                        │
│                                                                 │
│ Vendedor  │ Leads │ Oport │ Propostas │ Vendas │ Win% │ Ciclo  │
│───────────┼───────┼───────┼───────────┼────────┼──────┼────────│
│ Mariana   │  28   │  12   │     8     │   4    │ 33%  │  42d   │
│ Saulo     │  35   │  15   │    10     │   3    │ 20%  │  55d   │
│ Lilian    │  22   │   9   │     6     │   3    │ 33%  │  38d   │
│ Santiago  │  30   │  11   │     7     │   2    │ 18%  │  62d   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Ordem de Implementação

### Sprint 1 — Fundação + Pipeline (telas 01, 03, 04, 05)
> Entrega: Layout base + os dois kanbans + detalhe do deal
> Justificativa: É o core do CRM. Sem isso nada funciona.

| Ordem | Tela | Estimativa | Dependência |
|---|---|---|---|
| 1.1 | `01_layout.html` — Sidebar + Shell | — | Nenhuma |
| 1.2 | `03_pipeline_prevendas.html` — Kanban Pré Vendas | — | 01 |
| 1.3 | `04_pipeline_vendas.html` — Kanban Vendas | — | 01 |
| 1.4 | `05_deal_detail.html` — Detalhe do Deal | — | 01 |

### Sprint 2 — Financeiro + Estratégia (telas 08, 10, 11)
> Entrega: Propostas, Metas e Dashboard de Funil
> Justificativa: Resolve o "pouco estratégico" e "gestão de orçamentos".

| Ordem | Tela | Estimativa | Dependência |
|---|---|---|---|
| 2.1 | `08_propostas.html` — Propostas & Orçamentos | — | 01 |
| 2.2 | `10_metas.html` — Metas de Vendas | — | 01 |
| 2.3 | `11_dashboard_funil.html` — Dashboard de Funil | — | 01 |

### Sprint 3 — Dashboard + Master Data (telas 02, 06, 07)
> Entrega: Dashboard home, Empresas 360°, Contatos

| Ordem | Tela | Estimativa | Dependência |
|---|---|---|---|
| 3.1 | `02_dashboard.html` — Dashboard Home | — | 01 |
| 3.2 | `06_empresas.html` — Empresas 360° | — | 01 |
| 3.3 | `07_contatos.html` — Contatos | — | 01 |

### Sprint 4 — Visitas (tela 09)
> Entrega: Calendário de visitas

| Ordem | Tela | Estimativa | Dependência |
|---|---|---|---|
| 4.1 | `09_visitas.html` — Calendário de Visitas | — | 01 |

---

## Padrões de Design Compartilhados

### Tokens do Design System (aplicados em todas as telas)

| Token | Valor | Uso |
|---|---|---|
| `--almost-black` | #111111 | Background sidebar, textos primários |
| `--red` / `--color-accent` | #c82a2a | CTAs, alertas, destaques |
| `--whitesmoke` | #f5f5f5 | Background da área de conteúdo |
| `--monday-green` | #00ca72 | Sucesso, deals ganhos, metas batidas |
| `--monday-yellow` | #ffcb00 | Warning, morno, em andamento |
| `--monday-red` | #e44258 | Erro, perdido, atrasado |
| `--monday-blue` | #0073ea | Info, links, ações secundárias |
| `--monday-purple` | #6161ff | Destaques especiais, scores IA |
| Font | Inter Tight | Toda a aplicação |
| Radius | 8px (cards), pill (buttons/badges) | Consistência visual |

### Componentes Reutilizáveis

| Componente | Classes | Usado em |
|---|---|---|
| KPI Card | `.ds-card` + `.badge` | Dashboard, Propostas, Metas, Funil |
| Tabela | custom (zebra, hover) | Empresas, Contatos, Propostas, Metas |
| Kanban Card | custom | Pipeline PV, Pipeline Vendas |
| Badge/Tag | `.badge-*` | Temperatura, status, etapa |
| Formulário | `.ds-input` + `.ds-label` | Deal detail, criar proposta |
| Modal | `.ds-modal-*` | Confirmações, criar item |
| Botões | `.btn-primary`, `.btn-outline`, `.btn-ghost`, `.btn-accent` | Todas |
| Tooltip | `.ds-tooltip-wrap` | Scores, ícones de info |
| Progress Bar | custom | Metas, checklist de fase |

---

## Checklist de Validação (por tela)

Antes de considerar uma tela "pronta", validar contra os 5 problemas:

- [ ] **Não burocrático** — A tela mostra apenas o que é necessário na fase atual?
- [ ] **Centrado em deal/relacionamento** — A informação principal é o deal ou a conta, não a tarefa?
- [ ] **Estratégico** — A tela ajuda a tomar uma decisão ou apenas registra dados?
- [ ] **Sem gambiarra** — A tela funciona com dados do banco, sem precisar de sync externo?
- [ ] **Claro** — Um vendedor novo entenderia o que fazer em 10 segundos?
