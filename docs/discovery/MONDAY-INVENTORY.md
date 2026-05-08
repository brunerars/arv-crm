# Monday Inventory — ARV Systems
Coletado em: 2026-05-07

## Resumo executivo

- **Workspaces cobertos:** 5 (Comercial 💰, MCP CRM, Projetos 🚀, Serviço e Revenda, Administração 🎯)
- **Boards relevantes inventariados:** 67+ (boards-pais + 30 boards de projetos individuais agrupados por padrão)
- **Total de items somados (boards principais inventariados):** ~38.500 items
- **Boards com >1.000 items:** Ponto Digital 📅 (10.045), Ponto digital ADM (8.154), Tarefas 📌 Projetos (7.143), Tarefas Comercial (6.841), Quadro de Prospecção (3.709), Pipeline (1.875), Tarefas JM (1.067), Tarefas CM (1.042)
- **Limite de items dos boards de tarefas Projetos atingido:** Tarefas 📌 (7.143/10.000) e Ponto Digital 📅 (10.045/10.000 — **excedeu**)
- Todos os boards do **MCP CRM** estão com 1-2 items (workspace de redesign vazio, ainda em construção)
- **Pipeline (CRM legado)** = 183 colunas, 17 grupos, 1.875 items (planilha gigante com 24 campos planos de contato — 4 grupos de "Nome/Cargo/Depto/Tel/Email/Linkedin Contato 1..4")

---

## Workspace: Comercial 💰 (id 7490918)
CRM legado, 10 owners, criado 2024-07-29. Será substituído pelo MCP CRM.

### Board: Pipeline — id `7089923423`
- URL: https://arvsystems-ltda.monday.com/boards/7089923423
- Folder: CRM ✅🎯💰
- Grupos: 17 (Lead Inicial, Qualificação, Qualificado, Proposta, Negociação, Fechamento, Perdido, Convertido em Projeto etc — extensão sugerida pelo número)
- **Colunas: 183** (recordista absoluto)
  - Tipos predominantes: 92 `status`, 49 `numbers`, 29 `date`, 11 `formula`, 10 `text`, 5 `board_relation`, 4 `phone`, 4 `email`, 4 `button`, 3 `people`
  - **Colunas connect_boards (5):** `Subelementos`→7225377727, `Atividades`→9760832128 + 18393358566, `Calendário de Visitas`→9758896572, `Serviços e Revendas`→8238302492, `Portfólio de Automação`→8237943720
  - **24 campos planos de contato:** Nome/Cargo/Depto/Tel/Email/LinkedIn × 4 (Contato 1..4)
  - **Campos financeiros (24+):** Valor Estimado, Valor Final, Custo Fixo, Custo Financeiro, Comissão, Markup, CMV, Terceiros, Mão de Obras, IR, CSLL, ICMS, ISS, PIS, COFINS, fórmulas Proposta com/sem Imposto, Antecipação, Previsão Meta Ano/Mês
  - **Campos de qualificação BANT/MEDDIC duplicados:** dois conjuntos (originais `color_mksx*` + revisão `color_mkzj*`/`color_mkzn*`) para problema, resultados, payback, áreas envolvidas, papel do contato, histórico, caderno de encargos, ARV-similar, etc
  - **Sistema de scoring duplicado:** Lead Score + Technical Score + Score da Oportunidade + Temperatura + Classificação + Ação Recomendada
  - **Buttons:** Pesquisar CNPJ, Gerar Leadscore, Gerar Technical Score, Gerar Score
  - Integrações externas: nenhuma identificada
- Items: 1.875
- Última atividade: 2026-05-07
- Boards conectados: 7225377727 (subitens), 9760832128, 18393358566, 9758896572, 8238302492, 8237943720
- Item terminology padrão: "elemento"

### Board: Tarefas — id `9760832128`
- URL: https://arvsystems-ltda.monday.com/boards/9760832128
- Folder: CRM ✅🎯💰
- Grupos: 2 (Tarefas, Tarefas concluidas)
- Colunas: 16 — `name`, `subtasks` (→10040047994), `people` (Criador), `board_relation` (Pipeline →7089923423), 4× `mirror` (Resp. Comercial, Resp. Técnico, Nome do Projeto, LeadID — todos espelham Pipeline), `timeline`, 2× `status` (Tipo de Tarefa com 21 labels: Visita/Reunião/Email/Ligação/Whatsapp/Linkedin/Email/Atualização CRM..., Status), 4× `date`, `text`
- Items: **6.841**
- Última atividade: 2026-05-07
- Views: David, Lilian, Mariana, Mauricio, Santiago (filtros por pessoa)
- Boards conectados: Pipeline (mirror)

### Board: Tarefas Paralelas — id `18390965607`
- URL: https://arvsystems-ltda.monday.com/boards/18390965607
- Folder: CRM ✅🎯💰
- Grupos: 3 (Atividades, Concluidas, Canceladas)
- Colunas: 6 — `name`, `people`, `status` (4 labels), `subtasks` (→18390966883), `timeline`, `date`
- Items: 932
- Última atividade: 2026-05-06
- Boards conectados: nenhum externo

### Board: Calendário de Visitas — id `9758896572`
- URL: https://arvsystems-ltda.monday.com/boards/9758896572
- Folder: CRM ✅🎯💰
- Grupos: 4 (Em planejamento, Agendadas, Concluidas, Canceladas)
- Colunas: 24 — destaque: `subtasks`, `people`, 3× `status` (Status visita, Vendedor com 7 labels, Perfil 8 labels), `location`, 4× `mirror` (Distancia da planta, CEP, CEP Numero, Complemento — espelham Pipeline), `date`, `board_relation` Pipeline →7089923423, `text` LeadID, `phone` etc
- Items: 533
- Última atividade: 2026-05-07
- Boards conectados: Pipeline

### Board: Quadro de Prospecção — id `18399307546`
- URL: https://arvsystems-ltda.monday.com/boards/18399307546
- Folder: CRM ✅🎯💰
- Grupos: 4 (Prospectar, Sem Informações, Prospectados, Descartado)
- Colunas: 8 — `name`, `text` (Estado/Cidade/CNPJ), `people`, `button` "Enviar ao Pipeline", `status` (4 labels), `date`
- Items: **3.709**
- Última atividade: 2026-02-23 (>2 meses sem atividade)

### Board: Tarefas Técnicas — id `18393358566`
- URL: https://arvsystems-ltda.monday.com/boards/18393358566
- Folder: QUADROS AUXILIARES
- Grupos: 3 (A fazer, Concluidas, Cancelada)
- Colunas: 22 — `name`, `people`, 6× `mirror` espelhando Pipeline (Resp. Comercial, Resp. Técnico, Cronograma, Prazo entrega ARV, Prazo entrega Cliente, Status, Lead id, Temperatura, Nome do projeto), 3× `status` (Tarefa 5 labels, Status 6 labels), `numbers` Valor R$, 4× `date`, `formula` Horas, `subtasks` (→18394327801), `board_relation` Pipeline, `text` Descrição, `formula` Empresa
- Items: 184
- Última atividade: 2026-05-07
- Boards conectados: Pipeline

### Board: Entrada de Leads — id `18193210777`
- URL: https://arvsystems-ltda.monday.com/boards/18193210777
- Folder: QUADROS AUXILIARES
- Grupos: 1 (Entrada de Leads)
- Colunas: 10 — `name`, `people`, 2× `status` (Origem 3 labels, Sub Origem 9 labels), `text` CNPJ, `text` Nome, `phone`, `email`, `long_text` Demanda, `date`
- Items: 226
- Última atividade: 2026-05-07
- Possui **FormBoardView** "Entrada de Leads Internos"

### Board: Gestão de Contas — id `18396765892`
- URL: https://arvsystems-ltda.monday.com/boards/18396765892
- Folder: QUADROS AUXILIARES
- Grupos: 1
- Colunas: **62** (idêntica estrutura plana de contatos do Pipeline) — destaque: `people`, 2× `status` (Categoria, Status), 2× `date`, `numbers` Valor vendido, `text` Razão social/CNPJ/CEP/Numero/Complemento, `phone`, 7× `status` (Segmento 10 labels, Funcionarios, Tempo mercado, Plantas, Distancia, Lead score, Classificação 4 labels), 4× blocos de contato (Nome 1..4, Cargo 1..4 com 21 labels, Departamento 1..4 com 18 labels, Influência, LinkedIn, Telefone, E-mail), `board_relation` Pipeline, `mirror` (Espelho de status83 do Pipeline), `numbers` Oportunidades ativas, `date` Prox atividade
- Items: **3** (board novo, ainda subutilizado)
- Última atividade: 2026-05-05
- Boards conectados: Pipeline

### Board: Quotes & Invoices — id `8326289541` *(POTENCIALMENTE INATIVO)*
- URL: https://arvsystems-ltda.monday.com/boards/8326289541
- Folder: root
- Items: **1**
- Última atividade: 2025-01-26 (>15 meses)

---

## Workspace: MCP CRM (id 14592352)
Redesign comercial em curso. Criado 2026-03-07. Owner: Bruno. Descrição: "Substitui o workspace Comercial com estrutura baseada nos UMLs de Vendas. Escopo: Leads, Oportunidades, Orçamentos, Atividades, Contas."
**Todos os 12 boards estão com 1-2 items** — workspace de desenvolvimento, ainda não em produção. Todos com `top_group` "Inativos"/"Canceladas" como default.

### Board: 01_EMPRESAS — id `18402998719`
- Folder: 🏢 Master Data
- Descrição: "Master data de empresas. Base central de todas as organizações no CRM — prospects, leads ativos, clientes e inativos."
- Grupos: 4 (Inativos, Clientes Ativos, Prospects com Oportunidade, Base de Prospecção)
- Colunas: 20 — `name`, `text` CNPJ/Razão Social/Cidade/CEP/Site, 4× `status` (Segmento, Funcionários, Estado, Status Conta — todos placeholder), `numbers` Plantas/Distância/Valor Total, `phone`, 3× `date`, `people` Resp. Comercial, `long_text` Observações, **2× `board_relation`** (Leads →18402999165, Oportunidades →18402999166)
- Items: 1

### Board: 02_CONTATOS — id `18402998722`
- Folder: 🏢 Master Data
- Descrição: "Master data de contatos normalizados. Substitui os 24 campos planos de contato do Pipeline antigo."
- Grupos: 4 (Inativos, Operacionais, Influenciadores, Decisores)
- Colunas: 11 — `name`, 4× `status` (Cargo, Departamento, Influência, Ativo? — placeholder), `email`, `phone`, `text` LinkedIn, `date`, `board_relation` Empresa →18402998719, `long_text`
- Items: 1

### Board: 03_FONTES_CAPTACAO — id `18402998725`
- Folder: 🏢 Master Data
- Descrição: "Origens e canais de captação de leads. Rastreia CAC e taxa de conversão por fonte."
- Grupos: 2 (Canais Inativos, Canais Ativos)
- Colunas: 8 — `name`, 2× `status` (Canal, Origem), `text` Campanha, 4× `numbers` (CAC, Conversão %, Leads Gerados, Oportunidades Geradas)
- Items: 1

### Board: 04_LEADS — id `18402999165`
- Folder: 🎯 Funil Comercial
- Descrição: "Funil pré-vendas. Substitui o Quadro de Prospecção e os grupos Lead Inicial / Qualificação Inicial do Pipeline antigo. Etapas: Prospecção → Primeiro Contato → Qualificação → Qualificado → Descartado."
- Grupos: 5 (Descartado, Qualificado, Qualificação, Primeiro Contato, Prospecção)
- Colunas: 18 — `name`, `text` Lead ID, **3× `board_relation`** (Empresa, Contato Principal, Origem, Oportunidade), 5× `status` (Etapa, Sub-Status, Temperatura, Produto Interesse, Classificação, Motivo Descarte, Próx Atividade), 2× `numbers`, 3× `date`, `people`
- Items: 1

### Board: 05_OPORTUNIDADES — id `18402999166`
- Folder: 🎯 Funil Comercial
- Descrição: "Funil de vendas. Substitui o Pipeline principal. 8 etapas + sub-status contextuais. Gerado a partir da conversão de um Lead qualificado."
- Grupos: **9** (Perdido, Convertido em Projeto, Fechamento, Em Negociação, Proposta Enviada, Desenvolvimento de Proposta, Análise Interna, Qualificação da Oportunidade)
- Colunas: 27 — `name`, **7× `board_relation`** (Lead Origem, Empresa, Contatos, Orçamentos, Tarefas, Visitas, Tarefas Técnicas), 5× `status` (Etapa, Sub-Status, Temperatura, Classificação, Tipo Entrega, Motivo Perda), 2× `people`, 6× `numbers` (Valor Estimado/Projetado/Final, Probabilidade, Score Técnico, Score Oportunidade), 3× `date`, `time_tracking` Tempo na Etapa, `long_text`
- Items: 2

### Board: 06_ORCAMENTOS — id `18402999765`
- Folder: 💰 Orçamentos
- Descrição: "Propostas e orçamentos extraídos do Pipeline. Versioning, cálculo financeiro completo (CMV, markup, impostos). Integra analise-cmv e roi-calculator."
- Grupos: 5 (Rejeitados, Aprovados, Enviados Cliente, Em Elaboração, Group Title)
- Colunas: 25 — `name`, `board_relation` Oportunidade, 3× `status`, 14× `numbers` (Versão, Valor Bruto, CMV, Custo Fixo, Custo Financeiro, Mão Obra, Terceiros, Markup, Comissão, IR, CSLL, ICMS, ISS, PIS, COFINS, Validade), 2× `date`, `file` PDF, **2× `link`** (Link CMV Calculator, Link ROI Calculator — referência a sistemas externos)
- Items: 2

### Board: 07_TAREFAS — id `18402999766`
- Folder: ✅ Atividades
- Descrição: "Log unificado de atividades comerciais. 18 tipos de tarefa. Vinculado a Leads e Oportunidades."
- Grupos: 5
- Colunas: 9 — `name`, 2× `status` (Tipo, Canal), 2× `board_relation` (Lead, Oportunidade), `people`, 2× `date`, `long_text`
- Items: 1

### Board: 08_VISITAS — id `18402999768`
- Folder: ✅ Atividades
- Descrição: "Calendário de visitas de campo. 8 perfis de visita. Relatório pós-visita e próxima ação."
- Grupos: 5
- Colunas: 10 — `name`, 4× `status` (Perfil, Estado, Zona, Próxima Ação), 2× `board_relation` (Lead, Oportunidade), `people`, `date`, `text` Cidade, `long_text` Relatório
- Items: 1

### Board: 09_TAREFAS_TECNICAS — id `18402999770`
- Folder: ✅ Atividades
- Descrição: "Tarefas técnicas vinculadas a Oportunidades. Tipos: Estimativa, Projeção, Proposta, Revisão."
- Grupos: 4
- Colunas: 9 — `name`, 2× `status`, `board_relation` Oportunidade, 2× `people`, 2× `date`, `numbers` Valor, `long_text`
- Items: 1

### Board: 10_CONTAS — id `18402999771`
- Folder: 👥 Contas & Pós-Venda
- Descrição: "Gestão de contas ativas e clientes recorrentes. Health score, NPS médio, oportunidades de cross-sell."
- Grupos: 3
- Colunas: 11 — `name`, 2× `board_relation` (Empresa, Oportunidades), `people`, 3× `numbers` (Projetos Entregues, Valor Total, NPS), 2× `date`, 2× `status` (Health Score, Cross-sell), `long_text`
- Items: 1

### Board: HISTORICO_FASES — id `18402999772`
- Folder: 📊 Auxiliares & Histórico
- Descrição: "Audit trail automático de mudanças de etapa em Leads e Oportunidades. Alimentado por automação — leitura apenas."
- Grupos: 3
- Colunas: 8 — `name`, `status` Entidade, 2× `board_relation` (Lead, Oportunidade), 2× `text`, 2× `date`
- Items: 2

---

## Workspace: Projetos 🚀 (id 9465815)
PM industrial. 10 owners (toda gerência ARV). Criado 2025-01-14.

### Board: Portfólio de Automação 🤖 — id `8237943720` (HUB CENTRAL)
- URL: https://arvsystems-ltda.monday.com/boards/8237943720
- Folder: Portfólio de Projetos
- Grupos: 4 (Novas Automações, Em Execução, Em Garantia, Entregues)
- Colunas: 33 — `name`, `subtasks` (→8804689975), 4× `status` (Produto, Status Projeto 4 labels, Fase do Projeto 10 labels, Complexidade), `button` Gerar Resumo, 3× `people` (Líder Mecânica/Elétrica/Manufatura), 2× `mirror` enormes espelhando 18 boards de cronogramas individuais (Cronograma + Status Macro), 3× `link` externos (CMV, WBS, Cronograma), `formula` Dias sem Reunião, `date` Reunião, 4× `numbers` financeiros (Valor sem Impostos, CMV utilizado), 2× `formula` (Saldo CMV, % CMV), 3× `date` (Entrada, Garantia, Entrega), **9× `board_relation`** (Cronograma do Projeto →19 boards, Ponto Digital, Compras, Abertura de Chamado, Controle Fiscal, Pipeline, Montagem Mecânica, Pendências, Tarefas, link to Portfólio Automações)
- Items: 68 (1 por projeto)
- Última atividade: 2026-05-07
- Limite items: 10.000

### Board: Tarefas 📌 — id `8410467033`
- URL: https://arvsystems-ltda.monday.com/boards/8410467033
- Folder: Controle dos Usuários
- Grupos: 3
- Colunas: 18 — `name`, `subtasks`, `people`, `status`, `mirror` Prazo Pendência, `board_relation` Pendências, `mirror` Projeto, `status` Projeto (24 labels com OS), `status` Fase Cronograma (10 labels), 4× `date`, `numbers` Duração horas, `creation_log`, `checkbox` TAREFA WBS, `mirror` Tipo Pendência, `board_relation` Projeto (→Portfólio), `last_updated`, `checkbox` Task Genérica
- Items: **7.143** (perto do limite 10.000)
- Última atividade: 2026-05-07
- Boards conectados: Pendências, Portfólio Automação
- Views: Mecânica, Elétrica, Manufatura, Administração, Gestão de Pendência, Prazo Ordenado, Tasks genéricas

### Board: Itens Comprados 📦 — id `8251115831`
- URL: https://arvsystems-ltda.monday.com/boards/8251115831
- Folder: Controle dos Usuários
- Grupos: 4 (Pendente, Parcial, Recebidos, Cancelados)
- Colunas: 21 — `name`, 6× `status` (Produto ARV, Status, Entrega, Família 17 labels, Área Responsável), `text` Fornecedor, 2× `numbers` (OC, Valor Pedido/NF), `formula` Diferença, `file` OC PDF, 4× `date`, `board_relation` Projeto →Portfólio, `people`, `subtasks`, `last_updated`
- Items: 509
- Última atividade: 2026-05-07
- Possui **FormBoardView** "FUP DE MATERIAL ARV" (com regras condicionais: tipo Projeto/Serviço/Revenda)

### Board: Pendências 🔥 — id `18394600277`
- URL: https://arvsystems-ltda.monday.com/boards/18394600277
- Folder: Controle dos Usuários
- Grupos: 3 (Novas, Em Aberto, Resolvidas)
- Colunas: 16 — `name`, `subtasks`, `mirror` Status Macro, `status` Status, `date` Prazo, `formula` Dias até Prazo, `dropdown` Característica (Chamado/Planejamento), `text` Subconjunto, `people`, `board_relation` Projeto, 2× `status` (Complexidade 5 labels, Prioridade 5 labels), `long_text`, `date`, `people` Criador, `board_relation` Tarefas →8410467033
- Items: 205
- Última atividade: 2026-05-07
- FormBoardView "Pendências de Reuniões"

### Board: Agendamento de Veículo 🚗 — id `6635591814`
- URL: https://arvsystems-ltda.monday.com/boards/6635591814
- Folder: Controle dos Usuários
- Grupos: 3
- Colunas: 14 — `name`, `subtasks`, 4× `status` (Status Carro 13 labels com placas, Solicitante 28 labels com nomes, Condutor 26 labels, Carro 10 labels), 2× `timeline`/`date`, `text` Descrição, `last_updated`, `creation_log`
- Items: 505
- Última atividade: 2026-05-07
- FormBoardView "Frota ARV"

### Board: Treinamentos — id `5530626624` *(POTENCIALMENTE INATIVO)*
- URL: https://arvsystems-ltda.monday.com/boards/5530626624
- Folder: Controle da Gerência
- Items: 2
- Última atividade: 2026-02-03 (>3 meses)

### Board: Entrada e Saída Material — id `6045625973`
- Folder: Controle da Gerência
- Items: 58
- Última atividade: 2026-05-06
- Colunas: 14 — `name`, `people`, `text` (Cliente, Robot ID, P/N, S/N), 2× `date`, 2× `numbers` (NF Entrada/Saída), `numbers` O.S, 2× `long_text`, `file`
- FormBoardView "Registro de Material"

### Board: Ponto Digital 📅 — id `8251128262`
- URL: https://arvsystems-ltda.monday.com/boards/8251128262
- Folder: Controle da Gerência
- Grupos: 1
- Colunas: 17 — `name`, `people`, `date` (Prazo, Conclusão), `numbers` Quant Horas, `text` Observação, **3× `status` enormes** (Projeto com **40 labels** com OSs, Serviço 16 labels, Revenda 16 labels), `status` Fase Projeto, `status` Produto ARV, `checkbox` Registro por formulário, `status` Colaborador 17 labels, `formula` Conclusão Mês, `board_relation` Portfólio Automação, `subtasks`, `board_relation` Portfólio Serviços/Revendas
- Items: **10.045** (excedeu limite 10.000)
- Última atividade: 2026-03-30 (>1 mês)
- FormBoardView "Ponto Digital 📆" com regras condicionais Projeto/Serviço/Revenda

### Board: Férias coletivas 2025/2026 📆 — id `18236427369`
- Folder: Controle da Gerência
- Items: 66
- Última atividade: 2026-01-19 (>3 meses)

### Board: Cronograma Mariana — id `18408679470`
- URL: https://arvsystems-ltda.monday.com/boards/18408679470
- Folder: root (board novo, sem folder)
- Items: 34
- Última atividade: 2026-05-06
- Colunas: 11 (padrão template cronograma de projeto: subtasks, people, numbers Andamento %, status 5 labels, timeline Cronograma, numbers Dias, dependency, last_updated, board_relation Portfólio, status Trigger Fases)

### Boards de projetos individuais (padrão repetido — 19 projetos × 3 boards cada = ~57 boards)

Cada projeto industrial tem **3 boards padrão** com folder `[OS]` (ex: 01110, 01122, 01128, 01102, 01095, 01138, 01058, 01168, 01171, 01175, 01185, 01187, 01210, 01211, 01212, 01213, 01201, 01205, 2935):
1. **Cronograma do projeto** (`[OS] - [Nome do equipamento]`) — 9 grupos por fase do projeto, ~30-50 items, padrão 11-13 colunas: `subtasks`, `people` Responsável, `numbers` Andamento %, `status` 5 labels, `timeline` Cronograma Real, `dependency`, `board_relation` Portfólio, `status` Trigger Fases. Alguns têm `timeline` Linha de base + `formula` Diferença (snapshot do cronograma para tracking de atrasos)
2. **Mapa de Peças** (`[OS] - Mapa de Peças`) — ~150-200 items, ~25 colunas: peças com `status` Peça (10 labels), `text` Desenho, `numbers` Quant, `status` Operação (10 labels), `status` Tratamento, `status` Fornecedor (8 labels), 5× `numbers` (preços por fornecedor), 2× `formula` (totais), `file` Desenho PDF, `numbers` OC, `status` Conjunto/Orçado
3. **WBS** (`[OS] - WBS`) — ~50 items, 11 colunas: `subtasks`, `people`, `status` Aprovadas/Planejamento, `date` Prazo, `numbers` Duração horas, `status` Avisos, `last_updated`, 2× `date` (Entrada, Promoção), `board_relation` Portfólio

**Pasta vazias (sem boards):** Painéis Mecânica, Painéis Elétrica, Painéis Manufatura, Dashboard Gerenciais

**Sample verificado:**
- 01110 (Panasonic) — Cronograma 44 items + WBS 49 items + Mapa Peças 194 items, último update 2025-10/2025-05 (cronograma) **— possível zumbi**
- 01175 (Hunter-Senninger) — Cronograma 43 items, último update 2026-01-13 (>3 meses)
- 01185 (Festo) — Cronograma 37 items, último update 2026-02-10 (>2 meses)

---

## Workspace: Serviço e Revenda (id 14227361)
Workspace mini, 2 owners (Rodrigo + Bruno). Criado 2026-02-06. **Templates simples — pouco uso ainda.**

### Board: Portfólio Serviço & Revenda — id `18399001155`
- Items: 2 | Última atividade: 2026-02-06
- Grupos: 4 | Colunas: 11 — `name`, `people`, 2× `status` (Status, Produto), 3× `people` (Líderes), 3× `date`, `board_relation` Pendência →18399001504

### Board: Pendência — id `18399001504`
- Items: 1 | Última atividade: 2026-02-24
- Grupos: 3 | Colunas: 11 — `name`, `people`, `status`, `board_relation` Solução →18399001155, `mirror` Status Macro, `dropdown` Tipo Produto (Serviço/Revenda), `text` Descrição, 2× `people`, 2× `date`, `board_relation` Tarefas →18399001544

### Board: Tarefas Gerais — id `18399001544`
- Items: 11 | Última atividade: 2026-02-24
- Grupos: 3 | Colunas: 9 — `name`, `people`, `status`, `date` Prazo, `numbers` Duração, `board_relation` Pendências, `mirror` Tipo Produto, 2× `date`, `last_updated`

---

## Workspace: Administração 🎯 (id 5065308)
ADM/Financeiro/RH. 6 owners. Criado 2024-02-29.

### Board: Garantias — id `9569950485`
- Folder: Viviane | Items: 181 | Última atividade: 2026-05-07
- Grupos: 2 | Colunas: 9 — `name`, `subtasks`, `people`, `status`, **`dropdown` Projeto com 268 labels (cada OS é um label)**, `numbers` Nota, 3× `date`, `text` Descrição

### Board: Notas de Remessas — id `18193541733`
- Folder: Viviane | Items: 44 | Última atividade: 2026-04-27
- Colunas: 10 — `name`, 2× `date`, 2× `text` NF, `dropdown` Cliente/Fornecedor (16 labels), `numbers` CFOP, `text`, `status`, `file`
- 1 grupo
- FormBoardView

### Board: Controle de endividamento fiscal — id `18286172763`
- Folder: Viviane | Items: 17 | Última atividade: 2025-11-17 (>5 meses, **POTENCIALMENTE INATIVO**)
- Grupos: 1 | **Colunas: 108** (106× `numbers` + name + formula — planilha financeira)

### Board: Ponto digital — id `18289399220` (ADM, paralelo ao do Projetos)
- Folder: Viviane | Items: **8.154** | Última atividade: 2026-05-07
- Grupos: 1 | Colunas: 19 — agregado calculado a partir de 8251128262 (board_relation Ponto Digital), com mirrors (Dono, Projeto, Data Conclusão, horas), formulas (VALOR UNITÁRIO 2025/2026 com if-else gigantes por colaborador, Equipe, Membros), `board_relation` Tarefas 📌, mirrors (Projetos novos, Duração, Dono da tarefa, Conclusão), subitems
- **Sistema de cálculo de custo de mão-de-obra com tabela de R$/hora hardcoded em fórmulas** (R$ 46-129/hora por nome de pessoa)

### Board: Planejamento Fiscal — id `6501620314`
- Folder: Viviane | Items: 31 | Última atividade: 2026-05-06
- Colunas: 8 — `name`, `subtasks`, `people`, `status` (4 labels), `status` Recorrência (6 labels), 2× `date`, `status` Grupo

### Board: Controle Fiscal — id `6883862142`
- Folder: Viviane | Items: 106 | Última atividade: 2026-05-07
- Grupos: 3 (Projetos, Serviços, Revendas) | Colunas: 17 — `name`, `subtasks`, `people`, `status`, `text` Orçamento, `board_relation` →Portfólio + Serviços/Revendas, `mirror` Grupo, 4× `date`, 2× `formula` (Planejado vs Real, Planejado vs Faturado), `text` NF, `board_relation` Eventos Financeiros →Previsão+Efetivação, 2× `mirror` (Valor Total Parcelas, Andamento Pagamento)

### Board: Efetivação de Parcelas — id `6985266851`
- Folder: Viviane | Items: 225 | Última atividade: 2025-07-11 (>9 meses, **POTENCIALMENTE ZUMBI**)
- Grupos: 3 | Colunas: 12 — `name`, `people`, `board_relation` Controle Fiscal, `status` Fonte, `status` Status (Pago/Pendente), `numbers` Valor Parcela, `date`, `dropdown` Projeto (40 labels), `status` Fase, `date`, `last_updated`, `formula`

### Board: Previsão de Parcelas — id `6200322598`
- Folder: Viviane | Items: 259 | Última atividade: 2026-05-07
- Grupos: 3 | Colunas: 13 — `name`, `people`, `board_relation` Controle Fiscal, `status` Fonte, `numbers` Valor, 3× `date` (Original/Cronograma/Efetivação), `formula` Diferença, `status`, `dropdown` Projeto (41 labels), `status` Fase, `last_updated`, `date`

### Board: Tarefas VN — id `9454416367` (Viviane)
- Folder: Viviane | Items: 669 | Última atividade: 2026-05-07
- Grupos: 9 (Solicitadas, Diárias, Semanais, Quinzenais, Mensais, Trimestrais, Semestrais, Anuais, Concluidas)
- Colunas: 8 — `name`, `subtasks`, `people`, `status`, `timeline`, `status` Prioridade, 2× `date`

### Board: Renovação de Contrato — id `6864990943`
- Folder: Camila | Items: 36 | Última atividade: 2025-06-26 (>10 meses, **POTENCIALMENTE INATIVO**)
- Colunas: 9 — `name`, `subtasks`, `people`, `status`, `status` Recorrência, `timeline`, `text`, 2× `date`

### Board: Tarefas CM — id `9454092291` (Camila — mesmo template VN)
- Folder: Camila | Items: 1.042 | Última atividade: 2026-03-23 (>1 mês)

### Board: Veiculos ARV (Livre) — id `9622751861`
- Folder: Kaique | Items: 5 | Última atividade: 2025-08-07 (>9 meses, **POTENCIALMENTE INATIVO**)
- Colunas: 14 (placa, renavam, datas contrato, manutenções)

### Board: TESTE — id `18089454787`
- Folder: Kaique | Items: 2 | Última atividade: 2025-10-01 (>7 meses, **CLARAMENTE INATIVO/TESTE**)

### Board: 5S — id `18396179683`
- Folder: Kaique | Items: 13 | Última atividade: 2026-01-29 (>3 meses)
- Colunas: 4

### Board: Tarefas QIK — id `9454098359` (Kaique — mesmo template)
- Folder: Kaique | Items: 402 | Última atividade: 2026-05-04
- Mesmo template das Tarefas VN/CM (8 grupos por recorrência, mesmas colunas)

### Boards do folder Jamylli (RH/Talentos)
- **Fornecedores Whatsapp** (`9962749951`) — 18 items, 2025-10-08 (>6 meses, **INATIVO**), FormBoardView
- **Vagas Whatsapp** (`9962504415`) — 2 items, 2025-10-08 (>6 meses, **INATIVO**), FormBoardView
- **Controle de Integrações** (`10028005931`) — 74 items, 2026-04-08 (~1 mês), 8 colunas inclui `dropdown` Cliente
- **Controle de Estoque de Uniforme** (`9374147972`) — 20 items, 2025-11-03 (>6 meses, **INATIVO**), 14 grupos por tipo/tamanho
- **Controle de Colaboradores** (`9374132077`) — 36 items, 2025-07-21 (>9 meses, **INATIVO**), 12 grupos por mês de aniversário
- **Tarefas JM** (`9374164002`) — 1.067 items, 2026-05-07 (mesmo template das Tarefas VN/CM/QIK)
- **Controle de Estoque de EPI** (`9395246275`) — 25 items, 2025-06-25 (>10 meses, **INATIVO**)
- **Controle ASO** (`9395660820`) — 19 items, 2025-12-08 (>5 meses, **INATIVO**)

### Board: Tarefas CT — id `9454397461` (Cintia — mesmo template)
- Folder: Cintia | Items: 142 | Última atividade: 2026-05-06

### Board: Férias Coletivas Fornecedores — id `7806876316`
- Folder: Controle ADM | Items: 61 | Última atividade: 2025-06-25 (>10 meses, **INATIVO**)

### Board: Calendário ADM — id `9405322155`
- Folder: Controle ADM | Items: 15 | Última atividade: 2025-06-25 (>10 meses, **INATIVO**)
- FormBoardView

---

## Padrões observados

### Padrão 1: Tarefas pessoais por funcionário
**5 boards quase idênticos**, um por administrativo: Tarefas VN (669 items), Tarefas CM (1.042), Tarefas QIK (402), Tarefas JM (1.067), Tarefas CT (142). Mesma estrutura: 8-9 grupos por recorrência (Solicitadas/Diárias/Semanais/Quinzenais/Mensais/Trimestrais/Semestrais/Anuais/Concluidas), mesmas 8 colunas (people, status 5 labels, timeline, prioridade 4 labels, 2 datas, subtasks). **Total: 3.322 items somados em 5 boards funcionalmente equivalentes.**

### Padrão 2: Boards de projeto com 3-template
Cada OS de projeto tem **3 boards individuais**: Cronograma + WBS + Mapa de Peças. Identificados 19 projetos = ~57 boards. Estrutura totalmente padronizada (mesmas colunas com mesmos IDs, ex: `pessoas8`, `n_meros_mkm94kqb`, `in_cio2`). Boards Cronograma fazem reflection no Portfólio de Automação (mirror gigante com 18 board_ids).

### Padrão 3: Mirrors em cascata Pipeline → Tarefas/Visitas/Atividades
No CRM legado, **toda informação central vive no Pipeline**, e os boards de Tarefas/Visitas/Tarefas Técnicas usam `mirror` para refletir Resp. Comercial, Resp. Técnico, Cronograma, LeadID, Status. Resultado: alterar dados no Pipeline propaga via mirror.

### Padrão 4: Estrutura plana de contatos (4× duplicação)
Pipeline e Gestão de Contas armazenam até **4 contatos por empresa em 24 colunas planas** (Nome 1/2/3/4, Cargo 1/2/3/4, Departamento 1/2/3/4, Influência 1/2/3/4, LinkedIn 1/2/3/4, Telefone 1/2/3/4, Email 1/2/3/4). MCP CRM normaliza isso para board `02_CONTATOS` com relação N-para-1 a `01_EMPRESAS`.

### Padrão 5: Statuses gigantes com OSs como labels
Pelo menos 5 boards usam `status` ou `dropdown` com **40+ labels onde cada label é uma OS individual**: Tarefas 📌 (24 labels), Ponto Digital (40 labels), Garantias (268 labels), Efetivação Parcelas (40 labels), Previsão Parcelas (41 labels). Cresce a cada novo projeto. Anti-pattern para escala.

### Padrão 6: Sistemas de scoring/qualificação duplicados no Pipeline
Pipeline tem **dois conjuntos** de qualificação BANT/MEDDIC (originais `color_mksx*` + revisão `color_mkzj*`/`color_mkzn*`), 4 botões diferentes para gerar score (Lead Score, Technical Score, Score Oportunidade, Pesquisar CNPJ), e múltiplas colunas de score/temperatura/classificação coexistindo.

### Padrão 7: Cálculo de custo de mão-de-obra hardcoded
Board `Ponto digital` (ADM, 18289399220) calcula custo total via fórmula com if-else aninhado mapeando **nome de pessoa → R$/hora** (R$ 46-129/h), com tabela 2025 e 2026 separadas. Atualizar custo = editar fórmula.

### Padrão 8: MCP CRM com top_group "Inativos" como default
Todos os 12 boards do MCP CRM têm `top_group` apontando para grupos "Inativos"/"Canceladas" — provável bug de configuração (deveriam apontar para entrada/novo).

### Padrão 9: Statuses placeholder no MCP CRM
Quase todos os 50+ campos `status` do MCP CRM ainda estão com labels default "Em andamento/Feito/Parado" (não foram configurados). Não é template funcional ainda — apenas estrutura.

---

## Boards potencialmente inativos / zumbis

| Board | Workspace | Items | Última atividade | Idade |
|-------|-----------|-------|------------------|-------|
| Quotes & Invoices | Comercial | 1 | 2025-01-26 | >15 meses |
| Treinamentos | Projetos | 2 | 2026-02-03 | >3 meses |
| Férias coletivas 2025/2026 | Projetos | 66 | 2026-01-19 | >3 meses |
| Renovação de Contrato | ADM | 36 | 2025-06-26 | >10 meses |
| Veiculos ARV (Livre) | ADM | 5 | 2025-08-07 | >9 meses |
| TESTE | ADM | 2 | 2025-10-01 | >7 meses |
| Fornecedores Whatsapp | ADM | 18 | 2025-10-08 | >6 meses |
| Vagas Whatsapp | ADM | 2 | 2025-10-08 | >6 meses |
| Controle Estoque Uniforme | ADM | 20 | 2025-11-03 | >6 meses |
| Controle de Colaboradores | ADM | 36 | 2025-07-21 | >9 meses |
| Controle de Estoque EPI | ADM | 25 | 2025-06-25 | >10 meses |
| Controle ASO | ADM | 19 | 2025-12-08 | >5 meses |
| Férias Coletivas Fornecedores | ADM | 61 | 2025-06-25 | >10 meses |
| Calendário ADM | ADM | 15 | 2025-06-25 | >10 meses |
| Controle de endividamento fiscal | ADM | 17 | 2025-11-17 | >5 meses |
| Efetivação de Parcelas | ADM | 225 | 2025-07-11 | >9 meses |
| 01110 - WBS | Projetos | 49 | 2025-05-27 | >12 meses |
| 01110 - Mapa de Peças | Projetos | 194 | 2025-05-15 | >12 meses |
| 01110 - Cronograma | Projetos | 44 | 2025-10-03 | >7 meses |

**Observação:** vários boards de projetos antigos (01058, 01095, 01102, 01122, 01128, 01138, 01168, 01171) provavelmente têm padrão similar (projeto entregue, sem novas atividades) — não verificados individualmente para economizar requests.

---

## Notas sobre coleta

- 2 chamadas `get_board_info` retornaram payloads >limite e foram salvas em arquivos temp; extraídas via PowerShell parsing local: Pipeline (7089923423, 131k chars) e Controle de endividamento fiscal (18286172763, 69k chars)
- Boards de cronograma de projetos individuais foram amostrados (4 dos 19 projetos verificados em detalhe) — restantes inferidos pelo padrão estritamente repetido
- **Contagem de automações não disponível via MCP `get_board_info`** — campo `automations` não retornado pela API. Para contar automações seria necessário inspeção manual no Monday UI ou via GraphQL específico (`get_graphql_schema` carregaria a definição mas não foi chamado para preservar tokens)
- Boards de subitems (`Subelementos de X`) não foram inventariados — seguem template padrão Monday (4 colunas: name, person, status, date)
