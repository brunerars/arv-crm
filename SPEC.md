# arv-crm — SPEC v1.1
> Fonte da verdade do CRM próprio da ARV Systems (substitui Monday Comercial 💰).
> Data: 2026-05-07 · Bruno Constantinou · Status: aprovado 2026-05-08 · Revisado 2026-05-08 (v1.1: §12 chain de migrations corrigida — 3 issues resolvidos durante implementação)

Este documento cruza:
- `arv-crm/` (protótipo FastAPI+Next existente, ~25-30% pronto pela Fase 1A)
- `arv-crm/travas.txt` (15 stage gates)
- `arv-crm/dashboards.txt` (9 dashboards)
- `arv-crm/PIPELINE.xlsx` (1.856 leads × 218 colunas legado)
- `arv-crm/DADOS-VENDAS.xlsx` (417 empresas + 45 concorrentes + tabelas de apoio)
- `discovery/MONDAY-CRM-DEEPDIVE.md` (boards Comercial 💰 + redesign morto MCP CRM)
- `discovery/ARV-CRM-GAP.md` (estado real do protótipo)

---

## 0. Sumário

**Propósito:** definir entidades, estados, validações, dashboards, eventos e plano de migração do CRM próprio da ARV.

**Escopo:** funil completo pré-vendas + vendas + handoff. Pós-venda (Conta/NPS) fica para Fase 2.

**Não-objetivos:** mecanismo de pricing/proposta (vai pro `arv-framework` separado), gestão de projeto pós-venda (vai pro `arv-pm`).

---

## 1. Decisões arquiteturais

| # | Decisão | Justificativa |
|---|---|---|
| 1 | **Lead e Oportunidade como entidades distintas** (não 1 unificada com 15 etapas) | Já desenhado no MCP CRM redesign (`04_LEADS` + `05_OPORTUNIDADES`). Funis com responsabilidades, SLAs e dashboards separados. Conversão explícita facilita auditoria. |
| 2 | **3 papéis** no funil: `pre_vendas`, `vendas`, `tecnico` (+ `admin`) | Pipeline legado tem `Resp. Comercial` + `Resp. Técnico` + `Resp. Próx. Atividade`. Dashboards de Tração/Performance Técnica usam papel técnico como dimensão própria. |
| 3 | **Orçamento como entidade própria com versionamento** (1 Oportunidade : N Orçamentos) | Bug do legado (`Proposta sem Imposto` somava IR/CSLL) tem origem em campos planos. Versionamento + impostos em % evitam recálculo manual. |
| 4 | **Conta = flag `is_cliente` em Empresa** (Fase 1A); refatorar pra entidade `Conta` na Fase 2 | MVP-demo não precisa de NPS/Health/Cross-sell. Marcar empresa como cliente é suficiente para handoff inicial com arv-pm. |
| 5 | **Score híbrido**: ICP é função pura sobre Empresa; Técnico/Oportunidade são questionários com perguntas hardcoded em código + histórico em `ScoringResposta` | ICP usa firmographics (Segmento, Funcionários, Tempo Mercado, Plantas, Distância). Técnico e Oportunidade usam questionários estruturados. Mudar perguntas = 1 PR. |

---

## 2. Modelo de domínio

### 2.1 Entidades canônicas

```
User                — usuário do sistema com role (pre_vendas | vendas | tecnico | admin)
Empresa             — pessoa jurídica (com is_cliente flag)
Contato             — pessoa vinculada a Empresa (1:N, normalizado — substitui 4 contatos planos do legado)
Concorrente         — empresa concorrente catalogada
Origem              — fonte do lead (Ativa/Passiva × Pré-Vendas/Vendas)
Lead                — oportunidade em pré-vendas (5 etapas)
Oportunidade        — oportunidade em vendas (8 etapas) — pode existir SEM lead pai (origem direta vendas)
Orcamento           — versão de proposta financeira de uma Oportunidade (1:N)
Atividade           — ação atômica (email/ligação/reunião/visita/passagem/tarefa) — discriminator por tipo
Visita              — caso especial de Atividade com geo obrigatória (modelada como atividade.tipo=visita_* + campos geo opcionais)
ScoringResposta     — resposta a uma pergunta de score (TECNICO | OPORTUNIDADE)
HistoricoEtapaLead  — audit trail de transições no Lead
HistoricoEtapaOpp   — audit trail de transições na Oportunidade
MetaVendas          — meta de período (mensal/anual) por escopo (global/user/etapa)
```

### 2.2 Relações principais

```
Empresa 1:N Contato
Empresa 1:N Lead              (lead.empresa_id)
Empresa 1:N Oportunidade      (oportunidade.empresa_id)
Lead 1:1 Oportunidade         (oportunidade.lead_id, nullable — vendas direta não tem lead)
Oportunidade 1:N Orcamento    (orcamento.oportunidade_id)
Lead 1:N Atividade            (atividade.lead_id, nullable)
Oportunidade 1:N Atividade    (atividade.oportunidade_id, nullable)
Lead 1:N HistoricoEtapaLead
Oportunidade 1:N HistoricoEtapaOpp
Lead/Oportunidade 1:N ScoringResposta (polymorphic)
Empresa N:1 Origem
User N:M Lead/Oportunidade através de campos: responsavel_pre_vendas_id, responsavel_comercial_id, responsavel_tecnico_id
```

### 2.3 Campos chave por entidade

#### User
```
id, nome, email, hash_senha, role (enum: pre_vendas|vendas|tecnico|admin), ativo, created_at
```

#### Empresa
```
id, razao_social, nome_fantasia, cnpj, segmento_mercado_id, area_atuacao_id,
quantidade_funcionarios, tempo_mercado_anos, n_plantas_industriais, distancia_planta_km,
estado_uf, cidade, cep, endereco_numero, endereco_complemento, telefone_fixo, linkedin,
tipo (cliente | prospect), status (ativo | inativo),
is_cliente (bool, derivado de tipo='cliente'),
icp_score (float, calculado), icp_classificacao (A|B|C, derivado),
observacoes, created_at, updated_at
```

#### Contato
```
id, empresa_id, nome, cargo, departamento, nivel_influencia (decisor|influenciador|usuario|tecnico|sem_info),
telefone_whatsapp, email, linkedin, papel_decisao (texto livre — extraído do legado), created_at
```

#### Concorrente
```
id, cnpj, nome, uf, cidade, qtde_filiais, n_funcionarios_faixa, fundacao_ano,
portfolio, principais_clientes, principais_parceiros, observacoes
```

#### Origem
```
id, tipo (ativa | passiva), sub_tipo (pre_vendas | vendas | NULL — só faz sentido pra ativa),
canal (texto livre: linkedin | site | indicacao | evento | cold_call | etc), descricao
```

#### Lead (etapas pré-vendas)
```
id, empresa_id, responsavel_pre_vendas_id (User),
nome_projeto, descricao_demanda,
etapa (enum 5 valores — ver §3),
origem_id, sub_origem_canal (string),
data_entrada_pre_vendas, data_ultima_atividade,
descartado (bool), motivo_descarte, data_descarte,
data_reativacao, status_reativacao,
created_at, updated_at
```

Campos derivados (não armazenados):
```
proxima_atividade_id (derivado do MIN(atividade.data_prevista) WHERE atividade.lead_id=X AND data_realizacao IS NULL)
tempo_na_etapa (derivado do MAX(historico_etapa_lead.entrou_em) WHERE saiu_em IS NULL)
tempo_desde_ultima_atividade (now - data_ultima_atividade)
```

#### Oportunidade (etapas vendas)
```
id, empresa_id, lead_id (nullable — vendas direta não tem lead pai),
responsavel_comercial_id, responsavel_tecnico_id,
nome_projeto, descricao_demanda, area_atuacao_id, produto, tipo_entrega (estimativa | projecao | proposta),
etapa (enum 8 valores — ver §3),
data_handoff (transferida do lead),
data_ultima_atividade,
descartado (bool), motivo_descarte, data_descarte,
data_reativacao, status_reativacao,
score_tecnico (float), score_oportunidade (float),
temperatura_comercial (frio | morno | quente | NULL), temperatura_tecnica (frio | morno | quente | NULL),
acao_recomendada (string),
chance_conversao_pct (int),
data_prevista_venda, data_conclusao,
nivel_aderencia, nivel_complexidade,
prazo_emissao_pedido, prazo_entrega_cliente, prazo_entrega_arv,
cronograma_inicio, cronograma_fim, data_limite_aprovacao_comite,
passou_por_comite (bool),
visita_alinhamento_tecnico_necessaria (bool),
n_revisao (int),
n_os (string nullable — preenchido após PEDIDO CONVERTIDO),
pasta_projeto_atualizada (bool),
created_at, updated_at
```

#### Orcamento
```
id, oportunidade_id, versao (int, autoincr por oportunidade),
valor_base (decimal), 
custo_fixo, custo_financeiro, comissao_pct, markup_pct, cmv_estimado, custo_terceiros, custo_mao_obra,
ir_pct, csll_pct, icms_pct, iss_pct, pis_pct, cofins_pct,
valor_com_imposto (calc), valor_sem_imposto (calc, sem incluir IR/CSLL — corrigir bug do legado),
antecipacao_confirmada (decimal, nullable), antecipacao_prevista (decimal, nullable),
data_recebimento_antecipacao,
foi_enviado_cliente (bool), data_envio,
cliente_confirmou_recebimento (bool), prazo_avaliacao_tecnica_cliente,
solucao_tecnica_aprovada (bool), prazo_analise_comercial_cliente,
email_enviado_comprador (bool),
condicoes_comerciais_aceitas (bool), cliente_confirmou_intencao_compra (bool),
created_at, updated_at, criado_por_id
```

#### Atividade
```
id, tipo (enum: email | ligacao | reuniao_interna | passagem_bastao | tarefa | tarefa_tecnica | visita_comercial | visita_tecnica | apresentacao_proposta),
lead_id (nullable), oportunidade_id (nullable), empresa_id (nullable, derivado pelo lead/opp),
responsavel_id, criada_por_id,
descricao, data_prevista, data_realizacao,
status (planejada | em_andamento | realizada | cancelada),
resultado (texto), 
-- campos geo opcionais (preenchidos quando tipo é visita_*)
geo_uf, geo_cidade, geo_zona,
created_at, updated_at
```

#### ScoringResposta
```
id, lead_id (nullable), oportunidade_id (nullable),
categoria (TECNICO | OPORTUNIDADE),
pergunta_codigo (string — referencia o catálogo em scoring_catalog.py),
opcao_codigo (string), valor_pontos (float),
respondido_em, respondido_por_id
```

#### HistoricoEtapaLead / HistoricoEtapaOportunidade
```
id, lead_id (ou oportunidade_id), etapa,
entrou_em, saiu_em (nullable — etapa atual tem saiu_em=NULL),
responsavel_no_periodo_id (snapshot)
```

#### MetaVendas
```
id, periodo_inicio (date), periodo_fim (date),
escopo (GLOBAL | USER | ETAPA | ETAPA_USER),
user_id (nullable), etapa (nullable),
quantidade_meta (int, nullable — ex: 40 leads), valor_meta (decimal, nullable — ex: R$568.287)
```

---

## 3. Funil — etapas e transições

### 3.1 Lead — 5 etapas pré-vendas

```
LEAD_INICIAL → ANALISE_INTERNA → QUALIFICACAO_INICIAL → QUALIFICACAO_OPORTUNIDADE → [convertido em Oportunidade]
                                                                                     OU [DESCARTADO]
```

| Etapa | Quem responde | Próxima | Saída |
|---|---|---|---|
| `LEAD_INICIAL` | Pré-Vendas | ANALISE_INTERNA | descartar com motivo |
| `ANALISE_INTERNA` | Pré-Vendas | QUALIFICACAO_INICIAL | descartar |
| `QUALIFICACAO_INICIAL` | Pré-Vendas | QUALIFICACAO_OPORTUNIDADE | descartar |
| `QUALIFICACAO_OPORTUNIDADE` | Pré-Vendas | converte em Oportunidade (handoff) | descartar |

**Conversão Lead → Oportunidade** (handoff):
```python
def converter_para_oportunidade(lead, responsavel_comercial_id, responsavel_tecnico_id) -> Oportunidade:
    """
    Pré-condição: lead.etapa == QUALIFICACAO_OPORTUNIDADE e travas validadas
    Cria Oportunidade vinculada (lead_id=lead.id), copia campos relevantes,
    fecha histórico do lead, abre histórico da oportunidade em ESTIMATIVA.
    """
```

### 3.2 Oportunidade — 8 etapas vendas

```
ESTIMATIVA → ESTIMATIVA_EM_CONVERSAO → PROJECAO_ORCAMENTARIA → PROJECAO_EM_CONVERSAO →
DESENVOLVIMENTO_PROPOSTA → PROPOSTA_ENVIADA → PROPOSTA_EM_ANALISE → PROPOSTA_EM_NEGOCIACAO →
[EMISSAO_PEDIDO → CONVERTIDA_EM_VENDA] OU [DESCARTADA]
```

Detalhamento:

| Etapa | Quem responde | Próxima(s) |
|---|---|---|
| `ESTIMATIVA` | Vendas/Técnico | ESTIMATIVA_EM_CONVERSAO |
| `ESTIMATIVA_EM_CONVERSAO` | Vendas | PROJECAO_ORCAMENTARIA OU descartar |
| `PROJECAO_ORCAMENTARIA` | Vendas/Técnico | PROJECAO_EM_CONVERSAO |
| `PROJECAO_EM_CONVERSAO` | Vendas | DESENVOLVIMENTO_PROPOSTA OU descartar |
| `DESENVOLVIMENTO_PROPOSTA` | Vendas/Técnico (gera ticket no `arv-framework`) | PROPOSTA_ENVIADA |
| `PROPOSTA_ENVIADA` | Vendas | PROPOSTA_EM_ANALISE_TECNICA |
| `PROPOSTA_EM_ANALISE_TECNICA` | Vendas/Técnico | PROPOSTA_EM_ANALISE_COMERCIAL OU descartar |
| `PROPOSTA_EM_ANALISE_COMERCIAL` | Vendas | PROPOSTA_EM_NEGOCIACAO OU descartar |
| `PROPOSTA_EM_NEGOCIACAO` | Vendas | EMISSAO_PEDIDO OU descartar |
| `EMISSAO_PEDIDO` | Vendas | CONVERTIDA_EM_VENDA OU descartar |
| `CONVERTIDA_EM_VENDA` | (terminal) | dispara evento `OPPORTUNITY_WON` para arv-pm |

(Total: 11 etapas + 2 terminais. O `travas.txt` lista 15 etapas considerando ANALISE_INTERNA + LEAD_INICIAL + DESCARTADO. Mantive o nome canônico em PT-PT-PT-BR.)

### 3.3 Descarte

Descarte é flag (`descartado=True`) + `motivo_descarte` + `data_descarte`, **não etapa terminal**. Permite reativação posterior (`data_reativacao`, `status_reativacao`). Descartar a partir de qualquer etapa.

---

## 4. Travas (stage gates)

Validação no backend antes de qualquer transição. Hardcoded em `backend/services/stage_validators.py` como dict `etapa → lista de regras`.

### 4.1 Travas do Lead

| Saindo de | Campos obrigatórios |
|---|---|
| `LEAD_INICIAL` | empresa.razao_social, empresa.cnpj, contato#1.nome, contato#1.telefone OU email, origem_id, sub_origem_canal |
| `ANALISE_INTERNA` | (sem regras explícitas no `travas.txt` — apenas registrar entrou em `analise_interna`) |
| `QUALIFICACAO_INICIAL` | empresa.segmento_mercado_id, empresa.tempo_mercado_anos, empresa.distancia_planta_km, empresa.icp_score (calculado), empresa.icp_classificacao |
| `QUALIFICACAO_OPORTUNIDADE` | produto, area_atuacao_id |

### 4.2 Travas da Oportunidade

| Saindo de | Campos obrigatórios |
|---|---|
| `ESTIMATIVA` | tipo_entrega='estimativa', score_oportunidade (score_oportunidade não nulo) |
| `ESTIMATIVA_EM_CONVERSAO` | foi_enviado_cliente=True, data_envio NOT NULL |
| `PROJECAO_ORCAMENTARIA` | tipo_entrega='projecao' |
| `PROJECAO_EM_CONVERSAO` | dentro_faixa_investimento=True (campo no Orcamento ou na Oportunidade), aprovado_pelo_comite=True |
| `DESENVOLVIMENTO_PROPOSTA` | data_reuniao_passagem_bastao NOT NULL, temos_todas_info_tecnicas=True, temos_todas_info_comerciais=True |
| `PROPOSTA_ENVIADA` | orcamento.versao mais recente preenchido completo (todos os campos de meta de vendas) |
| `PROPOSTA_EM_ANALISE_TECNICA` | proposta_enviada_cliente=True, cliente_confirmou_recebimento=True, prazo_avaliacao_tecnica_cliente NOT NULL |
| `PROPOSTA_EM_ANALISE_COMERCIAL` | apresentacao_proposta_realizada=True (atividade type=apresentacao_proposta com data_realizacao), solucao_tecnica_aprovada_cliente=True, prazo_analise_comercial_cliente NOT NULL, email_enviado_comprador=True |
| `PROPOSTA_EM_NEGOCIACAO` | prazo_retorno_negociacao NOT NULL, valor_dentro_expectativa=True, visita_comercial_realizada=True (Atividade type=visita_comercial com data_realizacao) |
| `EMISSAO_PEDIDO` | condicoes_comerciais_aceitas=True, cliente_confirmou_intencao_compra=True, prazo_emissao_pedido NOT NULL, atendemos_prazo_cliente=True |
| `CONVERTIDA_EM_VENDA` | pedido_compra_recebido=True, pedido_compra_conferido=True, pasta_projeto_atualizada=True, n_os NOT NULL |
| `DESCARTAR` (qualquer etapa) | motivo_descarte NOT NULL |

**Implementação:**
```python
# stage_validators.py
LEAD_TRANSITION_RULES = {
    "LEAD_INICIAL": ["empresa.razao_social", "empresa.cnpj", "contato.nome", "contato.tel_OR_email", "origem_id", "sub_origem_canal"],
    ...
}

def validate_transition(entity, target_stage) -> ValidationResult:
    rules = TRANSITION_RULES.get(entity.etapa)
    missing = [r for r in rules if not _check_rule(entity, r)]
    return ValidationResult(ok=not missing, missing=missing)
```

---

## 5. Score

### 5.1 ICP — função pura sobre Empresa

```python
# backend/services/icp_calculator.py
def calcular_icp(empresa: Empresa) -> tuple[float, str]:
    """
    Score 0-10 baseado em firmographics:
    - Segmento de Mercado (peso 30%)
    - Quantidade de Funcionários (peso 20%)
    - Tempo no Mercado (peso 15%)
    - Nº Plantas Industriais (peso 15%)
    - Distância da Planta (peso 20%)
    
    Classificação:
    - A (Ideal): score >= 7.5
    - B (Aceitável): 5.0 <= score < 7.5
    - C (Marginal): score < 5.0
    """
```

Recalculado sempre que `Empresa` é atualizada (event listener SQLAlchemy).

### 5.2 Score Técnico e Score Oportunidade — questionários hardcoded

```python
# backend/services/scoring_catalog.py
PERGUNTAS_TECNICO = [
    {"codigo": "TECN_PROJ_SEMELHANTE", "texto": "A ARV já realizou um projeto semelhante em escopo e tecnologia?",
     "peso": 1.5, "opcoes": [
        {"codigo": "PROJ_IDENTICO", "texto": "Sim, projeto idêntico", "valor": 10},
        {"codigo": "PROJ_PARECIDO", "texto": "Parecido", "valor": 7},
        {"codigo": "PROJ_DIFERENTE", "texto": "Diferente", "valor": 3},
        {"codigo": "PROJ_NUNCA", "texto": "Nunca", "valor": 0},
     ]},
    {"codigo": "TECN_DOMINIO_ARV", "texto": "Este projeto está dentro do domínio técnico com provas sociais da ARV?", ...},
    {"codigo": "TECN_RISCO", "texto": "Qual o grau de risco técnico e operacional do projeto?", ...},
    {"codigo": "TECN_INFO_CLIENTE", "texto": "Quão completas e úteis são as informações fornecidas pelo cliente?", ...},
    {"codigo": "TECN_COMPLEXIDADE", "texto": "Qual o grau de complexidade técnica do projeto?", ...},
    {"codigo": "TECN_VIABILIDADE", "texto": "O projeto é tecnicamente viável com as tecnologias e know-how disponíveis?", ...},
    {"codigo": "TECN_RETROFIT_OU_NOVA", "texto": "O projeto envolve retrofit ou é uma solução nova?", ...},
    {"codigo": "TECN_PODE_ADIAR", "texto": "O cliente pode adiar ou não realizar este projeto sem impactos críticos?", ...},
    {"codigo": "TECN_DOMINA_TECH", "texto": "A ARV domina as tecnologias envolvidas neste projeto?", ...},
]

PERGUNTAS_OPORTUNIDADE = [
    {"codigo": "OPP_PROJETO_ACONTECE", "texto": "Existe chance do projeto não acontecer?", "peso": 2.0, "opcoes": [...]},
    {"codigo": "OPP_CAPEX_APROVADO", "texto": "Tem Capex aprovado para este projeto?", ...},
    {"codigo": "OPP_VALOR_ESTIMADO", "texto": "Existe valor estimado ou teto de investimento?", ...},
    {"codigo": "OPP_RESULTADOS_ESPERADOS", "texto": "Quais resultados esperados?", ...},
    {"codigo": "OPP_PAYBACK", "texto": "Payback esperado pelo cliente?", ...},
    {"codigo": "OPP_DOC_TECNICA", "texto": "Possui caderno de encargos/documentação técnica?", ...},
    {"codigo": "OPP_PAPEL_CONTATO", "texto": "Papel do contato na decisão do projeto?", ...},
    {"codigo": "OPP_JA_COMPROU_ARV", "texto": "Já comprou com a ARV?", ...},
]

def calcular_score(categoria: str, respostas: list[ScoringResposta]) -> float:
    catalogo = PERGUNTAS_TECNICO if categoria == "TECNICO" else PERGUNTAS_OPORTUNIDADE
    soma_ponderada = sum(r.valor_pontos * pergunta.peso for r in respostas para pergunta correspondente)
    soma_pesos = sum(pergunta.peso for pergunta no catalogo respondida)
    return soma_ponderada / soma_pesos  # média ponderada 0-10
```

Persistência: `ScoringResposta` guarda cada resposta com `pergunta_codigo` + `opcao_codigo` + `valor_pontos`. Lead/Oportunidade guarda apenas `score_*` agregado (recalculado a cada nova resposta).

**Mudar pergunta:** edita `scoring_catalog.py`, faz PR, deploy. Não migra dados antigos (respostas antigas continuam com `pergunta_codigo` válido — basta marcar versão deprecated se for o caso).

---

## 6. SLAs (matriz origem × etapa)

Configuração em `backend/sla_config.py` (já existe — refatorar). Estrutura `(etapa, origem_tipo, origem_sub_tipo) → dias_uteis`.

### Lead — pré-vendas

| Etapa | Passiva | Ativa Vendas | Ativa Pré-Vendas |
|---|---|---|---|
| `LEAD_INICIAL` | 3d | 15d | 7d |
| `ANALISE_INTERNA` | 5d (todos) | 5d | 5d |
| `QUALIFICACAO_INICIAL` | 7d | 30d | 20d |
| `QUALIFICACAO_OPORTUNIDADE` | 15d (todos) | 15d | 15d |
| `Passagem Pré-vendas → Vendas` (handoff) | 7d (todos) | 7d | 7d |

### Oportunidade — vendas

| Etapa | Dias úteis (todos os origens) |
|---|---|
| `ESTIMATIVA` | 5d |
| `ESTIMATIVA_EM_CONVERSAO` | 20d |
| `PROJECAO_ORCAMENTARIA` | 15d |
| `PROJECAO_EM_CONVERSAO` | 30d |
| `DESENVOLVIMENTO_PROPOSTA` | 15d |
| `PROPOSTA_ENVIADA` | 3d |
| `PROPOSTA_EM_ANALISE_TECNICA` | (depende prazo cliente) |
| `PROPOSTA_EM_ANALISE_COMERCIAL` | (depende prazo cliente) |
| `PROPOSTA_EM_NEGOCIACAO` | (depende prazo cliente) |

`sla_scheduler.py` (worker APScheduler) varre Leads e Oportunidades, calcula `tempo_na_etapa` a partir do **último `HistoricoEtapaLead/Opp` com `saiu_em IS NULL`** (corrigir bug atual que usa `data_entrada` da entidade), compara com SLA, dispara alertas.

---

## 7. Atividades, Visitas e Origens

### 7.1 Tipos de Atividade

```python
class TipoAtividade(str, Enum):
    EMAIL = "email"
    LIGACAO = "ligacao"
    REUNIAO_INTERNA = "reuniao_interna"
    PASSAGEM_BASTAO = "passagem_bastao"  # cerimônia formal pré-vendas → vendas
    TAREFA = "tarefa"  # tarefa genérica de comercial
    TAREFA_TECNICA = "tarefa_tecnica"  # tarefa do técnico
    VISITA_COMERCIAL = "visita_comercial"  # com geo
    VISITA_TECNICA = "visita_tecnica"  # com geo
    APRESENTACAO_PROPOSTA = "apresentacao_proposta"  # tipo específico — usado em trava
```

### 7.2 Visita

Visita = `Atividade` com `tipo IN (visita_comercial, visita_tecnica)` + campos geo preenchidos:
- `geo_uf` (CharField 2 — `SP`, `MG`, `RS`, etc)
- `geo_cidade` (string)
- `geo_zona` (string — usado para "Zonas SP", livre, ex: "Zona Leste", "Zona Sul")

Status da visita: usa o campo padrão `status` (planejada → em_andamento → realizada → cancelada). Dashboards "Visitas Planejadas/Agendadas/Realizadas" filtram por esse status.

### 7.3 Origem

```
Origem.tipo: ATIVA | PASSIVA
Origem.sub_tipo: PRE_VENDAS | VENDAS | NULL
   - se tipo=ATIVA: sub_tipo é obrigatório
   - se tipo=PASSIVA: sub_tipo=NULL (Passiva não tem sub-tipo papel)
Lead.sub_origem_canal: string livre (linkedin | site | indicacao | evento | cold_call | feira | publicidade | etc)
```

Tabela `Origem` é semente fixa (3 ou 4 linhas). Sub-origem é livre por enquanto — virar enum na Fase 1B se time pedir consistência.

---

## 8. Dashboards (9)

### 8.1 Priorização

| Dashboard | Fase | Justificativa |
|---|---|---|
| **Saúde do Funil** | **1A** | Dashboard executivo — mostra para quem aprovou o sistema |
| **Tração e Performance Pré-Vendas e Vendas** | **1A** | Dimensão de papel — valida arquitetura 3 papéis |
| **Check-in** | **1A** | Operacional — vai pegar quem usa o dia-a-dia |
| Tração e Performance Técnica | 1B | Dimensão técnica — adicionada após validar comercial |
| Entrada de Leads | 1B | Topo de funil detalhado |
| Topo de Funil | 1B | SLAs etapas iniciais |
| Meio de Funil | 1B | SLAs etapas intermediárias |
| Fundo de Funil | 1B | SLAs etapas finais |
| Planejamento de Visita | 1B | Geo + agenda |
| Meta de Venda (Previsão) | 1B | Forecasting |
| Resultado Anual | 1B | Card executivo (1 query) |

### 8.2 Endpoints e queries

Rota base: `GET /api/dashboard/<nome>` com query params `?periodo=mes_atual|mes_anterior|ano|custom&start=...&end=...&user_id=...`.

Cada dashboard com endpoint específico, retornando JSON estruturado por widget.

#### Exemplo — `/api/dashboard/saude-funil`

```json
{
  "entradas_no_mes_por_etapa": {
    "lead_inicial": {"valor": 47, "meta": 300},
    "analise_interna": {"valor": 12, "meta": 80},
    ...
  },
  "volume_atual_por_etapa": [...],
  "temperatura": {
    "comercial": {"frio": 12, "morno": 23, "quente": 8},
    "tecnica": {...}
  },
  "por_responsavel_comercial": [...],
  "por_origem": [...]
}
```

#### Exemplo — `/api/dashboard/check-in`

```json
{
  "tarefas_concluidas_por_usuario_mes": [{"user": "David", "qtd": 47}, ...],
  "tarefas_atrasadas_por_usuario": [...],
  "tarefas_concluir_essa_semana": [...],
  "leads_sem_atividade_por_responsavel": [...],
  "leads_sem_proxima_atividade_por_responsavel": [...],
  "leads_reuniao_interna_essa_semana": [...],
  "planejamento_trabalho_diario_por_usuario": [...]
}
```

(Detalhamento dos 9 dashboards: ver `dashboards.txt`. Implementar 1A primeiro, validar com time, depois 1B.)

---

## 9. Eventos de saída (webhooks)

Contrato definido na Fase 1B, **mas o schema do payload pode ser definido agora** para evitar reescrita.

### 9.1 Eventos

| Evento | Quando dispara | Consumer principal |
|---|---|---|
| `LEAD_CREATED` | Lead criado | (interno — analytics) |
| `LEAD_QUALIFIED` | Lead saiu de QUALIFICACAO_OPORTUNIDADE | (interno) |
| `OPPORTUNITY_CREATED` | Oportunidade criada (via handoff de lead OU venda direta) | (interno) |
| `OPPORTUNITY_PROPOSAL_REQUESTED` | Oportunidade entrou em DESENVOLVIMENTO_PROPOSTA | **arv-framework** — abre ticket para selecionar cards |
| `PROPOSAL_GENERATED` | (recebido do arv-framework) PDF + BOM gerados | (interno — anexa à oportunidade) |
| `OPPORTUNITY_WON` | Oportunidade entrou em CONVERTIDA_EM_VENDA | **arv-pm** — cria projeto com OS, herda cards selecionados |
| `OPPORTUNITY_LOST` | Oportunidade descartada | (interno — analytics) |

### 9.2 Payload base

```json
{
  "event": "OPPORTUNITY_PROPOSAL_REQUESTED",
  "version": "1.0",
  "occurred_at": "2026-05-07T14:32:11Z",
  "data": {
    "oportunidade_id": 123,
    "lead_id": 89,
    "empresa": {"id": 5, "razao_social": "...", "cnpj": "..."},
    "responsavel_comercial": {"id": 12, "nome": "..."},
    "responsavel_tecnico": {"id": 18, "nome": "..."},
    "produto": "...",
    "area_atuacao": "...",
    "valor_estimado": 850000.00
  }
}
```

### 9.3 Implementação

`backend/services/event_publisher.py` — função `publish(event, payload)`. Para Fase 1A pode ser apenas log + tabela `EventLog`. Para Fase 1B, HTTP POST para URLs configuradas em `EVENT_SUBSCRIBERS_URL` (env). Redis pub/sub se ficar pesado depois.

---

## 10. Permissões por papel

Modelo simples no MVP. Refatorar para RLS na Fase 2 se precisar.

| Recurso | admin | pre_vendas | vendas | tecnico |
|---|---|---|---|---|
| Lead — CRUD | ✅ | ✅ (responsavel_pre_vendas_id=self ou nulo) | 👁️ ler todos | 👁️ ler todos |
| Oportunidade — CRUD | ✅ | 👁️ ler (descendentes de seus leads) | ✅ (responsavel_comercial_id=self) | ✏️ atualizar campos técnicos (responsavel_tecnico_id=self) |
| Empresa, Contato — CRUD | ✅ | ✅ | ✅ | 👁️ |
| Concorrente — CRUD | ✅ | ✏️ | ✏️ | 👁️ |
| Atividade — CRUD | ✅ | ✅ (das suas) | ✅ (das suas) | ✅ (das suas) |
| Orcamento — CRUD | ✅ | 👁️ | ✅ | 👁️ |
| ScoringResposta TECNICO | ✅ | 👁️ | 👁️ | ✅ |
| ScoringResposta OPORTUNIDADE | ✅ | ✏️ (até handoff) | ✅ | 👁️ |
| Dashboards | ✅ todos | dashboards de sua etapa | dashboards de venda | dashboards técnicos |
| MetaVendas — CRUD | ✅ | 👁️ | 👁️ | 👁️ |

---

## 11. Plano de migração

> **Decisão (2026-05-08):** NÃO migrar histórico de Pipeline (1.856 leads históricos descartados). Importar apenas:
> 1. **Tabelas de referência** (Empresas + Concorrentes + Tabelas de Apoio) — uma vez, ETL simples
> 2. **WIP — oportunidades em curso** (leads e oportunidades NÃO fechadas/ganhas/perdidas no Pipeline atual) — migração cirúrgica, escopo a definir no momento do go-live
>
> Justificativa: histórico congela no Monday read-only; arv-crm começa "limpo" só com o que está vivo.

### 11.1 Fontes de dados (escopo reduzido)

| Fonte | Conteúdo | Destino | Quando migrar |
|---|---|---|---|
| `DADOS-VENDAS.xlsx` sheet "Cadastro de Empresas" | 417 empresas | `empresa` | Pré-go-live (seed) |
| `DADOS-VENDAS.xlsx` sheet "Cadastro de Concorrentes" | 45 concorrentes | `concorrente` | Pré-go-live (seed) |
| `DADOS-VENDAS.xlsx` sheet "Tabelas de Apoio" | listas de referência | seeds (segmentos, áreas, estados, status) | Pré-go-live (seed) |
| Monday `Comercial 💰` Pipeline — **só WIP** (filtro: etapa ≠ Convertida em Venda ∧ ≠ Descartado ∧ ≠ Perdida) | leads/oportunidades vivas | `lead`, `oportunidade`, `contato`, `atividade`, `orcamento`, `historico_etapa_*`, `scoring_resposta` | No go-live, snapshot |
| Histórico Pipeline (oportunidades fechadas/perdidas/descartadas) | 1.856 linhas legado | **NÃO MIGRA** — Monday vira read-only de consulta | nunca |

### 11.2 Mapeamento WIP → entidades

Mapping linha-a-linha das 218 colunas **dispensado** (Bruno aprovou em 2026-05-08). Quando go-live se aproximar:

1. Filtrar Pipeline por etapas ativas (~5-15% das 1.856 = ~90-280 linhas WIP estimadas)
2. Para esse subconjunto, mapping é direto: identificar `empresa`, `lead` ou `oportunidade`, último `orcamento`, próxima `atividade`, scoring atual
3. Implementar `backend/scripts/import_monday_wip.py` idempotente (natural key: `monday_lead_id`)

Resumo dos blocos relevantes para WIP (detalhado em `discovery/MONDAY-CRM-DEEPDIVE.md` §3.A):

| Bloco do Pipeline | → Entidade arv-crm |
|---|---|
| Identificação + Endereço + Firmographic | `empresa` (deduplica por CNPJ) |
| 4 Contatos planos | `contato` (1:N) — descartar "Sem Informação" |
| Etapa do Pipeline | distribui entre `lead.etapa` e `oportunidade.etapa` |
| Resp. Comercial, Resp. Técnico, Resp. Próx. Atividade | responsáveis em `lead`/`oportunidade` |
| Próx. Atividade + Data | nova `atividade` data_prevista |
| BANT/MEDDIC v2 (cols 170-177) | `scoring_resposta` categoria=OPORTUNIDADE |
| Score Técnico (cols 182-190) | `scoring_resposta` categoria=TECNICO |
| Custos + Impostos (% convertido) + Valor Estimado/Final | `orcamento` (1 versão importada) |
| Travas booleanas (~22 cols) | campos correspondentes em `oportunidade`/`orcamento` |
| Temperatura, Ação recomendada, Motivo Descarte | `oportunidade.*` |
| Datas "Entrou em X" + sheet "tempo na etapa" | `historico_etapa_*` |
| BANT/MEDDIC v1, contadores, monday Doc v2, anexos | **DESCARTAR** |

### 11.3 Estratégia ETL (escopo WIP)

```
Etapa 0: snapshot Monday no momento do go-live (Pipeline + Calendário Visitas)
Etapa 1: filtrar WIP (etapa ativa, ≠ ganha/perdida/descartada)
Etapa 2: seed Empresa (do Cadastro de Empresas, dedup por CNPJ)
Etapa 3: seed Concorrente (do Cadastro de Concorrentes)
Etapa 4: para cada linha WIP: criar/anexar Empresa → Contatos → Lead OU Oportunidade
Etapa 5: para WIP em Oportunidade: criar 1 Orcamento v1 com valores atuais
Etapa 6: para WIP com BANT v2/Score Técnico preenchido: criar ScoringResposta
Etapa 7: criar Atividade aberta para "Próx. Atividade"
Etapa 8: validação — count WIP origem == count destino, FKs ok, scores recalculados
```

Implementar como `backend/scripts/import_monday_wip.py` idempotente (re-rodar sem duplicar via `monday_lead_id`).

### 11.4 Pendência

- **Definir corte de WIP no go-live:** quais etapas exatas contam como "em curso". Provavelmente todas exceto `Convertida em Venda`, `Descartado`, `Perdida`. Confirmar quando estimar Fase 1B.

---

## 12. Schema DB — migrations necessárias

Estado atual: 4 migrations aplicadas (`001_initial_users`, `002_empresas_contatos_origens`, `003_leads_atividades_historico_scoring`, `004_add_ativo_fields`).

### Migrations novas necessárias para Fase 1A

> **Revisão v1.1 (2026-05-08):** corrige 3 issues identificados durante implementação:
> - Issue 1: SPEC v1 listava ordem que punha `008` (FK em oportunidade) antes da `006` (criar tabela) — fisicamente impossível
> - Issue 2: SPEC §2.3 declarava schema canônico de Empresa/Contato/Origem mas não havia migration cobrindo o drift entre `models/` atual e §2.3
> - Issue 3: `historico_etapa` antigo é estruturalmente incompatível com SPEC §3 — em dev (sem prod) DROP+CREATE é correto
>
> Chain reescrita: 15 migrations linear (005→019), com criação de tabelas novas COMPLETAS (não fragmentadas em "cria tabela" + "adiciona FK" + "adiciona campo").

#### Macro A — alignment do schema existente (Empresa/Contato/Origem + tabelas de referência)

| # | Migration | Conteúdo |
|---|---|---|
| 005 | `005_user_role_papeis_funil` | Estende `User.role` para `pre_vendas \| vendas \| tecnico \| admin` |
| 006 | `006_tabelas_referencia` | Novas tabelas: `segmento_mercado`, `area_atuacao`, `tipo_empresa`, `status_orcamento`, `equipe_comercial`. Seeds populam de `DADOS-VENDAS.xlsx` sheet "Tabelas de Apoio" (script separado pós-migrations) |
| 007 | `007_empresa_alignment` | Refactor `empresa`: renomeia `segmento` → FK `segmento_mercado_id`, `num_funcionarios` (str) → `quantidade_funcionarios` (int), `num_plantas` → `n_plantas_industriais`, `distancia_arv_km` → `distancia_planta_km`, `estado` → `estado_uf`. Adiciona: `area_atuacao_id` (FK), `tempo_mercado_anos` (int), `endereco_numero`, `endereco_complemento`, `telefone_fixo`, `linkedin`, `tipo_id` (FK), `is_cliente` (bool), `icp_score` (numeric), `icp_classificacao` (enum A\|B\|C) |
| 008 | `008_contato_alignment` | Refactor `contato`: substitui enum `nivel_influencia` (novos valores), adiciona `papel_decisao`, renomeia `whatsapp` → `telefone_whatsapp` |
| 009 | `009_origem_alignment` | Adiciona `canal` em `origem` (3ª dimensão de classificação: ATIVA/PASSIVA × PRE_VENDAS/VENDAS × CANAL) |

#### Macro B — novas entidades (criadas completas, sem fragmentação)

| # | Migration | Conteúdo |
|---|---|---|
| 010 | `010_concorrente` | Nova tabela `concorrente` (CNPJ, UF, portfolio, clientes, parceiros) |
| 011 | `011_oportunidade` | Nova tabela `oportunidade` **completa**: enum etapa (8 valores), `responsavel_comercial_id` + `responsavel_tecnico_id` (FKs), `temperatura_comercial`, `temperatura_tecnica`, `passou_por_comite`, `n_os`, `pasta_projeto_atualizada`, `motivo_descarte`, `acao_recomendada`, `lead_id` (FK opcional pra Lead pai). Cria já com TODOS os campos de §2.3 — não há migrations posteriores em `oportunidade` |
| 012 | `012_orcamento` | Nova tabela `orcamento` com versionamento (`versao` int), impostos em % (não R$): `ir_pct`, `csll_pct`, `icms_pct`, `iss_pct`, `pis_pct`, `cofins_pct`. Campos: custos detalhados (fixo, financeiro, comissão, markup, cmv, terceiros, mão_obra), valor_base, valor_final, antecipações, FK `oportunidade_id` |
| 013 | `013_meta_vendas` | Nova tabela `meta_vendas` (substitui meta hardcoded em fórmula Monday) |
| 014 | `014_event_log` | Tabela `event_log` para rastreabilidade de eventos de saída/entrada |

#### Macro C — alterações em entidades existentes

| # | Migration | Conteúdo |
|---|---|---|
| 015 | `015_lead_etapas_e_alignment` | Refactor `lead`: renomeia `responsavel_id` → `responsavel_pre_vendas_id`, substitui enum `etapa` (5 valores SPEC §3.1), adiciona `passou_por_comite`, `motivo_descarte`, `data_reativacao`, `status_reativacao`. Mapeia valores antigos pros novos. |
| 016 | `016_atividade_geo_e_tipos` | Estende enum `tipo` (passagem_bastao, visita_comercial, visita_tecnica, apresentacao_proposta, tarefa_tecnica) + campos geo (latitude, longitude, endereco_visita) |
| 017 | `017_scoring_categoria` | Adiciona `categoria` em `scoring_resposta` (`TECNICO \| OPORTUNIDADE`) + índices |

#### Macro D — schema breaking + fix

| # | Migration | Conteúdo |
|---|---|---|
| 018 | `018_historico_etapa_split_recreate` | **DROP** `historico_etapa` antigo (`etapa_anterior`, `etapa_nova`, `tempo_na_etapa_segundos`, `created_at` — incompatível com SPEC §3) **CREATE** `historico_etapa_lead` (`lead_id`, `etapa`, `entrou_em`, `saiu_em`, `responsavel_no_periodo_id`) + `historico_etapa_oportunidade` (idem para `oportunidade_id`). Justificativa: dev sem prod, sem dados reais — DROP+CREATE > migração de dados que seria custosa e descartável. |
| 019 | `019_fix_data_entrada_para_historico` | **CORREÇÃO DE BUG** — substitui usos de `lead.data_entrada` (campo plano que era usado como "tempo na etapa atual") por consulta a `historico_etapa_lead.entrou_em` da etapa atual. Aplicado nos services de tempo na etapa, dashboards e SLAs. |

**Ordem de execução: linear 005 → 006 → 007 → 008 → 009 → 010 → 011 → 012 → 013 → 014 → 015 → 016 → 017 → 018 → 019.** Nenhuma migration depende de algo que vem depois.

**Seeds pós-migrations (script `backend/scripts/seed_referencias.py`):**
- `segmento_mercado` ← DADOS-VENDAS.xlsx sheet "Segmentos de Mercado"
- `area_atuacao` ← idem sheet "Áreas de Atuação ARV"
- `tipo_empresa` ← idem sheet "Tipo de Empresa"
- `status_orcamento` ← idem sheet "Status de Orçamento"
- `equipe_comercial` ← idem sheet "Equipe Comercial"

---

## 13. Próximos passos

### 13.1 O que falta antes de codar

1. ✅ Decisões 1B + 2B + 3B + 4B + 5B confirmadas
2. ✅ **SPEC v1 aprovado por Bruno em 2026-05-08** (sem inconsistências pesadas; preocupação registrada: migração de WIP de oportunidades em curso — endereçada em §11)
3. ✅ Mapping linha-a-linha das 218 colunas **dispensado** — só WIP migra, mapeamento se faz no go-live (§11.2)
4. ⏳ Spec análogo do `arv-pm` e `arv-framework` — Bruno ainda não decidiu se faz agora ou depois
5. ⏳ Estimar Fase 1A com base nesse SPEC (refazer estimativa do gap analysis incluindo as novas entidades) — provavelmente 200-280h ao invés de 130-220h, mas com baseline confiável

### 13.2 Tasks da Fase 1A — alto nível

(Detalhamento atomic em GSD quando você autorizar.)

```
1. Schema base (migrations 005-019, inclui alignment Empresa/Contato/Origem) [24-40h]
2. Refactor Lead (etapas, responsáveis, descarte/reativação) [12-20h]
3. Criar Oportunidade (entidade + serviços + endpoints) [16-28h]
4. Criar Orcamento (entidade + cálculos + versionamento) [12-20h]
5. Refatorar Score (ICP function + scoring_catalog + handlers) [12-20h]
6. Implementar Travas (stage_validators.py + validate_transition em todos services) [10-16h]
7. Importer Monday → DB (idempotente) [16-32h]
8. Dashboards Fase 1A (Saúde do Funil + Tração + Check-in) [24-40h]
9. Frontend — adaptar Lead/Oportunidade split + form de score + dashboards prioritários [40-60h]
10. Corrigir bug data_entrada → HistoricoEtapa em SLA worker, dashboard, kanban [4-6h]
11. Deploy staging + onboarding 2-3 piloto [8-12h]

TOTAL Fase 1A: ~178-294h ≈ 5-8 semanas em 30-40h/sem
```

(Estimativa Schema base subiu de 16-32h pra 24-40h em v1.1 — refactor de Empresa/Contato/Origem com tabelas de referência adiciona ~8h de trabalho.)

---

## Apêndice A — Glossário e siglas

- **OS** = Ordem de Serviço (numeração de projeto interna ARV)
- **CMV** = Custo de Mercadoria Vendida
- **ICP** = Ideal Customer Profile
- **BANT** = Budget, Authority, Need, Timing
- **MEDDIC** = Metrics, Economic buyer, Decision criteria, Decision process, Identify pain, Champion
- **ETO** = Engineer-to-Order
- **CNPJ** = Cadastro Nacional da Pessoa Jurídica
- **NPS** = Net Promoter Score (não escopo Fase 1)
- **Capex** = Capital Expenditure
- **Pré-Vendas (papel)** = qualificação inicial e oportunidade até handoff
- **Vendas (papel)** = comercial responsável de oportunidade até venda
- **Técnico (papel)** = engenharia comercial / responsável técnico da oportunidade

## Apêndice B — Referências cruzadas

- Diagnóstico geral: `../DIAGNOSTICO.md`
- Gap analysis arv-crm: `../discovery/ARV-CRM-GAP.md`
- Monday CRM deep-dive: `../discovery/MONDAY-CRM-DEEPDIVE.md`
- Monday inventory geral: `../discovery/MONDAY-INVENTORY.md`
- GitHub inventory: `../discovery/GITHUB-INVENTORY.md`
- Travas: `./travas.txt`
- Dashboards: `./dashboards.txt`
- Manual institucional: `./Manual Institucional e de Processos da ARV Systems.docx`
