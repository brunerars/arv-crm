# Planejamento de Migração — CRM ARV Systems
> Monday.com + Make.com → SaaS Custom (Claude Code)
> Gerado em: 2026-03-16

---

## 0. Diagnóstico — Por que migrar?

### Os 5 problemas estruturais do CRM atual

#### 1. MUITO BUROCRÁTICO
O Pipeline tem **150+ colunas** e **17 grupos**. Para mover um lead de "Lead Inicial" a "Pedido Convertido", o vendedor precisa preencher dezenas de campos manuais em cada fase. O CRM deveria simplificar a venda, mas hoje ele **adiciona atrito**. Exemplos:
- 28 colunas só para 4 contatos (nome, telefone, e-mail, cargo, departamento, influência, linkedin × 4)
- Checklist de fase com 23 campos booleanos (Foi enviado? Confirmou? Aprovado? Conferido?...)
- Campos de custos tributários (IR, CSLL, ICMS, ISS, PIS, COFINS) preenchidos manualmente

**Princípio para o SaaS:** Capturar o mínimo necessário por fase. Campos aparecem apenas quando relevantes. Automação preenche o que for possível.

#### 2. CORE DO CRM É GESTÃO DE TAREFA
O Monday.com é uma ferramenta de **project management** adaptada para CRM. O paradigma fundamental é "item em board com status" — ou seja, **gestão de tarefa**. Um CRM deveria ser centrado em:
- **Relacionamento** (conta + contatos + histórico)
- **Oportunidade** (deal com valor, probabilidade, próximos passos)
- **Pipeline visual** (onde cada deal está e o que falta para avançar)

Hoje o Pipeline é um **board gigante** onde leads e oportunidades são tratados como "tarefas" que mudam de grupo. Não existe visão de conta, não existe timeline de interações, não existe forecast.

**Princípio para o SaaS:** Entidade central = Oportunidade. Tudo gira em torno do deal. Conta e contatos são contexto. Atividades são consequência, não o core.

#### 3. POUCO ESTRATÉGICO
O CRM atual é **operacional** — registra o que aconteceu, mas não ajuda a decidir o que fazer. Problemas:
- Sem forecast de vendas (previsão de receita por período)
- Sem análise de funil (conversão entre etapas, tempo médio por fase)
- Sem velocidade de vendas (deals/mês, ticket médio, ciclo de venda)
- Scores (Técnico e Oportunidade) existem mas não influenciam priorização automaticamente
- Metas de vendas em board separado com 60+ fórmulas/mirrors frágeis
- Sem alertas inteligentes (deals parados, follow-ups atrasados, contas em risco)

**Princípio para o SaaS:** Dashboard estratégico com métricas em tempo real. IA sugere ações. Scores influenciam fila de prioridade. Forecast automático.

#### 4. MUITA AUTOMAÇÃO GAMBIARRA
São **37 cenários Make.com** (18 ativos de vendas) que compensam limitações do Monday. Muitas são "cola" entre boards que não se conectam nativamente:
- `Status Sincronizados` — sincroniza status entre 3 boards (151 execuções)
- `CRM - ATUALIZA DADOS DE TAREFAS` — propaga dados do Pipeline para Tarefas (1.076 execuções)
- `Contador de descartado` — incrementa um número porque o Monday não tem counter nativo (226 execuções)
- `base clientes` — sincroniza dados entre Pipeline e Gestão de Contas (20 execuções)
- `Data de reativação` / `reativar leads` — workaround para reabrir leads descartados (276 + 25 execuções)

Essas automações são **frágeis** (dependem de webhooks, consomem operações Make, falham silenciosamente) e existem porque a **arquitetura de dados é ruim**, não porque o processo precisa delas.

**Princípio para o SaaS:** Banco de dados relacional elimina 70% dessas automações. O que sobra vira regra de negócio no backend (event-driven, não webhook).

#### 5. FALTA DE CLAREZA
Com 150+ colunas em um board, ninguém sabe exatamente:
- Quais campos são obrigatórios em cada fase
- O que precisa acontecer para avançar de etapa
- Onde encontrar a informação que precisa
- Qual a diferença entre "Estimativa Orçamentária" e "Projeção Orçamentária"

O Pipeline tem grupos como "Estimativa em Conversão" e "Projeção em Conversão" que confundem a equipe. Campos de score técnico, score de oportunidade, leadscore e classificação coexistem sem hierarquia clara.

**Princípio para o SaaS:** Cada etapa tem um checklist mínimo visível. Transições são explícitas com gates. Interface mostra apenas o contexto relevante da fase atual. Nomenclatura simples e consistente.

---

### Resumo do Diagnóstico

| Problema | Causa Raiz | Solução no SaaS |
|---|---|---|
| Burocrático | 150+ colunas, campos manuais | Progressive disclosure, auto-fill, campos por fase |
| Task-centric | Monday é PM tool, não CRM | Modelo centrado em oportunidade/relacionamento |
| Pouco estratégico | Sem analytics nativos | Dashboards, forecast, scoring com priorização |
| Gambiarras | Dados não normalizados | Banco relacional, regras de negócio no backend |
| Falta clareza | Tudo em 1 board, sem gates | Funil com etapas claras, checklist por fase, UX limpa |

---

## 1. Panorama Atual

### 1.1 Workspaces Monday.com
| Workspace | ID | Papel |
|---|---|---|
| **Comercial** | 7490918 | CRM em produção (Pipeline legado + boards auxiliares) |
| **MCP CRM** | 14592352 | Workspace de desenvolvimento do novo CRM normalizado |
| **Template CRM** | 14593012 | Templates (Metas de Vendas) |

### 1.2 Equipe Comercial (Usuários Relevantes)
| Nome | ID | Papel |
|---|---|---|
| Bruno (Admin) | 46925496 | Dono do CRM, responsável técnico |
| Cintia Olívia | 53261396 | Equipe comercial |
| Saulo | 53216306 | Equipe comercial |
| Mariana Constantinou | 48342980 | Vendedora |
| Lucas Mantovani | 76000687 | Equipe comercial |
| Vinicius Correia | 53261388 | Equipe comercial |
| Isabella Valverde Chaves | 67035925 | Inovação / Automações |

---

## 2. Estrutura de Boards — Workspace Comercial (Produção)

### 2.1 Pasta: CRM ✅🎯💰

#### Pipeline (ID: 7089923423) — BOARD PRINCIPAL
- **Items:** 1.854
- **Descrição:** Funil monolítico com 150+ colunas, gerenciando todo o fluxo de pré-vendas a vendas

**Grupos (Funil Completo):**
| # | Grupo | Fase |
|---|---|---|
| 1 | Lead Inicial | PRÉ VENDAS |
| 2 | Qualificação Inicial | PRÉ VENDAS |
| 3 | Qualificação da Oportunidade | PRÉ VENDAS |
| 4 | Análise Interna | PRÉ VENDAS |
| 5 | Estimativa Orçamentária | PRÉ VENDAS |
| 6 | Estimativa em Conversão | PRÉ VENDAS |
| 7 | Projeção Orçamentária | PRÉ VENDAS |
| 8 | Projeção em Conversão | PRÉ VENDAS |
| 9 | Passagem Pré Vendas → Vendas | TRANSIÇÃO |
| 10 | Desenvolvimento de Proposta | VENDAS |
| 11 | Proposta Enviada | VENDAS |
| 12 | Proposta em Análise Técnica | VENDAS |
| 13 | Proposta em Análise Comercial | VENDAS |
| 14 | Proposta em Negociação | VENDAS |
| 15 | Emissão do Pedido de Compra | VENDAS |
| 16 | Pedido Convertido em Venda | VENDAS (WON) |
| 17 | Leads Descartados (DL) | LOST |

**Dados Capturados por Fase — Pipeline Legado:**

##### DADOS DO LEAD (capturados na entrada)
| Campo | Tipo | Column ID |
|---|---|---|
| Nome (Razão Social) | name | name |
| Razão Social | text | text_mkswdjej |
| CNPJ | text | texto3__1 |
| CEP | text | text_mkv19nk3 |
| Número | text | text_mkv5d6xh |
| Complemento | text | text_mkt2js0v |
| Telefone Fixo | phone | phone_mkswx96x |
| Lead ID | text | texto0__1 |
| Origem | status | color_mksw655h |
| Sub-Origem | status | color_mksw880q |
| Resp. Comercial | people | person |
| Data de Entrada Pré Vendas | date | data |

##### CONTATOS (até 4 contatos inline — NÃO normalizado)
| Campo | Contato 1 | Contato 2 | Contato 3 | Contato 4 |
|---|---|---|---|---|
| Nome | texto__1 | text_mkswjyt7 | text_mksww1h5 | text_mkswwzt |
| Telefone/WhatsApp | telefone5__1 | phone_mkswrte1 | phone_mkswcz3v | phone_mkswf758 |
| E-mail | e_mail4__1 | email_mkswr508 | email_mkswfq2t | email_mkswjr7c |
| Cargo | color_mkswyrf9 | color_mkswg25h | color_mkswbwqb | color_mksww5ca |
| Departamento | color_mksw1c8f | color_mkswmpvb | color_mkswy5fr | color_mksw5ce7 |
| Nível Influência | color_mksw6w9r | color_mkswwfxb | color_mksws92c | color_mksws6z5 |
| LinkedIn | text_mkswskxg | text_mkswqjk1 | text_mksw9qmt | text_mkswtdt0 |

##### QUALIFICAÇÃO DO LEAD (Pré-Vendas)
| Campo | Tipo | Column ID |
|---|---|---|
| Segmento de Mercado | status | color_mksa4qtt |
| Qtd Funcionários | status | color_mksab6mj |
| Tempo no Mercado | status | color_mksaqv72 |
| Nº Plantas Industriais | status | color_mksa19z1 |
| Distância da Planta | status | color_mksa5jms |
| Lead Scoring | numbers | numeric_mksaxarq |
| Classificação de Leads | status | color_mksacpmx |
| Produto | status | status83__1 |
| Área de Atuação | status | color_mksxq7he |
| Tipo de Entrega | status | color_mksxmwc0 |

##### SCORE TÉCNICO (9 perguntas + botão IA)
| Campo | Column ID |
|---|---|
| ARV realizou projeto semelhante? | color_mkzjdndj |
| Dentro do domínio técnico ARV? | color_mkzjnbvr |
| Grau de risco técnico | color_mkzjfs9z |
| Completude das informações do cliente | color_mkzjpf79 |
| Grau de complexidade técnica | color_mkzj244p |
| Viabilidade técnica | color_mkzjaghc |
| Retrofit ou solução nova? | color_mkzjyp2f |
| Pode adiar sem impactos? | color_mkzjcv8v |
| ARV domina as tecnologias? | color_mkzj6r8y |
| **Valor do Score** | numeric_mkzj4xnw |
| **Score Técnico (label)** | color_mkzjw3ah |

##### SCORE DA OPORTUNIDADE (9 perguntas + botão IA)
| Campo | Column ID |
|---|---|
| Prazo estimado emissão pedido | color_mkzn6733 |
| Chance de não acontecer | color_mkzn6wg0 |
| Capex aprovado | color_mkzn9pxh |
| Valor estimado / teto | color_mkznn3dq |
| Resultados esperados | color_mkznjgpa |
| Payback esperado | color_mkzn1c9t |
| Caderno de encargos | color_mkzngaj9 |
| Papel na decisão | color_mkzndjfw |
| Já comprou com ARV? | color_mkznbc68 |
| **Score Oportunidade** | numeric_mksads1c |
| **Temperatura** | status46__1 |
| **Ação Recomendada** | color_mkzrrz8w |

##### PROPOSTA / FINANCEIRO (Vendas)
| Campo | Tipo | Column ID |
|---|---|---|
| Valor Estimado (R$) | numbers | numeric_mksxe7zk |
| Valor Final (R$) | numbers | numeric_mksx2yc6 |
| Valor Projetado | numbers | n_meros44__1 |
| Nº Revisão | numbers | numeric_mksxbxfb |
| Chance de Conversão | numbers | numeric_mksy1zy4 |
| Data Criação Orçamento | date | date_mkye4yvc |
| Data Prevista Vendas | date | date_mksys9x6 |
| Cronograma | timeline | timerange_mksx6wg8 |
| Prazo Entrega Cliente | date | date_mkxkv99j |
| Prazo Entrega ARV | date | date_mkxk4cz8 |

##### CUSTOS / MARKUP
| Campo | Column ID |
|---|---|
| Antecipação | numeric_mksz4237 |
| Custo Fixo | numeric_mksyrryy |
| Custo Financeiro | numeric_mksycfae |
| Comissão | numeric_mksyqzqr |
| Markup | numeric_mksypp34 |
| CMV | numeric_mksyv759 |
| Terceiros | numeric_mksyrsev |
| Mão de Obra | numeric_mksyc1vw |
| IR | numeric_mksy3e80 |
| CSLL | numeric_mksyr7gt |
| ICMS | numeric_mksy27nf |
| ISS | numeric_mksy99tc |
| PIS | numeric_mksyrsgs |
| COFINS | numeric_mksye7da |

##### FÓRMULAS CALCULADAS
| Fórmula | Column ID |
|---|---|
| Proposta com Imposto | formula_mkszg7rf |
| Proposta sem Imposto | formula_mkszj1d2 |
| Composição Meta de Vendas | formula_mkszhj55 |
| Previsão com Imposto | formula_mkszbz89 |
| Previsão sem Imposto | formula_mkszwn3x |
| Previsão Meta de Vendas | formula_mkszg3zx |
| Previsão Meta no Ano | formula_mksz9h3 |
| Previsão Meta no Mês | formula_mkt53wfv |

##### CHECKLIST DE FASE (Fundo de Funil)
| Campo | Column ID | Fase |
|---|---|---|
| Foi Enviado ao Cliente? | color_mkw946r6 | Proposta Enviada |
| Data de Envio | date_mkw97k45 | Proposta Enviada |
| Dentro da faixa? | color_mkwbpk1g | Proposta Enviada |
| Aprovado pelo Comitê | color_mkwhksae | Análise |
| Proposta Enviada ao Cliente | color_mkwhe726 | Proposta |
| Confirmou Recebimento | color_mkwhn5yv | Proposta |
| Prazo Avaliação Técnica | date_mkwhax75 | Análise Técnica |
| Apresentação Realizada | color_mkwhs0rn | Análise Técnica |
| Solução Técnica Aprovada | color_mkwhh8h8 | Análise Técnica |
| Prazo Análise Comercial | date_mkwhpq6v | Análise Comercial |
| E-mail ao Comprador | color_mkwhcba5 | Análise Comercial |
| Visita Comercial Realizada | color_mkwjtpkm | Negociação |
| Valor na Expectativa | color_mkwjret0 | Negociação |
| Prazo Retorno Negociação | date_mkwjp97c | Negociação |
| Condições Aceitas | color_mkwjecdh | Negociação |
| Confirmou Intenção | color_mkwjdmmr | Negociação |
| Atendemos Prazo | color_mkwj4dc3 | Pedido |
| Prazo Emissão Pedido | date_mkwjemxm | Pedido |
| Pedido Recebido | color_mkwjat8f | Pedido |
| Pedido Conferido | color_mkwjkexa | Pedido |
| Pasta Atualizada | color_mkwj6et3 | Pedido |
| Nº OS | text_mkwpwyjz | Pedido |
| Data Passagem Bastão | date_mkwkj5xk | Pedido |

##### RASTREAMENTO TEMPORAL (Contadores)
| Campo | Column ID |
|---|---|
| Tempo na Etapa | duration_mkswehxd |
| Data Ult. Atividade | date_mkswn328 |
| Entrou no fundo de funil | date_mkyaesy |
| Lead qualificado | date_mkz3sasq |
| Entrou em Estimativa | date_mkzahazd |
| Entrou em Projeção | date_mkzaprb1 |
| Entrou em Projeção em Conversão | date_mkzcznpt |
| Entrou em Estimativa e Conversão | date_mkzcg8ze |
| Entrou em Proposta Enviada | date_mkzch20r |
| Data Reativação | date_mm0gaa48 |
| Contador descartados | numeric_mkx498n9 |
| Contador Topo | formula_mkyesfge |
| Contador Meio | formula_mkyew65t |
| Contador Fundo | formula_mkyewwmk |

##### RELAÇÕES (Board Relations)
| Relação | Board Destino |
|---|---|
| Atividades | board_relation_mktjy6x8 |
| Calendário de Visitas | board_relation_mkttdz1k |
| Serviços e Revendas | board_relation_mkvd9n3m |
| Portfólio de Automação | board_relation_mkxe4wcc |
| Tarefas Técnicas | board_relation_mkz37spz |

---

#### Quadro de Prospecção (ID: 18399307546)
- **Items:** 3.709
- **Função:** Base de prospects pré-cadastro no Pipeline

| Campo | Tipo |
|---|---|
| Name (Razão Social) | name |
| Estado | text |
| Cidade | text |
| CNPJ | text |
| Pessoa (responsável) | people |
| Enviar ao Pipeline (botão) | button |
| Status | status (Prospectado / Parado / Falta Info / Descartado) |
| Data da Prospecção | date |

**Grupos:** Prospectar → Sem Info → Prospectados → Descartado

---

#### Calendário de Visitas (ID: 9758896572)
- **Items:** 473

| Campo | Tipo |
|---|---|
| Name | name |
| Agendada por | people |
| Status | status (Agendar/Agendada/Concluída/Cancelada) |
| Vendedor(a) | status (Alex/Gabriel/Mauricio/Lilian/Mariana/Santiago) |
| Responsável visita | people |
| Data da Visita | date |
| Perfil da Visita | status (FUP Proposta/Pré Vendas/NPS/Reativação/Prospecção/Alinhamento Técnico/Cross Sell) |
| Local | location |
| Zona | status (Sul/Norte/Leste/Oeste) |
| Cidade | text |
| Estado | text |
| LeadID | text |
| Pipeline | board_relation → Pipeline |
| Arquivos | file |
| Data de Entrada | date |
| Data de Conclusão | date |

**Grupos:** Planejamento → Agendadas → Concluídas → Canceladas

---

#### Gestão de Contas (ID: 18396765892)
- **Items:** 3
- **Função:** Gestão de contas de clientes ativos (Categoria: Base / Primeiro Contato / Reativação / Com Oportunidade)

---

#### Tarefas (ID: 9760832128) / Tarefas Paralelas (ID: 18390965607) / Tarefas Técnicas (ID: 18393358566)
- **Função:** Boards de atividades vinculados ao Pipeline

---

### 2.2 Pasta: QUADROS AUXILIARES

#### Entrada de Leads (ID: 18193210777)
- **Items:** 207
- **Função:** Intake de leads (formulário/automação)

| Campo | Tipo |
|---|---|
| Name | name |
| Pessoa | people |
| Origem | status (Ativa / Passiva / Indicação) |
| Sub Origem | status (Pré Vendas/Vendas/Ativa.ai/Busca Orgânica/Eventos/Tráfego Pago/Cliente/Colaborador/Parceiro) |
| CNPJ | text |
| Nome do Contato | text |
| Telefone do Contato | phone |
| E-mail do Contato | email |
| Descrição da Demanda | long_text |
| Data de Entrada | date |

---

### 2.3 Boards Auxiliares (root level)

| Board | ID | Items | Função |
|---|---|---|---|
| Subelementos de Pipeline | 7225377727 | 0 | Sub-items do Pipeline (perguntas/checklist) |
| Quotes & Invoices | 8326289541 | - | Orçamentos e faturas |
| Sub. Calendário Visitas | 9758896713 | - | Sub-items de visitas |
| Sub. Tarefas | 10040047994 | - | Sub-items de tarefas |

---

## 3. Estrutura do Novo CRM (MCP CRM — Workspace 14592352)

### 3.1 Master Data (Pasta: Dados Mestres)

#### 01_EMPRESAS (ID: 18402998719)
| Campo | Tipo |
|---|---|
| Name (Nome Fantasia) | name |
| CNPJ | text |
| Razão Social | text |
| Segmento | status |
| Nº Funcionários | status |
| Nº de Plantas | numbers |
| Distância ARV (km) | numbers |
| Cidade | text |
| Estado | status |
| CEP | text |
| Telefone | phone |
| Status da Conta | status |
| Data Cadastro | date |
| Data Última Compra | date |
| Valor Total Comprado (R$) | numbers |
| Responsável Comercial | people |
| Site | text |
| Observações | long_text |
| **→ Leads** | relation → 04_LEADS |
| **→ Oportunidades** | relation → 05_OPORTUNIDADES |

**Grupos:** Inativos / Clientes Ativos / Prospects com Oportunidade / Base de Prospecção

#### 02_CONTATOS (ID: 18402998722)
| Campo | Tipo |
|---|---|
| Name | name |
| Cargo | status |
| Departamento | status |
| Nível de Influência | status |
| E-mail | email |
| WhatsApp | phone |
| LinkedIn | text |
| Ativo? | status |
| Data Cadastro | date |
| **→ Empresa** | relation → 01_EMPRESAS |
| Observações | long_text |

**Grupos:** Inativos / Operacionais / Influenciadores / Decisores

### 3.2 Funil de Pré-Vendas (Pasta: Pipeline)

#### 04_LEADS (ID: 18402999165)
| Campo | Tipo |
|---|---|
| Name | name |
| Lead ID | text |
| **→ Empresa** | relation → 01_EMPRESAS |
| **→ Contato Principal** | relation → 02_CONTATOS |
| Responsável | people |
| Etapa | status |
| Sub-Status | status |
| Temperatura | status |
| **→ Origem** | relation → board 18402998725 |
| Produto de Interesse | status |
| Lead Score | numbers |
| Classificação | status |
| Valor Estimado (R$) | numbers |
| Motivo de Descarte | status |
| Data de Entrada | date |
| Data de Qualificação | date |
| Próx. Atividade | status |
| Data Próx. Atividade | date |
| **→ Oportunidade** | relation → 05_OPORTUNIDADES |

**Funil:** Prospecção → Primeiro Contato → Qualificação → Qualificado ✅ → Descartado ❌

### 3.3 Funil de Vendas (Pasta: Pipeline)

#### 05_OPORTUNIDADES (ID: 18402999166)
| Campo | Tipo |
|---|---|
| Name | name |
| **→ Lead de Origem** | relation → 04_LEADS |
| **→ Empresa** | relation → 01_EMPRESAS |
| **→ Contatos** | relation → 02_CONTATOS |
| Resp. Comercial | people |
| Resp. Técnico | people |
| Etapa | status |
| Sub-Status | status |
| Temperatura | status |
| Classificação | status |
| Tipo de Entrega | status |
| Valor Estimado (R$) | numbers |
| Valor Projetado (R$) | numbers |
| Valor Final (R$) | numbers |
| Probabilidade (%) | numbers |
| Score Técnico | numbers |
| Score Oportunidade | numbers |
| Data de Entrada | date |
| Data Prevista Fechamento | date |
| Data Fechamento / Perda | date |
| Motivo de Perda | status |
| Tempo na Etapa | time_tracking |
| Observações | long_text |
| **→ Orçamentos** | relation → 18402999765 |
| **→ Tarefas** | relation → 18402999766 |
| **→ Visitas** | relation → 18402999768 |
| **→ Tarefas Técnicas** | relation → 18402999770 |

**Funil:** Qualificação da Oportunidade → Análise Interna → Desenvolvimento de Proposta → Proposta Enviada → Em Negociação → Fechamento → Convertido em Projeto 🚀 / Perdido ❌

### 3.4 Metas de Vendas

#### ⭐️ Metas de vendas (ID: 18403001885)
- **Items:** 8 reps de venda
- **Estrutura:** Meta mensal (Jan-Dez) x Real (mirror do pipeline) x Fórmulas (% mensal, % anual, delta, trimestres)
- **Equipes:** PME / Médio Porte / Corporativo
- **Funções:** AE (Account Executive) / AM (Account Manager)

---

## 4. Automações Make.com (Team: ARV, ID: 351023)

### 4.1 Automações de VENDAS/CRM (Ativas)

| # | Cenário | ID | Execuções | Função |
|---|---|---|---|---|
| 1 | **CADASTRO DE LEADS** | 4346128 | 43 | Webhook → cria lead no Pipeline (Monday) |
| 2 | **Leads via Falecom** | 3108190 | 1.579 | Polling e-mail (30min) → regex + GPT → cria lead no Monday |
| 3 | **LEAD ID** | 4195249 | 233 | Gera Lead ID sequencial ao criar item no Monday |
| 4 | **Pesquisa por CNPJ** | 4306043 | 199 | Botão → ReceitaWS + CNPJA + GPT → enriquece dados empresa |
| 5 | **Score Técnico** | 4500872 | 24 | Botão → GPT analisa respostas → calcula score técnico |
| 6 | **Score Da oportunidade** | 4506006 | 31 | Botão → GPT analisa respostas → calcula score oportunidade |
| 7 | **CRM - ATUALIZA DADOS DE TAREFAS** | 4195306 | 1.076 | Webhook → sincroniza dados entre Pipeline e Tarefas |
| 8 | **CRM - DATA DA PROPOSTA ARV + CLIENTE** | 4227301 | 109 | Webhook → calcula datas de proposta |
| 9 | **Cronograma Técnico** | 4480179 | 50 | Webhook → sincroniza cronograma técnico |
| 10 | **Contador de descartado** | 4369333 | 226 | Webhook → incrementa contador ao descartar lead |
| 11 | **DATA INTEGRAÇÃO** | 4275504 | 42 | Webhook → calcula data de integração |
| 12 | **Data de reativação** | 4557435 | 276 | Webhook → registra data de reativação |
| 13 | **reativar leads** | 4557476 | 25 | Webhook → reativa lead (muda status, envia e-mail, anexa doc OneDrive) |
| 14 | **prazo atividades** | 4452903 | 128 | Webhook → calcula prazo de atividades |
| 15 | **Status Sincronizados** | 4503899 | 151 | Webhook → sincroniza status entre boards |
| 16 | **Responsável Comercial Visita** | 4216059 | 29 | Webhook → atribui responsável comercial na visita |
| 17 | **ruas/zonas** | 4397161 | 34 | CEP → HTTP geocoding + GPT → calcula zona |
| 18 | **base clientes** | 4524007 | 20 | Webhook → sincroniza base de clientes |

### 4.2 Automações de PROJETOS (Ativas)

| # | Cenário | ID | Execuções | Função |
|---|---|---|---|---|
| 1 | [ATA DE REUNIÃO] → PEGAR PENDENCIAS | 4503310 | 48 | Webhook → extrai pendências de ata |
| 2 | [ATA DE REUNIÃO] → TAREFAS CRIADAS | 4503147 | 51 | Webhook → cria tarefas a partir de ata |
| 3 | HUB-WBS-WEBHOOK | 4501176 | 37 | Webhook → hub de WBS projetos |
| 4 | [RESUMO PROJETO] → PEGA-CRONOGRAMA-POR-GRUPO | 4498978 | 79 | Webhook → monta cronograma por grupo |
| 5 | [RESUMO PROJETO] → PEGA MATERIAIS | 4536275 | 80 | Webhook → lista materiais do projeto |
| 6 | [RESUMO PROJETO] → PENDENCIAS NOVAS | 4503943 | 80 | Webhook → lista pendências novas |
| 7 | [RESUMO PROJETO] → TAREFAS DO PROJETO | 4580068 | 60 | Webhook → lista tarefas do projeto |
| 8 | USER-MONDAY | 4536440 | 40 | Webhook → retorna dados do usuário Monday |
| 9 | WORKFLOW DUPLO | 4545634 | 1 | Webhook → workflow de criação dupla |
| 10 | CRIA-PENDENCIA | 4576248 | 31 | Webhook → cria pendência |
| 11 | CRIA-TAREFA | 4576257 | 53 | Webhook → cria tarefa |
| 12 | PEGAR-PENDENCIAS | 4597712 | 14 | Webhook → busca pendências |
| 13 | MONDAY-PLANNER | 4607473 | 6 | Webhook → integra com Google Sheets |

### 4.3 Automações ADMINISTRATIVAS / RH (Ativas)

| # | Cenário | ID | Função |
|---|---|---|---|
| 1 | Aviso de gastos | 4400644 | Monday → e-mail Microsoft |
| 2 | EMAIL DE ANIVERSÁRIO | 4081789 | Monday → e-mail aniversário |
| 3 | EMAIL TEMPO DE EMPRESA | 4152296 | Monday → e-mail tempo empresa |
| 4 | Data da proxima ASO | 4449306 | Calcula próxima ASO |

### 4.4 Automações INATIVAS

| Cenário | ID | Motivo provável |
|---|---|---|
| conclusão de tarefas | 4438796 | Substituída |
| CRIA FORMULÁRIO COM ID DO CRM | 4365425 | Descontinuada |
| PROMOÇÃO WBS | 3560527 | Descontinuada |
| Travas | 4370461 | Substituída (896 execuções) |
| URL FORMS MONDAY AUTOMACAO EXEMPLO | 4063805 | Exemplo/dev |
| WORKFLOW-PROJETOS-2 | 4501036 | Dev |

---

## 5. Mapeamento Excalidraw → Sistemas Necessários

Com base na imagem `excalidraw - sistemas necessarios.png`:

### PRÉ VENDAS
| Funcionalidade | Status no Monday | Automação Make | Migrar para SaaS |
|---|---|---|---|
| **Leadscore** | ✅ numeric_mksaxarq (Pipeline) / numeric_mm175fye (04_LEADS) | ✅ LEAD ID + scoring manual | Lead Scoring engine (regras + IA) |
| **Opportunity Score** | ✅ numeric_mksads1c (Pipeline) / numeric_mm17nybg (05_OPORT.) | ✅ "Score Da oportunidade" (GPT) | Opportunity Scoring engine |
| **Score Técnico** | ✅ numeric_mkzj4xnw (Pipeline) / numeric_mm17jma4 (05_OPORT.) | ✅ "Score Técnico" (GPT) | Technical Scoring engine |
| **Chatbot** | ❌ Não existe no Monday | ❌ Não existe | Chatbot de qualificação (novo) |
| **FUP 3/7/10 dias** | ⚠️ Parcial (Data Próx. Atividade) | ⚠️ "prazo atividades" | Follow-up automatizado (3/7/10 dias) |
| **Enriquecimento de Leads** | ✅ Botão "Pesquisar CNPJ?" | ✅ "Pesquisa por CNPJ" (ReceitaWS + CNPJA + GPT) | Enriquecimento automático na entrada |

### VENDAS
| Funcionalidade | Status no Monday | Automação Make | Migrar para SaaS |
|---|---|---|---|
| **Geração de Orçamento/Proposta** | ✅ Campos financeiros no Pipeline | ✅ "CRM - DATA DA PROPOSTA" | Módulo de propostas/orçamentos |
| **Gestão de Metas** | ✅ Board "Metas de vendas" (mirrors + fórmulas) | ❌ Manual | Dashboard de metas (real-time) |
| **Visitas** | ✅ Calendário de Visitas (473 items) | ✅ "Responsável Comercial Visita" + "ruas/zonas" | Módulo de visitas com geolocalização |
| **Cross & Up Sell** | ⚠️ Perfil "Cross Sell" no Calendário | ❌ Não automatizado | Motor de recomendações cross/up sell |

---

## 6. Modelo de Dados Proposto para o SaaS

### 6.1 Entidades Principais

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   EMPRESAS   │────<│   CONTATOS   │     │   ORIGENS    │
│   (Contas)   │     │  (Pessoas)   │     │  (Canais)    │
└──────┬───────┘     └──────┬───────┘     └──────┬───────┘
       │                    │                    │
       │    ┌───────────────┼────────────────────┘
       │    │               │
       ▼    ▼               ▼
┌──────────────┐     ┌──────────────┐
│    LEADS     │────>│ OPORTUNIDADES│
│ (Pré-Vendas) │     │   (Vendas)   │
└──────┬───────┘     └──────┬───────┘
       │                    │
       │              ┌─────┼─────┬────────┐
       │              │     │     │        │
       ▼              ▼     ▼     ▼        ▼
┌──────────────┐ ┌────────┐┌────┐┌───────┐┌────────┐
│  ATIVIDADES  │ │ORÇAMENT││VISI││TAREFAS││TAREFAS │
│  (Follow-up) │ │  OS    ││TAS ││       ││TÉCNICAS│
└──────────────┘ └────────┘└────┘└───────┘└────────┘
```

### 6.2 Tabelas de Dados

#### `empresas` (Account)
```sql
id, nome_fantasia, razao_social, cnpj, segmento,
num_funcionarios, num_plantas, distancia_arv_km,
cidade, estado, cep, telefone, site,
status_conta (prospect|com_oportunidade|cliente_ativo|inativo),
responsavel_comercial_id, data_cadastro, data_ultima_compra,
valor_total_comprado, observacoes
```

#### `contatos` (Contact)
```sql
id, empresa_id (FK), nome, cargo, departamento,
nivel_influencia (operacional|influenciador|decisor),
email, whatsapp, linkedin, ativo, data_cadastro, observacoes
```

#### `leads` (Lead / Pré-Venda)
```sql
id, lead_id (sequencial), empresa_id (FK), contato_principal_id (FK),
origem_id (FK), responsavel_id,
etapa (prospeccao|primeiro_contato|qualificacao|qualificado|descartado),
sub_status, temperatura (frio|morno|quente),
produto_interesse, lead_score, classificacao,
valor_estimado, motivo_descarte,
data_entrada, data_qualificacao,
prox_atividade, data_prox_atividade,
oportunidade_id (FK → oportunidades, quando convertido)
```

#### `oportunidades` (Opportunity / Venda)
```sql
id, lead_origem_id (FK), empresa_id (FK),
resp_comercial_id, resp_tecnico_id,
etapa (qualificacao_oport|analise_interna|dev_proposta|
       proposta_enviada|negociacao|fechamento|convertido|perdido),
sub_status, temperatura, classificacao, tipo_entrega,
valor_estimado, valor_projetado, valor_final,
probabilidade_pct, score_tecnico, score_oportunidade,
data_entrada, data_prevista_fechamento, data_fechamento_perda,
motivo_perda, observacoes
```

#### `orcamentos` (Quote)
```sql
id, oportunidade_id (FK), num_revisao,
valor_estimado, valor_final, antecipacao,
custo_fixo, custo_financeiro, comissao, markup,
cmv, terceiros, mao_obra,
ir, csll, icms, iss, pis, cofins,
proposta_com_imposto (calc), proposta_sem_imposto (calc),
data_criacao, data_envio, status
```

#### `visitas` (Visit)
```sql
id, oportunidade_id (FK), empresa_id (FK),
agendada_por_id, responsavel_visita_id,
status (agendar|agendada|concluida|cancelada),
perfil (fup_proposta|pre_vendas|nps|reativacao|
        prospeccao|alinhamento_tecnico|cross_sell),
data_visita, local_lat, local_lng, zona, cidade, estado,
data_entrada, data_conclusao, arquivos
```

#### `atividades` (Activity / Follow-up)
```sql
id, lead_id (FK nullable), oportunidade_id (FK nullable),
tipo (ligacao|email|reuniao|follow_up|tarefa),
descricao, responsavel_id, data_prazo, data_conclusao,
status (pendente|em_andamento|concluida)
```

#### `scoring_respostas` (Score Answers)
```sql
id, entidade_tipo (lead|oportunidade), entidade_id,
tipo_score (leadscore|tecnico|oportunidade),
pergunta_id, resposta, peso, created_at
```

#### `metas_vendas` (Sales Target)
```sql
id, vendedor_id, equipe, funcao (ae|am),
ano, mes, valor_meta, valor_real (calculado)
```

#### `historico_etapas` (Stage History / Audit)
```sql
id, entidade_tipo, entidade_id,
etapa_anterior, etapa_nova,
usuario_id, data_mudanca, tempo_na_etapa_anterior
```

---

## 7. Automações a Replicar no SaaS

### 7.1 Prioridade ALTA (Core do CRM)

| Automação Make | Equivalente no SaaS | Complexidade |
|---|---|---|
| CADASTRO DE LEADS | API endpoint POST /leads + validação | Baixa |
| Leads via Falecom | E-mail parser + IA classificação + auto-create | Alta |
| LEAD ID | Auto-increment no banco | Trivial |
| Pesquisa por CNPJ | ReceitaWS/CNPJA integration + auto-enrich | Média |
| Score Técnico | Scoring engine com LLM (Claude API) | Média |
| Score Da oportunidade | Scoring engine com LLM (Claude API) | Média |
| CRM - ATUALIZA DADOS DE TAREFAS | Event-driven sync (DB triggers / webhooks) | Média |
| Status Sincronizados | Eliminado — relacionamentos diretos no banco | Trivial |
| Contador de descartado | DB counter / audit trail | Trivial |

### 7.2 Prioridade MÉDIA

| Automação Make | Equivalente no SaaS | Complexidade |
|---|---|---|
| CRM - DATA DA PROPOSTA | Lógica de negócio no módulo de propostas | Baixa |
| Data de reativação | Workflow de reativação automática | Média |
| reativar leads | Workflow: status change + e-mail + notificação | Média |
| prazo atividades | CRON job para alertas de prazo | Baixa |
| Responsável Comercial Visita | Assignment rules no módulo de visitas | Baixa |
| ruas/zonas | Geocoding API (Google Maps / ViaCEP) | Média |
| base clientes | Eliminado — dados normalizados no banco | Trivial |

### 7.3 Prioridade BAIXA (podem ficar para v2)

| Automação Make | Equivalente no SaaS |
|---|---|
| Cronograma Técnico | Módulo de cronograma |
| DATA INTEGRAÇÃO | Campo calculado |
| FUP 3/7/10 dias (NOVO) | CRON + notification engine |
| Chatbot (NOVO) | Widget embeddable com Claude API |
| Cross & Up Sell (NOVO) | Recommendation engine |

---

## 8. Volumes de Dados para Migração

| Entidade | Board Origem | Qtd Items |
|---|---|---|
| Prospects | Quadro de Prospecção | 3.709 |
| Leads + Oportunidades | Pipeline | 1.854 |
| Visitas | Calendário de Visitas | 473 |
| Leads (intake) | Entrada de Leads | 207 |
| Metas | Metas de vendas | 8 |
| Contas | Gestão de Contas | 3 |
| **Total estimado** | | **~6.254 registros** |

**Obs:** Os 1.854 items do Pipeline precisarão ser splitados entre `leads`, `oportunidades`, `contatos` (4 contatos por item = até 7.416 contatos) e `empresas` durante a migração.

---

## 9. Riscos e Considerações

1. **Pipeline monolítico:** O board Pipeline tem 150+ colunas e mistura pré-vendas + vendas. A migração requer regras de split por grupo/etapa.

2. **Contatos denormalizados:** Até 4 contatos inline por item no Pipeline (28 colunas de contato). Precisa normalizar para tabela `contatos`.

3. **Scoring com IA:** Os scores técnico e de oportunidade usam GPT via Make. No SaaS, migrar para Claude API.

4. **Fórmulas complexas:** O board de Metas usa 60+ fórmulas e mirrors. No SaaS, substituir por queries SQL / views materializadas.

5. **Integrações externas:** ReceitaWS, CNPJA, Google Sheets, Microsoft Email, OneDrive — precisam ser mantidas.

6. **Equipe em produção:** A migração precisa ser feita em paralelo (dual-write) para não interromper operações.

---

## 10. Fases de Implementação Sugeridas

| Fase | Escopo | Dependências |
|---|---|---|
| **F0 — Preparação** | Schema DB, auth, RBAC, API base | - |
| **F1 — Dados Mestres** | Empresas + Contatos + Origens + migração | F0 |
| **F2 — Funil Pré-Vendas** | Leads + Lead Scoring + Enriquecimento CNPJ | F1 |
| **F3 — Funil Vendas** | Oportunidades + Propostas + Scores IA | F2 |
| **F4 — Atividades** | Tarefas + Visitas + Follow-up + Calendário | F3 |
| **F5 — Metas & Dashboards** | Metas de vendas + KPIs + Relatórios | F3 |
| **F6 — Automações** | FUP automático + Chatbot + Cross/Up Sell | F4 |
| **F7 — Go-Live** | Migração final + dual-write + cutover | F5, F6 |
