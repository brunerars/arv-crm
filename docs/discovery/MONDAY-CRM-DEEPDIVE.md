# Monday CRM Deep-Dive — Comercial 💰 + MCP CRM
Coletado em: 2026-05-07 · Fonte: Monday MCP (`get_board_info` por board) · Read-only

## 0. Sumário

- Boards inventariados: **9 do Comercial 💰** (incluindo subitems Pipeline) + **12 do MCP CRM** = 21 boards
- Boards com schema campo-a-campo neste doc: **6 do Comercial** (Pipeline 183 cols, Tarefas 16, Calendário Visitas 24, Tarefas Técnicas 22, Gestão de Contas 62, Entrada de Leads + Quadro de Prospecção resumidos) + **12 do MCP CRM** (10–27 cols cada)
- Total de colunas catalogadas: **~470**
- Buracos de design detectados (conceito existe em `dashboards.txt`/`travas.txt` mas nenhum dos workspaces resolve bem): **6 críticos**
- **Pipeline** = 1.873 items, 17 grupos de funil, 183 colunas — concentra ~80% do valor de discovery
- **Workspace MCP CRM**: 12 boards, 14 items totais (vazios), todos `status` em labels-placeholder, todos `top_group=Inativos` — estrutura é o produto

---

## 1. Workspace `Comercial 💰` (legado, id 7490918)

CRM em uso por 10 vendedores. Criado 2024-07-29 por Bruno. Owners listados nos boards: Bruno, Maurício Flausino Junior, Lilian Costa, Mariana Constantinou, Camila Correa, Isabella Valverde Chaves, David, Santiago, Alex, Gabriel.

### 1.1 Lista completa de boards

| # | Board | id | Items | Cols | Folder | Última atividade |
|---|-------|----|------:|-----:|--------|------------------|
| 1 | **Pipeline** | 7089923423 | **1.873** | **183** | CRM ✅🎯💰 | 2026-05-07 |
| 2 | Subelementos de Pipeline | 7225377727 | (subitems) | — | root | — |
| 3 | **Tarefas** | 9760832128 | 6.860 | 16 | CRM ✅🎯💰 | 2026-05-07 |
| 4 | Subelementos de Tarefas | 10040047994 | (subitems) | 4 | root | — |
| 5 | **Tarefas Paralelas** | 18390965607 | 932 | 6 | CRM ✅🎯💰 | 2026-05-06 |
| 6 | Subelementos de Tarefas Paralelas | 18390966883 | (subitems) | — | root | — |
| 7 | **Calendário de Visitas** | 9758896572 | 533 | 24 | CRM ✅🎯💰 | 2026-05-07 |
| 8 | Subelementos de Calendário de Visitas | 9758896713 | (subitems) | 4 | root | — |
| 9 | **Quadro de Prospecção** | 18399307546 | 3.709 | 8 | CRM ✅🎯💰 | 2026-02-23 (>2m sem atividade) |
| 10 | **Tarefas Técnicas** | 18393358566 | 184 | 22 | QUADROS AUXILIARES | 2026-05-07 |
| 11 | Subelementos de Tarefas Técnicas | 18394327801 | (subitems) | — | root | — |
| 12 | **Entrada de Leads** | 18193210777 | 226 | 10 | QUADROS AUXILIARES | 2026-05-07 |
| 13 | **Gestão de Contas** | 18396765892 | 3 | 62 | QUADROS AUXILIARES | 2026-05-05 |
| 14 | Quotes & Invoices | 8326289541 | 1 | — | root | 2025-01-26 (>15m, **MORTO**) |

**5 boards mais relevantes (catalogados a fundo abaixo):** Pipeline, Tarefas, Calendário de Visitas, Tarefas Técnicas, Gestão de Contas. Quadro de Prospecção (3.709 items mas estrutura simples) é resumido. Tarefas Paralelas e Entrada de Leads são pequenos e resumidos.

### 1.2 Pipeline (id `7089923423`) — DEEP-DIVE

- URL: https://arvsystems-ltda.monday.com/boards/7089923423
- Folder: CRM ✅🎯💰 · item_terminology: "elemento" · items_limit: 100.000
- **183 colunas · 17 grupos · 1.873 items · last update 2026-05-07T18:56:35Z**
- Owners: Bruno (creator), Maurício Flausino Junior, Lilian Costa, Mariana Constantinou, Camila Correa, Isabella Valverde Chaves
- Subitems board: `7225377727`

**Grupos (17 — funil completo):**
1. Lead Inicial (`topics`) — top_group default
2. Qualificação Inicial (`group_title`)
3. Qualificação da Oportunidade (`novo_grupo83063__1`)
4. Análise Interna (`novo_grupo50616__1`)
5. Estimativa Orçamentaria (`novo_grupo17433__1`)
6. Estimativa em Conversão (`group_mkrhbmj7`)
7. Projeção Orçamentária (`novo_grupo7798__1`)
8. Projeção em Conversão (`novo_grupo44966__1`)
9. Passagem Pré Vendas - Vendas (`group_mkrd5vx5`)
10. Desenvolvimento de Proposta (`group_mkswfz5g`)
11. Proposta Enviada (`group_mkswvtc`)
12. Proposta em Análise Técnica (`group_mksw408e`)
13. Proposta em Análise Comercial (`group_mkswcwna`)
14. Proposta em Negociação (`group_mkswcx7x`)
15. Emissão do Pedido de Compra (`group_mkswn7r2`)
16. Pedido Convertido em Venda (`novo_grupo__1`)
17. Leads Descartados (DL) (`novo_grupo36134__1`)

**Schema campo-a-campo (183 colunas, em ordem):**

| # | id | title | type | detalhe |
|---|----|-------|------|---------|
| 1 | `name` | Name | name | — |
| 2 | `subelementos__1` | Subelementos | subtasks | board=7225377727 |
| 3 | `text_mksybz8v` | Nome do Projeto | text | — |
| 4 | `status` | **Etapa do Pipeline** | status | **20 labels:** Pedido Convertido em Venda; Leads Descartados (DL); Estimativa Orçamentaria; Estimativa em Conversão; Qualificação da Oportunidade; Análise Interna; Lead Inicial; Passagem Pré Vendas - Vendas; Projeção Orçamentária; Projeção em Conversão; Qualificação Inicial; Passagem Técnico-Comercial; Desenvolvimento de Proposta; Proposta Enviada; Proposta em Análise Técnica; Proposta em Análise Comercial; Proposta em Negociação; Emissão do Pedido de Compra; Registro de Projeto Pendente; Projeto Registrado |
| 5 | `long_text_mksxf4sk` | Descrição atual ou ideal da demanda | long_text | — |
| 6 | `multiple_person_mksf93j3` | Resp. Próx. Atividade | people | — |
| 7 | `person` | Resp. Comercial | people | — |
| 8 | `multiple_person_mks9bx3` | Resp. Técnico | people | — |
| 9 | `text_mkswdjej` | Razão Social | text | — |
| 10 | `texto__1` | **Nome do Contato 1** | text | bloco contato 1/4 |
| 11 | `telefone5__1` | Telefone / WhatsApp | phone | bloco contato 1/4 |
| 12 | `e_mail4__1` | E-mail | email | bloco contato 1/4 |
| 13 | `date_mkswn328` | Data da Ult. Atividade | date | — |
| 14 | `data` | Data de Entrada Pré Vendas | date | — |
| 15 | `date_mkv0wpbb` | Data de Entrada Vendas | date | — |
| 16 | `color_mkswyrf9` | Cargo Contato 1 | status | 21 labels (Gerente, Diretor, Coordenador, Supervisor, Engenheiro, Sem Informação, Comprador, Técnico, Analista, Sócio/Proprietário, Estagiário, Consultor, Assistente, Aprendiz, Especialista, Líder, Operador, Inspetor, CEO, Representante, Encarregado) |
| 17 | `color_mksw1c8f` | Departamento Contato 1 | status | 23 labels (Produção, Engenharia, Compras, Manutenção, Comercial, Sem Info, Diretoria, T.I, Inovação, Administrativo, Financeiro, Qualidade, Logística, Segurança Trab, Automação, Projetos, Processos, Vendas, PCP, Jurídico, Industrial, Operações, Executivo) |
| 18 | `color_mksw6w9r` | Nível de Influência | status | 6 labels (Apoia levantamento de dados; Executa tarefas operacionais; Participa da recomendação; Influência técnica/financeira; Decisor final/Comitê; Sem Info) |
| 19 | `texto3__1` | CNPJ | text | — |
| 20 | `button_mkw4n6q4` | Pesquisar CNPJ? | button | enriquecimento via integração |
| 21 | `text_mkv19nk3` | CEP | text | — |
| 22 | `text_mkv5d6xh` | Número | text | — |
| 23 | `text_mkt2js0v` | Complemento de endereço | text | — |
| 24 | `phone_mkswx96x` | Telefone Fixo | phone | — |
| 25 | `text_mkswskxg` | Linkedin | text | da empresa |
| 26 | `color_mksa4qtt` | Segmento de Mercado | status | 10 labels (Eletroeletrônica; Automotiva & Máq Pesadas; Farmacêutica; Higiene & Beleza; Alimentícia; Embalagens; Fundição & Metalurgia; Defesa & Segurança; Bens Duráveis; Outros) |
| 27 | `color_mksab6mj` | Quantidade de Funcionários | status | 3 labels (100-500; +500; <100) |
| 28 | `color_mksaqv72` | Tempo no Mercado | status | 3 labels (5-10 anos; +10 anos; <5 anos) |
| 29 | `color_mksa19z1` | Nº de Plantas Industriais | status | 4 labels (2-3; +3; 1; N/A) |
| 30 | `color_mksa5jms` | Distância da Planta | status | 3 labels (201-800 km; Até 200 km; Acima de 800 km) |
| 31 | `button_mkszf40g` | Gerar Leadscore ✅ | button | — |
| 32 | `numeric_mksaxarq` | 🧮 Lead Scoring | numbers | calculado pelo botão |
| 33 | `color_mksacpmx` | 🏆 Classificação de Leads | status | 4 labels (B–Potencial; A–Ideal; D–Fora do ICP; C–Baixo perfil) |
| 34 | `text_mkswjyt7` | **Nome do Contato 2** | text | bloco contato 2/4 |
| 35 | `phone_mkswrte1` | Telefone / WhatsApp Contato 2 | phone | bloco 2/4 |
| 36 | `email_mkswr508` | E-mail Contato 2 | email | bloco 2/4 |
| 37 | `color_mkswg25h` | Cargo Contato 2 | status | **33 labels** (superset do Cargo 1, sujou com variantes "Engenheiro de Processos", "Engenharia Manutenção", "Analista de Manutenção", "Gestor", etc — labels duplicadas/inconsistentes) |
| 38 | `color_mkswmpvb` | Departamento Contato 2 | status | 18 labels |
| 39 | `color_mkswwfxb` | Nível de Influência Contato 2 | status | 6 labels (mesmo conjunto de Influência) |
| 40 | `text_mkswqjk1` | Linkedin Contato 2 | text | — |
| 41 | `text_mksww1h5` | **Nome do Contato 3** | text | bloco contato 3/4 |
| 42 | `phone_mkswcz3v` | Telefone / WhatsApp Contato 3 | phone | bloco 3/4 |
| 43 | `email_mkswfq2t` | E-mail Contato 3 | email | bloco 3/4 |
| 44 | `color_mkswbwqb` | Cargo Contato 3 | status | 21 labels (typo "Assitente") |
| 45 | `color_mkswy5fr` | Departamento Contato 3 | status | 18 labels |
| 46 | `color_mksws92c` | Nível de Influência Contato 3 | status | 6 labels |
| 47 | `text_mksw9qmt` | Linkedin 3 | text | — |
| 48 | `text_mkswwzt` | **Nome do Contato 4** | text | bloco contato 4/4 |
| 49 | `phone_mkswf758` | Telefone / WhatsApp Contato 4 | phone | bloco 4/4 |
| 50 | `email_mkswjr7c` | E-mail Contato 4 | email | bloco 4/4 |
| 51 | `color_mksww5ca` | Cargo Contato 4 | status | 21 labels |
| 52 | `color_mksw5ce7` | Departamento Contato 4 | status | 18 labels (typos "Operaçôes", "Logistica", "Indutrial") |
| 53 | `color_mksws6z5` | Nível de Influência Contato 4 | status | 6 labels |
| 54 | `text_mkswtdt0` | Linkedin 4 | text | — |
| 55 | `color_mksw655h` | **Origem** | status | **15 labels (com duplicidades):** Pré Vendas; Vendas; Ativa.Ai; Busca Orgânica; Indicação Parceiros; Indicação Clientes; Tráfego Pago (×2); Solicitação do Cliente; Ativa; Visita; Contato Vendedora; Passiva; Tráfego Direto; Indicação |
| 56 | `color_mksw880q` | **Sub-Origem** | status | 23 labels (Campanha Geral; Pré-Vendas; Vendas; Busca Orgânica; Anúncio; Prospecção Ativa - Vendas; Prospecção Ativa - Pré Vendas; Base de Leads Ativos - Vendas; Base de Leads Inativos - Pré Vendas; Solicitação do Cliente; Ativa.Ai; Festo; Eventos e Feiras; Colaborador; Chatbot ARV; Andre Souza Ex MM; Tráfego Pago; Parceiro; AGF; Omron; Luis Silva; Base de Leads Inativos; Cliente) |
| 57 | `status83__1` | Produto | status | 5 labels (Apresentação; Prospecção Ativa (Reativação); Serviço; Automação; Revenda) |
| 58 | `color_mksxq7he` | Área de Atuação | status | 9 labels (Máquinas Especiais p/ Automação; Linhas de Montagem; Controle Qualidade; Embalagem; Logística Interna; Soluções Robóticas; Consultoria; Suporte/Otimização; Apresentação) |
| 59 | `color_mktjwzaz` | **Próx. Atividade** | status | 24 labels (mesmo conjunto do Tarefas.Tipo + alguns duplicados como "Reunião agendada" + "Reunião Agendada", "No-Show" + "No-Show 😢") |
| 60 | `date_mksa17zw` | Data Próx. Atividade | date | — |
| 61 | `color_mksxmwc0` | Tipo de Entrega | status | 4 labels (Projeção; Proposta; Estimativa; Apresentação) |
| 62 | `color_mksxe29g` | É melhoria de processo ou meio de produção? | status | 2 labels (Meio de Produção; Melhoria de Processo) |
| 63 | `color_mksxwxq9` | O processo já existe ou será implementado? | status | 2 labels |
| 64 | `color_mksxt3k3` | Existe um valor estimado ou teto de investimento? | status | 5 labels (BANT-budget v1) |
| 65 | `color_mksxskzt` | Investimento já foi aprovado internamente? | status | 5 labels (BANT-budget v1) |
| 66 | `color_mksx5yf3` | Prazo desejado para implantação? | status | 5 labels (BANT-time v1) |
| 67 | `color_mksxg6bp` | Prazo estimado para emissão do pedido? | status | 5 labels (BANT-time v1) |
| 68 | `color_mksx1bgp` | Qual problema ou desafio será resolvido? | status | 5 labels (MEDDIC-Pain v1) |
| 69 | `color_mksxtvdx` | Quais resultados esperados? | status | 5 labels (MEDDIC-Metrics v1) |
| 70 | `color_mksxwvzv` | Payback esperado? | status | 5 labels (MEDDIC-Metrics v1) |
| 71 | `color_mksx8ht7` | Quais áreas estão envolvidas? | status | 5 labels (MEDDIC-Champion v1) |
| 72 | `color_mksxsrng` | Papel do contato na decisão | status | 5 labels (MEDDIC-Decision v1) |
| 73 | `color_mksxm337` | Histórico com automação industrial | status | 5 labels |
| 74 | `color_mksxpmnv` | Possui caderno de encargos? | status | 5 labels (v1) |
| 75 | `color_mksxmzfq` | Já comprou com a ARV? | status | 5 labels |
| 76 | `color_mksxr12n` | ARV já desenvolveu solução similar? | status | 5 labels (v1) |
| 77 | `color_mksxbaex` | Clareza técnica esperada | status | 5 labels |
| 78 | `color_mksx8geh` | Status da Projeção | status | 3 labels (Em andamento; Feito; Parado) — **placeholder default Monday** |
| 79 | `color_mksxkea4` | Projeção Aprovada Internamente? | status | 2 labels (Sim/Não) |
| 80 | `n_meros44__1` | Valor Projetado | numbers | R$ |
| 81 | `color_mksxvwrc` | Projeção Validada com Resp. Comercial? | status | 2 labels |
| 82 | `color_mksxqt8f` | É cliente ARV | status | 2 labels |
| 83 | `color_mksxxr7x` | Informações Finais do Cliente? | status | 2 labels |
| 84 | `color_mksxvkcz` | Nivel de Aderência? | status | 3 labels (Média/Alta/Baixa) |
| 85 | `color_mksxyht2` | Nível de Complexidade? | status | 3 labels (Média/Alta/Baixa) |
| 86 | `timerange_mksx6wg8` | Cronograma da Proposta | timeline | — |
| 87 | `color_mksxkqwz` | Status (geral da oportunidade) | status | 7 labels (Fazendo; Feito; Parado; Em Aprovação; Revisão; Cancelada; Esperando retorno) |
| 88 | `numeric_mksxe7zk` | Valor Estimado (R$) | numbers | — |
| 89 | `numeric_mksx2yc6` | Valor Final | numbers | R$ |
| 90 | `numeric_mksxbxfb` | Nº de Revisão | numbers | — |
| 91 | `color_mksxt903` | **Motivo do Descarte** | status | **17 labels (com duplicatas):** Oportunidade Imatura; Falta de Qualificação; Inviabilidade Técnica (×2); Objeções Comerciais; Decisão do Cliente (×2); Perda por Inércia; Outros; Falta de Interação; Preço Incompatível; Cadastro/Score/Compliance; Baixo ICP; Falta Qualificação/Info; Perda Concorrente; On Hold; Sem Oportunidade Identificada |
| 92 | `direct_doc_mksaegmg` | monday Doc v2 | direct_doc | — |
| 93 | `numeric_mksy1zy4` | Chance de Conversão | numbers | unit % |
| 94 | `date_mkye4yvc` | Data Criação de Orçamento | date | — |
| 95 | `date_mksys9x6` | Data Prevista de Vendas | date | — |
| 96 | `numeric_mksz4237` | Antecipação | numbers | unit % |
| 97 | `date_mktcs7zw` | Data Recebimento Antecipação | date | — |
| 98 | `numeric_mksyrryy` | **Custo Fixo** | numbers | R$ — bloco financeiro |
| 99 | `numeric_mksycfae` | Custo Financeiro | numbers | R$ |
| 100 | `numeric_mksyqzqr` | Comissão | numbers | R$ |
| 101 | `numeric_mksypp34` | Markup | numbers | R$ |
| 102 | `numeric_mksyv759` | CMV | numbers | R$ |
| 103 | `numeric_mksyrsev` | Terceiros | numbers | R$ |
| 104 | `numeric_mksyc1vw` | Mão de Obras | numbers | R$ |
| 105 | `numeric_mksy3e80` | IR | numbers | R$ (valor, não %) |
| 106 | `numeric_mksyr7gt` | CSLL | numbers | R$ |
| 107 | `numeric_mksy27nf` | ICMS | numbers | R$ |
| 108 | `numeric_mksy99tc` | ISS | numbers | R$ |
| 109 | `numeric_mksyrsgs` | PIS | numbers | R$ |
| 110 | `numeric_mksye7da` | COFINS | numbers | R$ |
| 111 | `formula_mkszg7rf` | Proposta com Imposto | formula | `SUM(CMV, MãoObras, Terceiros, CustoFixo, Comissão, CustoFin, Markup, IR, CSLL, ICMS, PIS, COFINS, ISS)` |
| 112 | `formula_mkszj1d2` | Proposta sem Imposto | formula | `SUM(CMV, MãoObras, Terceiros, CustoFixo, Comissão, CustoFin, Markup, IR, CSLL)` *(inclui IR/CSLL — possível bug semântico)* |
| 113 | `formula_mkszhj55` | Composição Meta de Vendas | formula | `SUM(CustoFixo, CustoFin, Comissão, Markup, MãoObras)` |
| 114 | `formula_mkszbz89` | Previsão com Imposto | formula | `MULTIPLY(Proposta com Imposto, Chance de Conversão)` |
| 115 | `formula_mkszwn3x` | Previsão sem Imposto | formula | `MULTIPLY(Proposta sem Imposto, Chance de Conversão)` |
| 116 | `formula_mkszg3zx` | Previsão Meta de Vendas | formula | `MULTIPLY(Composição Meta, Chance de Conversão)` |
| 117 | `formula_mksz9h3` | **Previsão Meta no Ano** | formula | `MULTIPLY(DIVIDE({Previsão Meta}, 7562285.08), 100)` — **meta anual hardcoded R$ 7.562.285,08** |
| 118 | `formula_mkt53wfv` | **Previsão Meta no Mês** | formula | `ROUND(MULTIPLY(DIVIDE({Previsão Meta}, 630190.59), 100), 1)` — **meta mensal hardcoded R$ 630.190,59 = anual/12** |
| 119 | `formula_mktcfwg2` | Antecipações Confirmadas | formula | `IF(Chance==100%, ProstSemImp*Chance*Antecip, "Oportunidade Não Convertida")` |
| 120 | `formula_mktc8ntd` | Antecipações Previstas | formula | `IF(Chance<100%, ProstSemImp*Chance*Antecip, "Oportunidade Convertida 🥇")` |
| 121 | `date_mkt4ttsf` | Data Conclusão | date | — |
| 122 | `texto0__1` | **Lead ID** | text | identificador alternativo, vai como mirror para todos os boards filhos |
| 123 | `numeric_mktde1w6` | META LEADS (NÃO APAGAR) | numbers | **valor zumbi/meta inline em coluna numbers** |
| 124 | `board_relation_mktjy6x8` | Atividades | board_relation | boards: 9760832128 (Tarefas), 18393358566 (Tarefas Técnicas) |
| 125 | `board_relation_mkttdz1k` | Calendário de Visitas | board_relation | board: 9758896572 |
| 126 | `board_relation_mkvd9n3m` | Serviços e Revendas | board_relation | board: 8238302492 (workspace Serviço e Revenda) |
| 127 | `color_mkw946r6` | Foi Enviado ao Cliente? | status | Sim/Não — TRAVA Estimativa em Conversão |
| 128 | `date_mkw97k45` | Data de Envio | date | TRAVA Estimativa em Conversão |
| 129 | `color_mkwbpk1g` | Dentro da faixa de investimento? | status | Sim/Não |
| 130 | `color_mkwhksae` | Aprovado pelo Comitê | status | Sim/Não |
| 131 | `date_mkwhhrc0` | Data de reunião de apresentação | date | — |
| 132 | `color_mkwhe726` | **Proposta Enviada ao Cliente** | status | Sim/Não — TRAVA Proposta em Análise Técnica |
| 133 | `color_mkwhn5yv` | Cliente Confirmou Recebimento | status | Sim/Não — TRAVA |
| 134 | `date_mkwhax75` | Prazo Avaliação Técnica do Cliente | date | TRAVA |
| 135 | `color_mkwhs0rn` | Apresentação da Proposta Realizada | status | Sim/Não |
| 136 | `color_mkwhh8h8` | Solução Técnica Aprovada pelo Cliente | status | Sim/Não — TRAVA Análise Comercial |
| 137 | `date_mkwhpq6v` | Prazo Análise Comercial do Cliente | date | TRAVA |
| 138 | `color_mkwhcba5` | E-mail Enviado ao Comprador | status | Sim/Não — TRAVA |
| 139 | `color_mkwjtpkm` | Visita Comercial Realizada | status | Sim/Não — TRAVA Negociação |
| 140 | `color_mkwjret0` | Valor Está Dentro da Expectativa | status | Sim/Não — TRAVA Negociação |
| 141 | `date_mkwjp97c` | Prazo Retorno Negociação | date | TRAVA |
| 142 | `color_mkwjecdh` | Condições Comerciais Aceitas | status | Sim/Não — TRAVA Emissão Pedido |
| 143 | `color_mkwjdmmr` | Cliente Confirmou Intenção de Compra | status | Sim/Não — TRAVA Emissão Pedido |
| 144 | `color_mkwj4dc3` | Atendemos o Prazo de Entrega | status | Sim/Não — TRAVA Emissão Pedido |
| 145 | `date_mkwjemxm` | Prazo Estimado Emissão Pedido | date | TRAVA |
| 146 | `color_mkwjat8f` | Pedido de Compra Recebido | status | Sim/Não — TRAVA Pedido Convertido |
| 147 | `color_mkwjkexa` | Pedido de Compra Conferido | status | Sim/Não — TRAVA Pedido Convertido |
| 148 | `color_mkwj6et3` | **Pasta do Projeto Atualizada** | status | Sim/Não — TRAVA Pedido Convertido (handoff PM) |
| 149 | `text_mkwpwyjz` | **Número da OS** | text | TRAVA Pedido Convertido — chave de junção CRM↔PM |
| 150 | `date_mkwkj5xk` | Data reunião de passagem de bastão | date | TRAVA Desenv. Proposta |
| 151 | `color_mkwkap0w` | Temos todas as informações técnicas | status | 3 labels (Em andamento/Feito/Parado) — **TRAVA Desenv. Proposta**, mas tipo errado para Sim/Não |
| 152 | `color_mkwkx98g` | Temos todas as informações comerciais | status | Sim/Não — TRAVA |
| 153 | `color_mkwp9bkf` | Projeção Aprovada Internamente? (V2) | status | Sim/Não — **DUPLICADO de col 79** |
| 154 | `color_mkwpfkmm` | Reunião de Apresentação Foi Agendada Com Cliente? | status | Sim/Não — TRAVA Projeção em Conversão |
| 155 | `numeric_mkx498n9` | Contador descartados | numbers | provável fórmula manual |
| 156 | `board_relation_mkxe4wcc` | **Portfólio de Automação** | board_relation | board: 8237943720 (workspace Projetos) |
| 157 | `color_mkzjdndj` | A ARV já realizou um projeto semelhante? | status | 4 labels (Tech Score v2) |
| 158 | `color_mkzjnbvr` | Domínio técnico com provas sociais? | status | 4 labels (Tech Score v2) |
| 159 | `color_mkzjfs9z` | Grau de risco técnico/operacional? | status | 4 labels |
| 160 | `color_mkzjpf79` | Quão completas as informações do cliente? | status | 4 labels |
| 161 | `color_mkzj244p` | Grau de complexidade técnica? | status | 4 labels |
| 162 | `color_mkzjaghc` | Projeto é tecnicamente viável? | status | 4 labels |
| 163 | `color_mkzjyp2f` | Retrofit ou solução nova? | status | 3 labels |
| 164 | `color_mkzjcv8v` | Cliente pode adiar sem impactos críticos? | status | 4 labels |
| 165 | `color_mkzj6r8y` | ARV domina as tecnologias? | status | 4 labels |
| 166 | `button_mkzjxacy` | **Gerar Technical Score** | button | — |
| 167 | `numeric_mkzj4xnw` | Valor do Score | numbers | calculado pelo botão |
| 168 | `color_mkzjw3ah` | **Score Técnico** | status | 5 labels (Quente; Muito Quente; Morno; Frio; Congelado) |
| 169 | `color_mkzn6733` | Prazo emissão do pedido (V2) | status | 5 labels — DUPLICADO da col 67 |
| 170 | `color_mkzn6wg0` | Existe chance do projeto não acontecer? | status | 3 labels (Não sei; Sim; Não) |
| 171 | `color_mkzn9pxh` | Tem Capex aprovado para este projeto? | status | 3 labels |
| 172 | `color_mkznn3dq` | Existe valor estimado/teto de investimento? (V2) | status | 3 labels — DUPLICADO da col 64 |
| 173 | `color_mkznjgpa` | Quais resultados esperados? (V2) | status | 3 labels — DUPLICADO da col 69 |
| 174 | `color_mkzn1c9t` | Payback esperado pelo cliente (V2) | status | 5 labels — DUPLICADO da col 70 |
| 175 | `color_mkzngaj9` | Possui caderno de encargos? (V2) | status | 3 labels — DUPLICADO da col 74 |
| 176 | `color_mkzndjfw` | Papel do contato na decisão (V2) | status | 5 labels — DUPLICADO da col 72 |
| 177 | `color_mkznbc68` | Já comprou com a ARV? (V2) | status | 3 labels — DUPLICADO da col 75 |
| 178 | `button_mkzr5jw1` | **Gerar Score** (oportunidade) | button | — |
| 179 | `numeric_mksads1c` | Score da Oportunidade | numbers | — |
| 180 | `status46__1` | **Temperatura** | status | 6 labels (Frio; Congelado; Morno; Muito Quente; Não Aplicado; Quente) — comercial+técnica num campo só |
| 181 | `color_mkzrrz8w` | Ação recomendada | status | 3 labels (PROJEÇÃO; ESTIMATIVA; ORÇAMENTO) |
| 182 | `file_mkzv4pgq` | Arquivos | file | — |
| 183 | `numeric_mm332c62` | Valor Revisado | numbers | R$ |

**Observações sobre Pipeline:**
- **Connect_boards (3):** Atividades→Tarefas+Tarefas Técnicas, Calendário Visitas→9758896572, Serviços e Revendas→8238302492, Portfólio Automação→8237943720. Pipeline é linkado por board_relation reverso por: Tarefas, Calendário, Tarefas Técnicas, Gestão de Contas (2 cols), Quadro de Prospecção (button só), Portfólio Automação (lookup).
- **Sem integrations externas** explícitas (campo `integration` não retornado em nenhuma coluna).
- **Sem coluna explícita de "Temperatura Comercial" vs "Temperatura Técnica":** col 168 (Score Técnico) e col 180 (Temperatura) carregam isso, mas dashboards.txt pede 2 visões separadas (Funil + Total para cada uma). Discrepância confirmada (ver §3.C).
- **Sem coluna "Próxima Atividade" no sentido de FK→Atividade.** Tem `Próx. Atividade` (col 59, status com 24 labels = tipo da próxima ação) + `Data Próx. Atividade` (col 60). Não há FK explícita ao item de Tarefas.
- **Buttons (4):** Pesquisar CNPJ, Gerar Leadscore, Gerar Technical Score, Gerar Score (oportunidade) — 3 sistemas de scoring distintos coexistem.
- **Travas mapeadas** (`travas.txt` cita 14 etapas com checkpoints): cols 127–148 cobrem Estimativa em Conversão → Pedido Convertido em Venda. Faltam travas de Qualificação Inicial (que apenas dependem de NomeEmpresa+Origem+SubOrigem+CNPJ+Telefone+NomeContato+Whatsapp+Email — todos já existem) e Qualificação da Oportunidade (Produto+Área já existem).
- **Subitems board** (7225377727) usa schema padrão Monday (name, person, status default 3 labels, date) — não foi catalogado em detalhe pois é placeholder.

### 1.3 Tarefas (id `9760832128`) — DEEP-DIVE

- URL: https://arvsystems-ltda.monday.com/boards/9760832128 · Folder CRM ✅🎯💰
- **6.860 items · 16 colunas · 2 grupos** (Tarefas / Tarefas concluidas)
- 5 Views salvas com filtro por person: David, Lilian, Mariana, Mauricio, Santiago

| # | id | title | type | detalhe |
|---|----|-------|------|---------|
| 1 | `name` | Name | name | — |
| 2 | `subtasks_mkvqb3jq` | Subelementos | subtasks | board=10040047994 |
| 3 | `person` | Criador | people | max 1 person |
| 4 | `board_relation_mktjzc7x` | **Pipeline** | board_relation | board=7089923423 |
| 5 | `lookup_mm32tzyr` | Resp. Comercial | mirror | de 7089923423.person |
| 6 | `lookup_mm32p6fr` | Resp. Técnico | mirror | de 7089923423.multiple_person_mks9bx3 |
| 7 | `lookup_mkzrhtcd` | Nome do Projeto | mirror | de 7089923423.text_mksybz8v |
| 8 | `timerange_mm31z58n` | Cronograma da Proposta | timeline | — |
| 9 | `status` | **Tipo de Tarefa** | status | **21 labels:** Agendar Visita 🚗; Reunião Interna 📈; Aguardando Informações ℹ️; Desenvolvimento de Material ✏️; Mensagem Linkedin 🤳; Estudo do Projeto 📝; Teste de Laboratório ⚙️; Revisão de Proposta; Revisão de Projeção; Desenvolvimento de Proposta 📓; Visita Agendada 🏭; Reunião agendada 🗓️; Email 📩; Atualização de CRM 🖥️; Ligação 📞; WhatsApp 📲; Desenvolvimeto de Projeção 📒 (typo); Contato com Fornecedor ☎️; Desenvolvimento de Estimativa 📝; No-Show |
| 10 | `color_mky0131a` | Status | status | 4 labels (Em Progresso; Concluído; Parado; Não Iniciado) |
| 11 | `data` | Prazo Início | date | — |
| 12 | `date_mktjarje` | Prazo Final | date | — |
| 13 | `date_mkxvg5aa` | Data Conclusão | date | show_time_by_default |
| 14 | `date_mktj3mgn` | Data Criação | date | — |
| 15 | `text_mktjeky0` | Informações da Tarefa | text | — |
| 16 | `lookup_mktjq3y5` | LeadID | mirror | de 7089923423.texto0__1 |

### 1.4 Calendário de Visitas (id `9758896572`) — DEEP-DIVE

- 533 items · 24 cols · 4 grupos (Visitas em planejamento/Agendadas/concluidas/canceladas)

| # | id | title | type | detalhe |
|---|----|-------|------|---------|
| 1 | `name` | Name | name | — |
| 2 | `subelementos_mkm5jkrb` | Subelementos | subtasks | board=9758896713 |
| 3 | `person` | Agendada por | people | — |
| 4 | `status` | Status | status | 4 labels (Visita Agendada 🏭; Visita Concluída!; Visita Cancelada!; Agendar Visita 🚗) |
| 5 | `status_1__1` | Vendedor(a) | status | 7 labels (Alex; Gabriel; Mauricio; Lilian; Mariana; (vazio); Santiago) — **anti-pattern: nome de vendedor em status** |
| 6 | `multiple_person_mkyax6ev` | Responsavel pela visita | people | — |
| 7 | `data` | Data da Visita | date | — |
| 8 | `status_1_mkka4da5` | **Perfil da Visita** | status | 8 labels (FUP de Proposta; Pré Vendas; NPS; Reativação de Cliente; Prospecção de Negócios; A definir.; Alinhamento Técnico; Cross Sell) |
| 9 | `location_mkxjcjz3` | Local | location | — (geolocalização Monday) |
| 10 | `lookup_mkx65t6z` | Distancia da planta | mirror | de 7089923423.color_mksa5jms |
| 11 | `color_mkxjdxea` | Zona | status | 5 labels (Zona Sul/Norte/Leste/Oeste/vazio) |
| 12 | `text_mkxjhbcf` | Cidade | text | — |
| 13 | `text_mkxjkkjj` | Estado | text | — |
| 14 | `lookup_mkv7gp8v` | CEP | mirror | de 7089923423.text_mkv19nk3 |
| 15 | `lookup_mkv7yw1n` | CEP Numero | mirror | de 7089923423.text_mkv5d6xh |
| 16 | `lookup_mkv7w3je` | Complemento | mirror | de 7089923423.text_mkt2js0v |
| 17 | `arquivos_mkmvpyfs` | Arquivos | file | — |
| 18 | `data__1` | Data de Entrada | date | — |
| 19 | `data2__1` | Data de Conclusão | date | — |
| 20 | `text_mktt8ma6` | LeadID | text | (campo plano) |
| 21 | `board_relation_mkttnjes` | **Pipeline** | board_relation | board=7089923423 |
| 22 | `lookup_mkttg7dq` | Vendedor | mirror | de 7089923423.person (DUPLICA col 5 que é status) |
| 23 | `lookup_mkttarfc` | Leadid | mirror | de 7089923423.texto0__1 (duplica col 20 que é text) |
| 24 | `numeric_mktvdpy6` | Números | numbers | nome genérico — provavelmente zumbi |

### 1.5 Tarefas Técnicas (id `18393358566`) — DEEP-DIVE

- 184 items · 22 cols · 3 grupos (A fazer/Concluidas/Cancelada)

| # | id | title | type | detalhe |
|---|----|-------|------|---------|
| 1 | `name` | Name | name | — |
| 2 | `person` | Pessoa | people | — |
| 3 | `lookup_mkzspsbh` | Responsavel Comercial | mirror | de 7089923423.person |
| 4 | `lookup_mkz48p5x` | Responsável Técnico | mirror | de 7089923423.multiple_person_mks9bx3 |
| 5 | `color_mkz3h068` | **Tarefa** | status | 5 labels (Desenv. de Estimativa 📝; Desenv. de Proposta 📓; Revisão de Projeção; Desenvolvimeto de Projeção 📒; Revisão de Proposta) — **subset do Tarefas.Tipo** |
| 6 | `board_relation_mkz392ns` | Pipeline | board_relation | board=7089923423 |
| 7 | `text_mkz32q36` | Descrição | text | — |
| 8 | `lookup_mkz4avhj` | Cronograma | mirror | de 7089923423.timerange_mksx6wg8 |
| 9 | `color_mkz46t4h` | Status | status | 6 labels (Fazendo; Feito; Parado; Em Aprovação; Cancelada; Esperando retorno) |
| 10 | `numeric_mkzc7km3` | Valor | numbers | unit R$ |
| 11 | `lookup_mkz3z6sp` | Prazo de entrega ARV | mirror | de 7089923423.date_mkxk4cz8 (col não listada nas 183! coluna do Pipeline está disponível mas talvez seja arquivada/inválida) |
| 12 | `lookup_mkz326cm` | Prazo de entrega do Cliente | mirror | de 7089923423.date_mkxkv99j (idem) |
| 13 | `date_mkz3x9gg` | Data Inicio | date | with time |
| 14 | `date_mkz3qcxx` | Data Fim | date | with time |
| 15 | `formula_mkz3ced6` | **Horas** | formula | `ROUND(DAYS({DataFim}, {DataInicio}) * 24, 2)` |
| 16 | `lookup_mkz3cce2` | Temperatura | mirror | de 7089923423.status46__1 |
| 17 | `date_mkz3hybb` | Data Conclusão | date | — |
| 18 | `lookup_mkz4xyev` | Lead id | mirror | de 7089923423.texto0__1 |
| 19 | `subtasks_mkzccvrv` | Subitems | subtasks | board=18394327801 |
| 20 | `lookup_mkzen6c2` | Espelho (Status do Pipeline) | mirror | de 7089923423.status (Etapa do Pipeline com 20 labels) |
| 21 | `formula_mkzj41xx` | Empresa | formula | `{board_relation_mkz392ns#Names}` |
| 22 | `lookup_mkzrn4t5` | nome do projeto | mirror | de 7089923423.text_mksybz8v |

**Observação:** este board é o equivalente a `Tarefas` mas só para tarefas técnicas (Estimativa/Projeção/Proposta/Revisão). É um "split" funcional do board Tarefas. No MCP CRM Bruno reproduziu essa separação (`07_TAREFAS` + `09_TAREFAS_TECNICAS`) — confirma intenção de manter distinção.

### 1.6 Gestão de Contas (id `18396765892`) — DEEP-DIVE

- 3 items · 62 cols · 1 grupo · descrita como "Master de clientes/contas"
- **Reproduz literalmente a estrutura plana de 4 contatos do Pipeline** + estende com colunas próprias

Resumo dos blocos (cada bloco tem **8 cols repetidas 4× = 32 cols só de contatos**):
- **Empresa:** name, Vendedor(a) (people), Categoria (status 3 labels: Cliente Base; Cliente Primeiro Contato; Cliente com Contato), Status (status 3 labels: Inativo; Ativo; Reativação), Ultimo Contato (date), Ultimo Projeto (date), Valor vendido (numbers R$), Razão social (text), CNPJ (text), CEP (text), número (text), complemento (text), Telefone fixo (phone)
- **Empresa-classificação:** Segmento de mercado (status 10 labels), Quantidade de funcionarios (status 3), tempo de mercado (status 3), n° de plantas (status 4), Distancia da planta (status 3), Lead score (numbers), Classificação (status 4)
- **Contato 1..4 (× 4):** Nome (text), Telefone (phone), E-mail (email), Cargo (status 21 labels), Departamento (status 18 labels), Nivel de influencia (status 6 labels), Linkedin (text)
- **Linkagem Pipeline:** board_relation Pipeline (`board_relation_mkzz2fsn`), Oportunidades ativas (numbers), Prox atividade (date), Espelho (mirror de 7089923423.status83__1 = Produto)

**Observação importante:** este board é a versão pre-MCP-CRM da intenção de Bruno: separar "conta" de "oportunidade", mas mantém os 32 campos planos de contato (não normaliza). É uma camada intermediária que vai ser **superada pelo `01_EMPRESAS` + `02_CONTATOS` do MCP CRM**.

### 1.7 Resumos dos boards menores

**Tarefas Paralelas** (id `18390965607`, 932 items, 6 cols):
- `name`, `person`, `status` (4 labels: Em andamento/Feito/Parado/+1), `subtasks_mkmskgrh`→18390966883, `timeline`, `data`
- 3 grupos (Atividades/Concluidas/Canceladas)
- **Sem board_relation com Pipeline** — tarefas avulsas, não vinculadas a leads. Preocupação para o SPEC: como manter histórico desse tipo no arv-crm? (Ex: "estudar concorrente", "fazer reunião com fornecedor X").

**Quadro de Prospecção** (id `18399307546`, 3.709 items, 8 cols):
- `name`, `text` Estado, `text` Cidade, `text` CNPJ, `people`, `button` "Enviar ao Pipeline", `status` (4 labels: Prospectar/Sem Informações/Prospectado/Descartado), `date`
- 4 grupos · sem activity há >2 meses (2026-02-23) — **provável zumbi** ou base de prospecção fria

**Entrada de Leads** (id `18193210777`, 226 items, 10 cols):
- `name`, `people`, `status` Origem (3 labels), `status` Sub Origem (9 labels), `text` CNPJ, `text` Nome, `phone`, `email`, `long_text` Demanda, `date`
- 1 grupo · FormBoardView "Entrada de Leads Internos" → form para colaborador interno cadastrar lead

---

## 2. Workspace `MCP CRM` (redesign morto, id 14592352)

Criado 2026-03-07 por Bruno. Descrição própria: "Substitui o workspace Comercial com estrutura baseada nos UMLs de Vendas. Escopo: Leads, Oportunidades, Orçamentos, Atividades, Contas."
**Estrutura completa, dados zero.** Todos os 12 boards têm 1-2 items + labels-placeholder ("Em andamento/Feito/Parado") + `top_group` apontando para grupo de items inativos/cancelados.

### 2.1 Lista dos 12 boards

| # | Board | id | Folder | Items | Cols | Grupos |
|---|-------|----|--------|------:|-----:|-------:|
| 1 | 01_EMPRESAS | 18402998719 | 🏢 Master Data | 1 | 20 | 4 |
| 2 | 02_CONTATOS | 18402998722 | 🏢 Master Data | 1 | 11 | 4 |
| 3 | 03_FONTES_CAPTACAO | 18402998725 | 🏢 Master Data | 1 | 8 | 2 |
| 4 | 04_LEADS | 18402999165 | 🎯 Funil Comercial | 1 | 18 | 5 |
| 5 | 05_OPORTUNIDADES | 18402999166 | 🎯 Funil Comercial | 2 | 27 | 9 |
| 6 | 06_ORCAMENTOS | 18402999765 | 💰 Orçamentos | 2 | 25 | 5 |
| 7 | 07_TAREFAS | 18402999766 | ✅ Atividades | 1 | 9 | 5 |
| 8 | 08_VISITAS | 18402999768 | ✅ Atividades | 1 | 10 | 5 |
| 9 | 09_TAREFAS_TECNICAS | 18402999770 | ✅ Atividades | 1 | 9 | 4 |
| 10 | 10_CONTAS | 18402999771 | 👥 Contas & Pós-Venda | 1 | 11 | 3 |
| 11 | HISTORICO_FASES | 18402999772 | 📊 Auxiliares & Histórico | 2 | 8 | 3 |

(11 listados — folder "🏢 Master Data" tem 3 boards, "🎯 Funil Comercial" tem 2, "💰 Orçamentos" tem 1, "✅ Atividades" tem 3, "👥 Contas & Pós-Venda" tem 1, "📊 Auxiliares & Histórico" tem 1 = **11 boards**. O 12º contado anteriormente parece ter sido erro de contagem do inventory anterior — workspace_info confirma 11 boards. Corrigido.)

### 2.2 Análise de intenção (mais importante que o conteúdo)

A estrutura desses 11 boards revela 6 decisões de design que Bruno tomou (mas não chegou a implementar nem a popular):

**1. Normalização em master data (`01_EMPRESAS` + `02_CONTATOS`).** Bruno separou explicitamente Empresa de Contato, com `02_CONTATOS.Empresa` como `board_relation` 1:1 → 01_EMPRESAS. Isso elimina o anti-pattern dos 24 campos planos de contato (Nome 1/2/3/4, Cargo 1/2/3/4...) que existem no Pipeline e foram replicados no `Gestão de Contas`. **Alinha 100% com `arv-crm/backend/models/contato.py` + `empresa.py`.** A descrição do board é literal: "Substitui os 24 campos planos de contato do Pipeline antigo".

**2. Funil em duas etapas (Lead → Oportunidade).** O board `04_LEADS` (descrito como "Funil pré-vendas. Substitui o Quadro de Prospecção e os grupos Lead Inicial / Qualificação Inicial do Pipeline antigo") tem 5 etapas (Prospecção → Primeiro Contato → Qualificação → Qualificado → Descartado). O `05_OPORTUNIDADES` ("Funil de vendas. Substitui o Pipeline principal. 8 etapas...") tem 8 etapas (Qualificação Oportunidade → Análise Interna → Desenvolvimento Proposta → Proposta Enviada → Em Negociação → Fechamento → Convertido em Projeto / Perdido). **Bruno quebrou as 20 etapas em 2 entidades.** O `arv-crm` usa um modelo único de Lead atualmente — decisão importante para o SPEC: implementar a separação Lead vs Oportunidade ou manter unificado? A intenção registrada aqui é separar.

**3. Orçamento como entidade própria com versionamento.** `06_ORCAMENTOS` tem coluna `Versão` (numbers), `board_relation` Oportunidade 1:N (várias versões por oportunidade), 14 campos numéricos para impostos+custos+CMV+markup, integração com analise-cmv-tool e roi-calculator via `link` columns. **No Pipeline atual, todos os 24 campos financeiros vivem na própria oportunidade — não há versionamento de proposta.** Intenção clara de adicionar isso ao SPEC.

**4. Atividade dividida em 3 boards (`07_TAREFAS`, `08_VISITAS`, `09_TAREFAS_TECNICAS`).** Mantém a divisão atual do legado (Tarefas + Calendário de Visitas + Tarefas Técnicas). Cada um tem `board_relation` para Lead E Oportunidade (não só Pipeline). **Confirma que `arv-crm/backend/models/atividade.py` deve ter um discriminator type para distinguir Visita / Tarefa Comercial / Tarefa Técnica** — ou 3 sub-tipos via SQLAlchemy inheritance.

**5. Pós-venda como entidade separada (`10_CONTAS`).** Conceito novo que NÃO existe no Comercial 💰 (o board `Gestão de Contas` é uma tentativa fraca, com 3 items). Tem campos próprios: NPS Médio, Health Score, Cross-sell. **arv-crm não tem essa entidade hoje — é gap claro de SPEC.**

**6. Audit trail explícito (`HISTORICO_FASES`).** Bruno criou um board para registrar mudanças de fase em Lead/Oportunidade ("Audit trail automático de mudanças de etapa em Leads e Oportunidades. Alimentado por automação — leitura apenas"). O `arv-crm/backend/models/historico_etapa.py` já existe (citado no DIAGNOSTICO §1.1). Confirma alinhamento.

**Bug consistente em todos os 11 boards:** `top_group` aponta para grupo "Inativos"/"Canceladas" (deveria apontar para entrada como Prospecção ou A Fazer). Provável erro de configuração do MCP/script de criação. Não afeta a intenção mas deve ser corrigido se workspace continuar vivo.

**O que falta:** Bruno NÃO criou board para:
- **Meta de vendas** (apesar de `dashboards.txt` pedir Meta de Vendas). Não há entidade `Meta` no MCP CRM.
- **Temperatura Comercial vs Técnica como dimensões separadas.** Tem 1 coluna `Temperatura` em Lead e em Oportunidade (mas labels-placeholder).
- **Score Lead (ICP) explícito como entidade separada de Score Oportunidade.** Tem `Lead Score` numbers em 04_LEADS, e `Score Técnico`+`Score Oportunidade` em 05_OPORTUNIDADES — separados. Mas como labels não foram configurados, é difícil saber se Bruno planejou 2 ou 3 sistemas distintos. Pelo Pipeline (que tem TODOS os 3), parece que intenção é manter 3 sistemas: Lead/Score+ICP, Score Técnico (de viabilidade), Score Oportunidade (BANT/MEDDIC).

### 2.3 Schema dos 11 boards do MCP CRM

#### 2.3.1 `01_EMPRESAS` (id 18402998719) — 20 cols, 4 grupos

Grupos: Inativos (top_group), Clientes Ativos, Prospects com Oportunidade, Base de Prospecção

| # | id | title | type | detalhe |
|---|----|-------|------|---------|
| 1 | name | Name | name | — |
| 2 | text_mm17pys6 | CNPJ | text | — |
| 3 | text_mm17fr0p | Razão Social | text | — |
| 4 | color_mm17mvyy | Segmento | status | placeholder labels |
| 5 | color_mm17f20m | Nº Funcionários | status | placeholder labels |
| 6 | numeric_mm175k3k | Nº de Plantas | numbers | — |
| 7 | numeric_mm17gbkb | Distância ARV (km) | numbers | — |
| 8 | text_mm17vb5c | Cidade | text | — |
| 9 | color_mm17e6ep | Estado | status | placeholder |
| 10 | text_mm17qaak | CEP | text | — |
| 11 | phone_mm174x7k | Telefone | phone | — |
| 12 | color_mm17qzzc | Status da Conta | status | placeholder |
| 13 | date_mm17het8 | Data Cadastro | date | — |
| 14 | date_mm1716a6 | Data Última Compra | date | — |
| 15 | numeric_mm17s6c3 | Valor Total Comprado (R$) | numbers | — |
| 16 | multiple_person_mm176mv5 | Responsável Comercial | people | — |
| 17 | text_mm179q9p | Site | text | — |
| 18 | long_text_mm175zs3 | Observações | long_text | — |
| 19 | board_relation_mm17ycbm | **Leads** | board_relation | board=18402999165 |
| 20 | board_relation_mm17w6t6 | **Oportunidades** | board_relation | board=18402999166 |

#### 2.3.2 `02_CONTATOS` (id 18402998722) — 11 cols, 4 grupos

Grupos: Inativos (top_group), Operacionais, Influenciadores, Decisores

| # | id | title | type | detalhe |
|---|----|-------|------|---------|
| 1 | name | Name | name | — |
| 2 | color_mm179p2k | Cargo | status | placeholder (no legado tem 21–33 labels) |
| 3 | color_mm17vz0f | Departamento | status | placeholder (no legado tem 18–23 labels) |
| 4 | color_mm17v123 | Nível de Influência | status | placeholder (no legado tem 6 labels) |
| 5 | email_mm1771fb | E-mail | email | — |
| 6 | phone_mm17rdpb | WhatsApp | phone | — |
| 7 | text_mm175aeq | LinkedIn | text | — |
| 8 | color_mm177p2x | Ativo? | status | placeholder |
| 9 | date_mm176t1y | Data Cadastro | date | — |
| 10 | board_relation_mm175bjr | **Empresa** | board_relation | board=18402998719 (1:1, mas board_relation Monday é N:N) |
| 11 | long_text_mm17yjjs | Observações | long_text | — |

#### 2.3.3 `03_FONTES_CAPTACAO` (id 18402998725) — 8 cols, 2 grupos

Grupos: Canais Inativos (top_group), Canais Ativos

| # | id | title | type | detalhe |
|---|----|-------|------|---------|
| 1 | name | Name | name | — |
| 2 | color_mm17bhyv | Canal | status | placeholder |
| 3 | color_mm17kt63 | Origem | status | placeholder |
| 4 | text_mm17cj9k | Campanha | text | — |
| 5 | numeric_mm175h4t | Custo de Aquisição (R$) | numbers | CAC |
| 6 | numeric_mm17kjtv | Taxa de Conversão (%) | numbers | — |
| 7 | numeric_mm17nsjg | Leads Gerados | numbers | — |
| 8 | numeric_mm17rky6 | Oportunidades Geradas | numbers | — |

#### 2.3.4 `04_LEADS` (id 18402999165) — 18 cols, 5 grupos

Grupos: Descartado (top_group), Qualificado, Qualificação, Primeiro Contato, Prospecção

| # | id | title | type | detalhe |
|---|----|-------|------|---------|
| 1 | name | Name | name | — |
| 2 | text_mm173w65 | Lead ID | text | — |
| 3 | board_relation_mm17snsx | **Empresa** | board_relation | board=18402998719 |
| 4 | board_relation_mm179hsf | **Contato Principal** | board_relation | board=18402998722 |
| 5 | multiple_person_mm171htd | Responsável | people | — |
| 6 | color_mm17yc1p | Etapa | status | placeholder (deveria ter 5: Prospecção..Descartado) |
| 7 | color_mm17q0yg | Sub-Status | status | placeholder |
| 8 | color_mm17jvv6 | Temperatura | status | placeholder |
| 9 | board_relation_mm17q3rx | **Origem** | board_relation | board=18402998725 (FONTES_CAPTACAO) |
| 10 | color_mm17r0cx | Produto de Interesse | status | placeholder |
| 11 | numeric_mm175fye | Lead Score | numbers | — |
| 12 | color_mm17v8kb | Classificação | status | placeholder (no legado tem 4 labels: A-Ideal..D-Fora ICP) |
| 13 | numeric_mm1757tx | Valor Estimado (R$) | numbers | — |
| 14 | color_mm175v8f | Motivo de Descarte | status | placeholder (no legado tem 17 labels) |
| 15 | date_mm17fdvg | Data de Entrada | date | — |
| 16 | date_mm17wccb | Data de Qualificação | date | — |
| 17 | color_mm17g86m | Próx. Atividade | status | placeholder |
| 18 | date_mm17kvw5 | Data Próx. Atividade | date | — |
| 19 | board_relation_mm17sj8 | **Oportunidade** | board_relation | board=18402999166 (Lead vira oportunidade quando Qualificado) |

#### 2.3.5 `05_OPORTUNIDADES` (id 18402999166) — 27 cols, 9 grupos

Grupos: Perdido (top_group), Convertido em Projeto, Fechamento, Em Negociação, Proposta Enviada, Desenvolvimento de Proposta, Análise Interna, Qualificação da Oportunidade, "Group Title" (lixo do template).

| # | id | title | type | detalhe |
|---|----|-------|------|---------|
| 1 | name | Name | name | — |
| 2 | board_relation_mm17swyk | **Lead de Origem** | board_relation | board=18402999165 |
| 3 | board_relation_mm1747kx | **Empresa** | board_relation | board=18402998719 |
| 4 | board_relation_mm17y560 | **Contatos** | board_relation | board=18402998722 (N contatos, não só 1) |
| 5 | multiple_person_mm174w2k | Resp. Comercial | people | — |
| 6 | multiple_person_mm17qf7y | Resp. Técnico | people | — |
| 7 | color_mm17wy2a | Etapa | status | placeholder (deveria ter 8 etapas) |
| 8 | color_mm17d8dx | Sub-Status | status | placeholder |
| 9 | color_mm17kqqf | Temperatura | status | placeholder |
| 10 | color_mm179n8x | Classificação | status | placeholder |
| 11 | color_mm17e1ba | Tipo de Entrega | status | placeholder (deveria ter 4: Projeção/Proposta/Estimativa/Apresentação) |
| 12 | numeric_mm17c194 | Valor Estimado (R$) | numbers | — |
| 13 | numeric_mm17dvrn | Valor Projetado (R$) | numbers | — |
| 14 | numeric_mm179y8s | Valor Final (R$) | numbers | — |
| 15 | numeric_mm17xvmd | Probabilidade (%) | numbers | — |
| 16 | numeric_mm17jma4 | Score Técnico | numbers | — |
| 17 | numeric_mm17nybg | Score Oportunidade | numbers | — |
| 18 | date_mm17606e | Data de Entrada | date | — |
| 19 | date_mm179w7f | Data Prevista de Fechamento | date | — |
| 20 | date_mm17538e | Data de Fechamento / Perda | date | — |
| 21 | color_mm17qmp3 | Motivo de Perda | status | placeholder |
| 22 | duration_mm17h0sd | Tempo na Etapa | time_tracking | tipo nativo Monday |
| 23 | long_text_mm17ek5j | Observações | long_text | — |
| 24 | board_relation_mm17j7ns | **Orçamentos** | board_relation | board=18402999765 |
| 25 | board_relation_mm17fnjr | **Tarefas** | board_relation | board=18402999766 |
| 26 | board_relation_mm1748xw | **Visitas** | board_relation | board=18402999768 |
| 27 | board_relation_mm17sfn6 | **Tarefas Técnicas** | board_relation | board=18402999770 |

#### 2.3.6 `06_ORCAMENTOS` (id 18402999765) — 25 cols, 5 grupos

Grupos: Rejeitados / Arquivados (top_group), Aprovados, Enviados ao Cliente, Em Elaboração, "Group Title".

| # | id | title | type | detalhe |
|---|----|-------|------|---------|
| 1 | name | Name | name | — |
| 2 | board_relation_mm17q1d1 | **Oportunidade** | board_relation | board=18402999166 |
| 3 | color_mm17fjzc | Tipo | status | placeholder |
| 4 | numeric_mm17gnzn | Versão | numbers | **versionamento explícito** |
| 5 | color_mm179tke | Status | status | placeholder |
| 6 | numeric_mm17wn6z | Valor Bruto (R$) | numbers | — |
| 7 | numeric_mm17vfa1 | CMV (R$) | numbers | — |
| 8 | numeric_mm17qma7 | Custo Fixo (R$) | numbers | — |
| 9 | numeric_mm17fqkq | Custo Financeiro (R$) | numbers | — |
| 10 | numeric_mm17n4c4 | Mão de Obra (R$) | numbers | — |
| 11 | numeric_mm179ebc | Terceiros (R$) | numbers | — |
| 12 | numeric_mm1792y1 | **Markup (%)** | numbers | unit % (no Pipeline é R$ — diferença semântica importante) |
| 13 | numeric_mm17hben | Comissão (%) | numbers | unit % |
| 14 | numeric_mm17w2rw | IR (%) | numbers | unit % (no Pipeline é R$) |
| 15 | numeric_mm17p30q | CSLL (%) | numbers | unit % |
| 16 | numeric_mm17fcnf | ICMS (%) | numbers | unit % |
| 17 | numeric_mm17vzqy | ISS (%) | numbers | unit % |
| 18 | numeric_mm1718pr | PIS (%) | numbers | unit % |
| 19 | numeric_mm179xtq | COFINS (%) | numbers | unit % |
| 20 | date_mm17ebx2 | Prazo de Entrega | date | — |
| 21 | numeric_mm17kzjw | Validade (dias) | numbers | — |
| 22 | date_mm177d16 | Data de Envio | date | — |
| 23 | color_mm17hr03 | Motivo de Perda | status | placeholder |
| 24 | file_mm17c0a3 | Arquivo PDF | file | — |
| 25 | link_mm17aef2 | Link CMV Calculator | link | URL externa |
| 26 | link_mm17njsb | Link ROI Calculator | link | URL externa |

**Surpresa:** no MCP CRM, impostos são em % (não R$ como no Pipeline). É uma decisão arquitetural — propostas se calculam multiplicando o Valor Bruto pelas alíquotas. Mais limpo do que o Pipeline, que armazena valores absolutos.

#### 2.3.7 `07_TAREFAS` (id 18402999766) — 9 cols, 5 grupos

Grupos: Canceladas (top_group), Concluídas, Em Andamento, A Fazer, "Group Title".

| # | id | title | type | detalhe |
|---|----|-------|------|---------|
| 1 | name | Name | name | — |
| 2 | color_mm17xr6r | Tipo de Tarefa | status | placeholder (deveria ter 18 tipos conforme descrição) |
| 3 | board_relation_mm17kqg2 | **Lead** | board_relation | board=18402999165 (tarefa pode estar em lead E em oportunidade — não exclusivo) |
| 4 | board_relation_mm17jefw | **Oportunidade** | board_relation | board=18402999166 |
| 5 | multiple_person_mm17j478 | Responsável | people | — |
| 6 | date_mm17sy4f | Prazo | date | — |
| 7 | date_mm17r3qf | Data de Conclusão | date | — |
| 8 | color_mm17k8vc | Canal | status | placeholder |
| 9 | long_text_mm17xxp4 | Conteúdo | long_text | — |

#### 2.3.8 `08_VISITAS` (id 18402999768) — 10 cols, 5 grupos

Grupos: Canceladas (top_group), Concluídas, Agendadas, Em Planejamento, "Group Title".

| # | id | title | type | detalhe |
|---|----|-------|------|---------|
| 1 | name | Name | name | — |
| 2 | color_mm17nc7 | Perfil da Visita | status | placeholder (deveria ter 8 perfis conforme descrição) |
| 3 | board_relation_mm178kqd | **Lead** | board_relation | board=18402999165 |
| 4 | board_relation_mm17bqcq | **Oportunidade** | board_relation | board=18402999166 |
| 5 | multiple_person_mm17kshh | Responsável | people | — |
| 6 | date_mm17e0jc | Data da Visita | date | — |
| 7 | text_mm1766p5 | Cidade | text | — |
| 8 | color_mm17h1et | Estado | status | placeholder |
| 9 | color_mm17x0ve | Zona | status | placeholder (deveria ter Zona Sul/Norte/Leste/Oeste) |
| 10 | color_mm171ntx | Próxima Ação | status | placeholder |
| 11 | long_text_mm17f4c8 | Relatório de Visita | long_text | — |

**Notar:** sem `location` (geo) e sem mirror de "Distância da planta". O legado (Calendário de Visitas) tem `location` columns + mirror de distância. Bruno simplificou — possivelmente intencionalmente. Se quer manter geo no arv-crm, precisa ressuscitar isso.

#### 2.3.9 `09_TAREFAS_TECNICAS` (id 18402999770) — 9 cols, 4 grupos

Grupos: Canceladas (top_group), Concluídas, A Fazer, "Group Title".

| # | id | title | type | detalhe |
|---|----|-------|------|---------|
| 1 | name | Name | name | — |
| 2 | color_mm17s99e | Tipo | status | placeholder (deveria ter Estimativa/Projeção/Proposta/Revisão) |
| 3 | board_relation_mm174ndz | **Oportunidade** | board_relation | board=18402999166 (não tem Lead — só vinculado a oportunidade) |
| 4 | multiple_person_mm17yyn3 | Responsável Técnico | people | — |
| 5 | multiple_person_mm17s2br | Responsável Comercial | people | — |
| 6 | color_mm179nyd | Status | status | placeholder |
| 7 | date_mm17nscj | Data Início | date | — |
| 8 | date_mm17t083 | Data Fim | date | — |
| 9 | numeric_mm177q1f | Valor (R$) | numbers | — |
| 10 | long_text_mm17b8y3 | Descrição | long_text | — |

#### 2.3.10 `10_CONTAS` (id 18402999771) — 11 cols, 3 grupos

Grupos: Inativos (top_group), Em Garantia, Clientes Ativos.

| # | id | title | type | detalhe |
|---|----|-------|------|---------|
| 1 | name | Name | name | — |
| 2 | board_relation_mm175q70 | **Empresa** | board_relation | board=18402998719 |
| 3 | multiple_person_mm17g753 | Resp. Comercial | people | — |
| 4 | numeric_mm17efm1 | Nº Projetos Entregues | numbers | — |
| 5 | numeric_mm17ft38 | Valor Total (R$) | numbers | — |
| 6 | date_mm17zxe4 | Último Projeto | date | — |
| 7 | date_mm17nm64 | Próximo Contato | date | — |
| 8 | color_mm17qxzw | **Health Score** | status | placeholder (conceito novo!) |
| 9 | numeric_mm178p7 | NPS Médio | numbers | — |
| 10 | color_mm17payd | Oportunidade Cross-sell | status | placeholder |
| 11 | long_text_mm17cfr4 | Observações | long_text | — |
| 12 | board_relation_mm17nynv | **Oportunidades** | board_relation | board=18402999166 |

#### 2.3.11 `HISTORICO_FASES` (id 18402999772) — 8 cols, 3 grupos

Grupos: Histórico de Oportunidades (top_group), Histórico de Leads, "Group Title". "Audit trail automático... leitura apenas".

| # | id | title | type | detalhe |
|---|----|-------|------|---------|
| 1 | name | Name | name | — |
| 2 | color_mm17ywyk | Entidade | status | placeholder (esperado: Lead vs Oportunidade) |
| 3 | board_relation_mm17m5yy | **Lead** | board_relation | board=18402999165 |
| 4 | board_relation_mm176th6 | **Oportunidade** | board_relation | board=18402999166 |
| 5 | text_mm171a2z | Fase | text | nome da etapa |
| 6 | text_mm17kxgr | Sub-Status ao Sair | text | — |
| 7 | date_mm17snka | Data de Entrada na Fase | date | — |
| 8 | date_mm17sgab | Data de Saída | date | — |

---

## 3. Cruzamento

### A. Mapeamento Pipeline → entidades arv-crm

Para cada uma das 183 colunas do Pipeline, mapeamento da entidade-alvo no arv-crm. Convenções:
- **Empresa** = ARV: `models/empresa.py`
- **Contato** = ARV: `models/contato.py` (relação 1:N com Empresa)
- **Lead/Oportunidade** = ARV: `models/lead.py` (atualmente unificados; SPEC pode dividir)
- **Atividade** = ARV: `models/atividade.py`
- **Origem** = ARV: `models/origem.py`
- **ScoringResposta** = ARV: `models/scoring_resposta.py` (já existe; armazena respostas de scorecard)
- **HistoricoEtapa** = ARV: `models/historico_etapa.py`
- **Orçamento** = entidade NOVA proposta pelo MCP CRM (`06_ORCAMENTOS`)
- **MetaVendas** = entidade NOVA (não existe nem no legado nem no MCP)
- **Conta** = entidade NOVA proposta pelo MCP CRM (`10_CONTAS`)

| # Pipeline | Coluna | Tipo | Entidade arv-crm | Field sugerido | Observação |
|---:|--------|------|------------------|----------------|------------|
| 1 | Name | name | Lead | `nome` | identificador human readable |
| 2 | Subelementos | subtasks | — | — | descartar (Monday-only) |
| 3 | Nome do Projeto | text | Lead | `nome_projeto` | — |
| 4 | Etapa do Pipeline | status (20 labels) | Lead | `etapa: Enum` | dividir em duas: 5 valores Lead-stage + 8 Oportunidade-stage (alinhar com MCP CRM) |
| 5 | Descrição atual ou ideal da demanda | long_text | Lead | `descricao_demanda` | — |
| 6 | Resp. Próx. Atividade | people | Atividade | `responsavel_id` | denormalização (já vem da próxima atividade vinculada) |
| 7 | Resp. Comercial | people | Lead | `responsavel_comercial_id` (FK User) | — |
| 8 | Resp. Técnico | people | Lead | `responsavel_tecnico_id` | — |
| 9 | Razão Social | text | Empresa | `razao_social` | mover para Empresa, deduplicar |
| 10 | Nome do Contato 1 | text | Contato | `nome` | virar 1 contato relacionado ao Empresa, não campo flat |
| 11 | Telefone / WhatsApp | phone | Contato | `whatsapp` | idem |
| 12 | E-mail | email | Contato | `email` | idem |
| 13 | Data da Ult. Atividade | date | Lead | `data_ultima_atividade` | DERIVADO (max(atividade.data_conclusao)). Não persistir; calcular |
| 14 | Data de Entrada Pré Vendas | date | Lead | `data_entrada_prevendas` | — |
| 15 | Data de Entrada Vendas | date | Lead | `data_entrada_vendas` | — |
| 16 | Cargo Contato 1 | status (21 labels) | Contato | `cargo: Enum` | enum único compartilhado entre todos contatos |
| 17 | Departamento Contato 1 | status (23 labels) | Contato | `departamento: Enum` | enum único — limpar typos do legado |
| 18 | Nível de Influência | status (6) | Contato | `influencia: Enum` | — |
| 19 | CNPJ | text | Empresa | `cnpj` | — |
| 20 | Pesquisar CNPJ? | button | — | — | substituir por integração CNPJWS no `cnpj_service.py` (já existe!) |
| 21 | CEP | text | Empresa | `cep` | — |
| 22 | Número | text | Empresa | `numero` | — |
| 23 | Complemento | text | Empresa | `complemento` | — |
| 24 | Telefone Fixo | phone | Empresa | `telefone` | — |
| 25 | Linkedin | text | Empresa | `linkedin` | — |
| 26 | Segmento de Mercado | status (10) | Empresa | `segmento: Enum` | — |
| 27 | Quantidade de Funcionários | status (3) | Empresa | `porte_funcionarios: Enum` | — |
| 28 | Tempo no Mercado | status (3) | Empresa | `tempo_mercado: Enum` | — |
| 29 | Nº de Plantas Industriais | status (4) | Empresa | `num_plantas: Enum` | — |
| 30 | Distância da Planta | status (3) | Empresa | `distancia_planta: Enum` | — |
| 31 | Gerar Leadscore | button | — | — | substituir por endpoint `POST /leads/{id}/calc-leadscore` no `scoring_service.py` |
| 32 | Lead Scoring | numbers | Lead | `lead_score` | calculado por scoring_service |
| 33 | Classificação de Leads | status (4) | Lead | `classificacao_icp: Enum` (A/B/C/D) | derivado do Lead Score |
| 34–40 | Bloco Contato 2 (Nome/Tel/Email/Cargo/Depto/Influência/Linkedin) | — | Contato | (mesma estrutura do Contato 1) | virar registro 2/N do Contato relacionado |
| 41–47 | Bloco Contato 3 | — | Contato | idem | registro 3/N |
| 48–54 | Bloco Contato 4 | — | Contato | idem | registro 4/N |
| 55 | Origem | status (15, com duplicatas) | Origem | `origem.canal: Enum` | dedupe ("Tráfego Pago" duplicado, "Indicação" desdobrado em "Indicação Parceiros"+"Indicação Clientes") |
| 56 | Sub-Origem | status (23) | Origem | `origem.sub_canal` | mover para entidade Origem (já existe model) |
| 57 | Produto | status (5) | Lead | `produto: Enum` (Apresentação/Prospecção Ativa/Serviço/Automação/Revenda) | — |
| 58 | Área de Atuação | status (9) | Lead | `area_atuacao: Enum` | — |
| 59 | Próx. Atividade | status (24) | Atividade | `tipo: Enum` | derivado da próxima atividade vinculada (TIPO da atividade — não da etapa do funil). Limpar duplicatas ("Reunião agendada" vs "Reunião Agendada") |
| 60 | Data Próx. Atividade | date | Atividade | `data_inicio` da próxima atividade | DERIVADO |
| 61 | Tipo de Entrega | status (4) | Lead | `tipo_entrega: Enum` (Projeção/Proposta/Estimativa/Apresentação) | — |
| 62 | É melhoria ou meio de produção? | status (2) | Lead | `tipo_demanda: Enum` (Meio_Producao/Melhoria_Processo) | — |
| 63 | Processo já existe? | status (2) | Lead | `processo_existe: bool` | — |
| 64 | Existe valor estimado? | status (5) | ScoringResposta | scoring_resposta(pergunta=BUDGET_VALOR) | sistema BANT v1 |
| 65 | Investimento aprovado? | status (5) | ScoringResposta | scoring_resposta(BUDGET_APROVACAO) | BANT v1 |
| 66 | Prazo desejado para implantação? | status (5) | ScoringResposta | scoring_resposta(TIME_IMPLANTACAO) | BANT v1 |
| 67 | Prazo emissão pedido? | status (5) | ScoringResposta | scoring_resposta(TIME_PEDIDO) | BANT v1 |
| 68 | Qual problema/desafio? | status (5) | ScoringResposta | scoring_resposta(PAIN_PROBLEMA) | MEDDIC v1 |
| 69 | Quais resultados esperados? | status (5) | ScoringResposta | scoring_resposta(METRICS_RESULTADOS) | MEDDIC v1 |
| 70 | Payback esperado? | status (5) | ScoringResposta | scoring_resposta(METRICS_PAYBACK) | MEDDIC v1 |
| 71 | Quais áreas envolvidas? | status (5) | ScoringResposta | scoring_resposta(CHAMPION_AREAS) | MEDDIC v1 |
| 72 | Papel do contato na decisão | status (5) | ScoringResposta | scoring_resposta(DECISION_PAPEL) | MEDDIC v1 |
| 73 | Histórico com automação | status (5) | ScoringResposta | scoring_resposta(HIST_AUTOMACAO) | MEDDIC v1 |
| 74 | Caderno de encargos? | status (5) | ScoringResposta | scoring_resposta(DOC_CADERNO) | MEDDIC v1 |
| 75 | Já comprou com a ARV? | status (5) | ScoringResposta | scoring_resposta(HIST_ARV) | MEDDIC v1 |
| 76 | ARV já desenvolveu similar? | status (5) | ScoringResposta | scoring_resposta(SIMILAR_ARV) | MEDDIC v1 |
| 77 | Clareza técnica esperada | status (5) | ScoringResposta | scoring_resposta(TECH_CLAREZA) | MEDDIC v1 |
| 78 | Status da Projeção | status (3 default) | — | — | **ZUMBI** — labels não customizadas, é placeholder |
| 79 | Projeção Aprovada Internamente? | status (2) | Lead | `projecao_aprovada_interna: bool` | — |
| 80 | Valor Projetado | numbers | Lead | `valor_projetado_brl` | — |
| 81 | Projeção Validada com Comercial? | status (2) | Lead | `projecao_validada_comercial: bool` | — |
| 82 | É cliente ARV | status (2) | Empresa | derivado de `Empresa.tem_compras` ou `Conta` existente | DERIVADO |
| 83 | Informações Finais? | status (2) | Lead | `info_final_completa: bool` | — |
| 84 | Nivel de Aderência? | status (3) | Lead | `nivel_aderencia: Enum` | — |
| 85 | Nível de Complexidade? | status (3) | Lead | `nivel_complexidade: Enum` | — |
| 86 | Cronograma da Proposta | timeline | Lead | `cronograma_inicio` + `cronograma_fim` | — |
| 87 | Status (geral oport.) | status (7) | Lead | `status_oportunidade: Enum` (Fazendo/Feito/Parado/EmAprovação/Revisão/Cancelada/EsperandoRetorno) | — |
| 88 | Valor Estimado (R$) | numbers | Lead | `valor_estimado_brl` | — |
| 89 | Valor Final | numbers | Lead | `valor_final_brl` | — |
| 90 | Nº de Revisão | numbers | Orçamento | `versao` | mover para Orçamento (intenção MCP CRM) |
| 91 | Motivo do Descarte | status (17, com duplicatas) | Lead | `motivo_descarte: Enum` | dedupe (Inviabilidade Técnica e Decisão Cliente repetidas) |
| 92 | monday Doc v2 | direct_doc | — | — | descartar (Monday-only) |
| 93 | Chance de Conversão | numbers | Lead | `prob_conversao_pct` | derivado da etapa? ou input manual? — decidir |
| 94 | Data Criação de Orçamento | date | Orçamento | `data_criacao` | mover |
| 95 | Data Prevista de Vendas | date | Lead | `data_prevista_fechamento` | — |
| 96 | Antecipação | numbers | Orçamento | `antecipacao_pct` | mover |
| 97 | Data Recebimento Antecipação | date | Orçamento | `data_recebimento_antecipacao` | mover |
| 98 | Custo Fixo | numbers | Orçamento | `custo_fixo_brl` | — |
| 99 | Custo Financeiro | numbers | Orçamento | `custo_financeiro_brl` | — |
| 100 | Comissão | numbers | Orçamento | `comissao_brl` | — |
| 101 | Markup | numbers | Orçamento | `markup_brl` (legado) ou `markup_pct` (MCP) | **decidir convenção: R$ ou %** |
| 102 | CMV | numbers | Orçamento | `cmv_brl` | — |
| 103 | Terceiros | numbers | Orçamento | `terceiros_brl` | — |
| 104 | Mão de Obras | numbers | Orçamento | `mao_obra_brl` | — |
| 105 | IR | numbers | Orçamento | `ir_brl` (legado) ou `ir_pct` (MCP) | decidir |
| 106 | CSLL | numbers | Orçamento | `csll_brl` | idem |
| 107 | ICMS | numbers | Orçamento | `icms_brl` | idem |
| 108 | ISS | numbers | Orçamento | `iss_brl` | idem |
| 109 | PIS | numbers | Orçamento | `pis_brl` | idem |
| 110 | COFINS | numbers | Orçamento | `cofins_brl` | idem |
| 111 | Proposta com Imposto | formula | Orçamento | `valor_total_com_imposto` (computed prop) | derivado |
| 112 | Proposta sem Imposto | formula | Orçamento | `valor_total_sem_imposto` | derivado — **revisar fórmula: inclui IR/CSLL no "sem imposto", possível bug** |
| 113 | Composição Meta de Vendas | formula | Orçamento | `composicao_meta` | derivado (CustoFixo+CustoFin+Comissão+Markup+MãoObra) |
| 114 | Previsão com Imposto | formula | Lead | `previsao_com_imposto` | derivado (Proposta × Chance) |
| 115 | Previsão sem Imposto | formula | Lead | `previsao_sem_imposto` | derivado |
| 116 | Previsão Meta de Vendas | formula | Lead | `previsao_meta` | derivado |
| 117 | Previsão Meta no Ano | formula | Lead | derivado de MetaVendas anual | **NÃO HARDCODAR R$ 7.562.285,08 — buscar de MetaVendas.ano=2026** |
| 118 | Previsão Meta no Mês | formula | Lead | derivado de MetaVendas mensal | **NÃO HARDCODAR R$ 630.190,59 — buscar de MetaVendas.mes** |
| 119 | Antecipações Confirmadas | formula | Lead | derivado | bug Monday: usa string como output ("Oportunidade Não Convertida") — separar em 2 colunas |
| 120 | Antecipações Previstas | formula | Lead | derivado | idem |
| 121 | Data Conclusão | date | Lead | `data_fechamento_perda` | — |
| 122 | Lead ID | text | Lead | `lead_id_externo` | manter para compat com migração |
| 123 | META LEADS (NÃO APAGAR) | numbers | — | — | **ZUMBI** — meta inline numa coluna; mover para MetaVendas |
| 124 | Atividades (rel) | board_relation | Atividade | FK reverso já modelado | — |
| 125 | Calendário de Visitas (rel) | board_relation | Atividade (subtipo Visita) | idem | — |
| 126 | Serviços e Revendas (rel) | board_relation | — | — | descartar (workspace separado, fora de escopo CRM) |
| 127 | Foi Enviado ao Cliente? | status (2) | Lead | `foi_enviado_cliente: bool` (TRAVA Estimativa em Conversão) | trava `travas.txt` |
| 128 | Data de Envio | date | Lead | `data_envio_estimativa` | trava |
| 129 | Dentro da faixa de investimento? | status (2) | Lead | `dentro_faixa_investimento: bool` | — |
| 130 | Aprovado pelo Comitê | status (2) | Lead | `aprovado_comite: bool` (TRAVA Projeção em Conversão) | trava |
| 131 | Data de reunião de apresentação | date | Lead | `data_reuniao_apresentacao` | — |
| 132 | Proposta Enviada ao Cliente | status (2) | Orçamento | `proposta_enviada: bool` | TRAVA |
| 133 | Cliente Confirmou Recebimento | status (2) | Orçamento | `cliente_confirmou_recebimento: bool` | TRAVA |
| 134 | Prazo Avaliação Técnica do Cliente | date | Orçamento | `prazo_aval_tecnica_cliente` | TRAVA |
| 135 | Apresentação Realizada | status (2) | Lead | `apresentacao_realizada: bool` | — |
| 136 | Solução Técnica Aprovada | status (2) | Lead | `solucao_tecnica_aprovada: bool` | TRAVA Análise Comercial |
| 137 | Prazo Análise Comercial | date | Orçamento | `prazo_aval_comercial_cliente` | TRAVA |
| 138 | E-mail Enviado ao Comprador | status (2) | Atividade | uma atividade do tipo Email | TRAVA |
| 139 | Visita Comercial Realizada | status (2) | Atividade | derivado de Atividade(tipo=Visita,subtipo=Comercial) | TRAVA |
| 140 | Valor Está Dentro da Expectativa | status (2) | Lead | `valor_dentro_expectativa: bool` | TRAVA |
| 141 | Prazo Retorno Negociação | date | Lead | `prazo_retorno_negociacao` | TRAVA |
| 142 | Condições Comerciais Aceitas | status (2) | Lead | `cond_comerciais_aceitas: bool` | TRAVA |
| 143 | Cliente Confirmou Intenção Compra | status (2) | Lead | `cliente_confirmou_intencao: bool` | TRAVA |
| 144 | Atendemos o Prazo de Entrega | status (2) | Lead | `atende_prazo_entrega_cliente: bool` | TRAVA |
| 145 | Prazo Estimado Emissão Pedido | date | Lead | `prazo_estimado_emissao_pedido` | TRAVA |
| 146 | Pedido de Compra Recebido | status (2) | Lead | `pedido_compra_recebido: bool` | TRAVA Pedido Convertido |
| 147 | Pedido de Compra Conferido | status (2) | Lead | `pedido_compra_conferido: bool` | TRAVA Pedido Convertido |
| 148 | Pasta do Projeto Atualizada | status (2) | Lead | `pasta_projeto_atualizada: bool` | TRAVA Pedido Convertido (handoff PM) |
| 149 | Número da OS | text | Lead | `numero_os` | **chave de junção CRM↔arv-pm** — TRAVA |
| 150 | Data passagem de bastão | date | Lead | `data_passagem_bastao` | TRAVA Desenv. Proposta |
| 151 | Temos info técnicas | status (3 default) | Lead | `info_tecnicas_completas: bool` | TRAVA — **bug: deveria ser 2 labels Sim/Não, está com 3 placeholder** |
| 152 | Temos info comerciais | status (2) | Lead | `info_comerciais_completas: bool` | TRAVA |
| 153 | Projeção Aprovada Interna? (V2) | status (2) | — | — | **DUPLICADO da col 79 — descartar** |
| 154 | Reunião Agendada com Cliente? | status (2) | Lead | `reuniao_agendada_cliente: bool` | TRAVA Projeção em Conversão |
| 155 | Contador descartados | numbers | — | — | **ZUMBI** — provável fórmula manual; descartar |
| 156 | Portfólio de Automação (rel) | board_relation | — | — | descartar (workspace PM, fora CRM) |
| 157 | ARV já realizou semelhante? | status (4) | ScoringResposta | scoring_resposta(TECH_PRECEDENTE) | sistema Tech Score v2 |
| 158 | Domínio técnico com provas? | status (4) | ScoringResposta | scoring_resposta(TECH_DOMINIO) | TechScore v2 |
| 159 | Risco técnico/operacional? | status (4) | ScoringResposta | scoring_resposta(TECH_RISCO) | TechScore v2 |
| 160 | Info do cliente úteis? | status (4) | ScoringResposta | scoring_resposta(TECH_INFO_CLIENTE) | TechScore v2 |
| 161 | Complexidade técnica? | status (4) | ScoringResposta | scoring_resposta(TECH_COMPLEXIDADE) | TechScore v2 |
| 162 | Tecnicamente viável? | status (4) | ScoringResposta | scoring_resposta(TECH_VIABILIDADE) | TechScore v2 |
| 163 | Retrofit ou solução nova? | status (3) | ScoringResposta | scoring_resposta(TECH_RETROFIT) | TechScore v2 |
| 164 | Cliente pode adiar sem impactos? | status (4) | ScoringResposta | scoring_resposta(TECH_URGENCIA) | TechScore v2 |
| 165 | ARV domina tecnologias? | status (4) | ScoringResposta | scoring_resposta(TECH_DOMINIO_TEC) | TechScore v2 |
| 166 | Gerar Technical Score | button | — | — | substituir por endpoint `POST /leads/{id}/calc-techscore` |
| 167 | Valor do Score (Técnico) | numbers | Lead | `score_tecnico` | calculado |
| 168 | Score Técnico (label) | status (5) | Lead | `temperatura_tecnica: Enum` (Quente/MuitoQuente/Morno/Frio/Congelado) | — |
| 169 | Prazo emissão pedido (V2) | status (5) | — | — | **DUPLICADO da col 67** |
| 170 | Existe chance projeto não acontecer? | status (3) | ScoringResposta | scoring_resposta(OPP_RISCO_NAO_OCORRER) | sistema Score Oportunidade |
| 171 | Tem Capex aprovado? | status (3) | ScoringResposta | scoring_resposta(OPP_CAPEX) | ScoreOportunidade |
| 172 | Existe valor estimado? (V2) | status (3) | — | — | **DUPLICADO da col 64** |
| 173 | Quais resultados? (V2) | status (3) | — | — | **DUPLICADO da col 69** |
| 174 | Payback (V2) | status (5) | — | — | **DUPLICADO da col 70** |
| 175 | Caderno encargos? (V2) | status (3) | — | — | **DUPLICADO da col 74** |
| 176 | Papel contato decisão (V2) | status (5) | — | — | **DUPLICADO da col 72** |
| 177 | Já comprou ARV? (V2) | status (3) | — | — | **DUPLICADO da col 75** |
| 178 | Gerar Score (oportunidade) | button | — | — | substituir por endpoint `POST /leads/{id}/calc-oportscore` |
| 179 | Score da Oportunidade | numbers | Lead | `score_oportunidade` | calculado |
| 180 | Temperatura | status (6) | Lead | `temperatura_comercial: Enum` (Frio/Congelado/Morno/MuitoQuente/NãoAplicado/Quente) | **separa do Score Técnico (col 168)** |
| 181 | Ação recomendada | status (3) | Lead | `acao_recomendada: Enum` (PROJEÇÃO/ESTIMATIVA/ORÇAMENTO) | — |
| 182 | Arquivos | file | Lead | `arquivos: List[Arquivo]` | tabela auxiliar de Arquivo |
| 183 | Valor Revisado | numbers | Orçamento | `valor_revisado_brl` | mover |

**Estatísticas do mapeamento:**
- → **Empresa**: 14 colunas (CNPJ, Razão Social, endereço, segmento, porte, distância, etc)
- → **Contato**: 4 × 7 = **28 colunas** (consolidados em registros, não em campos planos)
- → **Lead**: ~50 colunas (etapa, valores, datas, scores, campos de trava)
- → **Orçamento**: ~22 colunas (todo bloco financeiro + meta + antecipação)
- → **Atividade**: 5 colunas (próx atividade, datas, tipo)
- → **Origem**: 2 colunas (canal, sub-canal)
- → **ScoringResposta**: ~28 colunas (todas as perguntas BANT/MEDDIC/TechScore/OppScore — 1 registro por pergunta+lead)
- → **MetaVendas (NOVO)**: 2 colunas das fórmulas (cols 117-118 hardcoded)
- → **Conta (NOVO)**: 1 coluna (col 82 É cliente ARV — derivado)
- **Descartáveis (zumbis/duplicados/Monday-only)**: 18 colunas — Subelementos, monday Doc, V2-duplicates (153, 169, 172-177), Status placeholder col 78, META LEADS col 123, Contador col 155, board_relation Serviços/Portfolio (cols 126, 156), buttons (4× tornam-se endpoints, não colunas), Pesquisar CNPJ (button)

### B. Conceitos do redesign não cobertos no legado

| Conceito intencionado no MCP CRM | Existe no Comercial 💰? | Já está no arv-crm? | Recomendação |
|----------------------------------|------------------------|---------------------|--------------|
| **Empresa como entidade própria** (`01_EMPRESAS`) | parcial (Gestão de Contas, 3 items) | sim (`models/empresa.py`) | **incorporar** — usar como autoridade |
| **Contato normalizado N:N com Empresa** (`02_CONTATOS`) | não (4 campos planos) | sim (`models/contato.py`) | **incorporar** — gerar N contatos por lead na migração |
| **Origem como entidade com CAC/conversion %** (`03_FONTES_CAPTACAO`) | parcial (apenas labels em status) | sim (`models/origem.py`) — checar se tem CAC/conversion% | **incorporar** — adicionar campos CAC, taxa_conversao, leads_gerados, oportunidades_geradas |
| **Funil em 2 entidades: Lead pré-vendas + Oportunidade vendas** | não (1 board com 20 etapas) | parcial (1 entidade Lead com etapas) | **decisão arquitetural pendente** — recomendo unificar (1 entidade com discriminator `tipo: Lead\|Oportunidade`) ou separar (2 tabelas + status flow). Bruno indicou separar via MCP CRM mas o arv-crm já está com unificado. **Levantar essa questão no SPEC.** |
| **Orçamento como entidade própria com versionamento** (`06_ORCAMENTOS`) | não (24 campos financeiros no Pipeline) | **não** | **incorporar** — entidade nova `Orcamento` com versão, FK Oportunidade, blocos financeiros, link CMV/ROI |
| **Tarefas vinculadas a Lead E Oportunidade (não só Pipeline)** | não (mirror Pipeline) | parcial (Atividade tem FK Lead) | já alinhado |
| **Contas / Pós-Venda com Health Score, NPS, Cross-sell** (`10_CONTAS`) | parcial (Gestão de Contas com Categoria/Status, mas sem health/NPS) | **não** | **incorporar** — entidade nova `Conta` com FK Empresa, NPS, Health, Cross-sell. Pode entrar como Fase 2 do arv-crm (pós-venda). |
| **HISTORICO_FASES como audit trail** (`HISTORICO_FASES`) | não (Monday tem activity log próprio) | sim (`models/historico_etapa.py` já existe) | já alinhado |
| **Impostos em % (não R$)** | não (Pipeline armazena valores absolutos) | não verificado | **decisão de modelagem** — % é mais escalável (alíquotas mudam por imposto e segmento). Recomendo: armazenar % e calcular R$ derivado. |
| **`Tempo na Etapa` via tipo `time_tracking`** | não (calculado por fórmula sobre datas) | parcial (HistoricoEtapa permite calcular) | já alinhado |
| **Descrição na metadata do board** (cada board MCP tem `description`) | não | n/a | irrelevante para arv-crm |

### C. Buracos detectados (precisam decisão de design no SPEC)

Conceitos pedidos por `dashboards.txt` ou `travas.txt` mas que **não têm correspondência clara em nenhum dos 2 workspaces** ou existem com modelagem inadequada:

#### C.1 Temperatura Comercial vs Temperatura Técnica
- **Pipeline:** col 180 `Temperatura` (status, 6 labels), col 168 `Score Técnico` (status, 5 labels). São 2 conceitos distintos: Temperatura = score oportunidade (BANT/MEDDIC), Score Técnico = viabilidade técnica.
- **MCP CRM:** col `Temperatura` em Lead (placeholder) E em Oportunidade (placeholder) — ainda não diferenciou Comercial vs Técnica.
- **dashboards.txt** "Saúde do Funil" pede 2 visualizações distintas: "Temperatura de Oportunidades no Funil" + "Total Temperatura Comercial" + "Temperatura Técnica no Funil" + "Total Temperatura Técnica".
- **Conclusão:** modelo arv-crm precisa de **2 enums separados**: `temperatura_comercial: Enum` (Frio/Morno/Quente/MuitoQuente/Congelado/NãoAplicado) e `temperatura_tecnica: Enum` (mesmos labels). Ambos derivados de scoring_service. **CONFIRMADO COMO BURACO.**

#### C.2 Meta de vendas individual e global
- **Pipeline:** col 117 `Previsão Meta no Ano` tem **R$ 7.562.285,08 hardcoded** na fórmula. Col 118 `Previsão Meta no Mês` tem **R$ 630.190,59 hardcoded**. Col 123 `META LEADS (NÃO APAGAR)` é numbers usado como tag/marker.
- **MCP CRM:** **não tem board de Meta**. Conceito ausente.
- **dashboards.txt** pede metas: "Entrada Leads (Meta 300)", "Prospecção ativa (Meta 40 por responsável/mês)", "Meta de Vendas (Previsão e Antecipação)" com R$ 568.287 hardcoded em outro lugar.
- **Conclusão:** entidade NOVA no arv-crm: `MetaVendas` com campos `(periodo: ano|mes, valor_brl, responsavel_id: nullable User, tipo: Enum[GLOBAL_VOLUME, GLOBAL_VALOR, INDIV_VENDEDOR, INDIV_PRE_VENDEDOR, ENTRADA_LEAD, PROSP_ATIVA])`. **CONFIRMADO COMO BURACO.**

#### C.3 Próxima Atividade (campo derivado vs explícito)
- **Pipeline:** tem `Próx. Atividade` (col 59, status com 24 labels = TIPO da próxima ação) + `Data Próx. Atividade` (col 60). **Não há FK a uma Atividade real**, é só um campo descritivo manualmente preenchido.
- **MCP CRM:** col `Próx. Atividade` em Lead (placeholder) + col `Data Próx. Atividade` (date). Mesma estrutura, sem FK.
- **dashboards.txt** "Check-in" pede "Lead sem Próxima Atividade por Responsável Comercial" (gráfico pizza) — implica que precisa identificar leads cujo próximo atividade está vencido OU não existe.
- **Conclusão:** no arv-crm, **derivar próxima atividade** a partir de `Atividade.where(lead_id=X, data_inicio>=now, status=NaoIniciado).order_by(data_inicio).first()`. Adicionar em `lead_service.py` campo computed `proxima_atividade: Atividade | None`. NÃO criar campo flat. **REFUTADO** — modelagem clara, mas precisa documentar a decisão no SPEC.

#### C.4 Visita planejada/agendada/realizada com geo
- **Comercial 💰:** Calendário de Visitas (533 items, 24 cols) tem **`location` (Monday geo)** + mirror de "Distância da planta" + 4 status para Zona/Cidade/Estado/Vendedor + Perfil da Visita (8 labels).
- **MCP CRM:** `08_VISITAS` (10 cols) **NÃO tem `location` nem mirror geo**. Tem só Cidade(text), Estado(status placeholder), Zona(status placeholder).
- **dashboards.txt** "Planejamento de Visita" pede: "Planejadas/Agendadas por Zonas de SP", "Planejadas/Agendadas por Estados", e "Visitas com Datas Passadas Não Remanejadas" (visitas vencidas sem reagendamento).
- **Conclusão:** arv-crm precisa de modelagem geo no Atividade (subtipo Visita): campos `zona_sp: Enum`, `estado: str`, `cidade: str`, `lat: float`, `lng: float`, `distancia_planta_km: int`. Bruno **simplificou no MCP** (removeu geo). Precisa decidir: incorporar geo ou não? Se incorporar, é trabalho adicional vs. baseline arv-crm. **PARCIALMENTE REFUTADO** — existe no legado, mas Bruno o removeu intencionalmente no redesign. **Resolver no SPEC: keep ou drop geo?**

#### C.5 OS / Pasta do Projeto (handoff CRM → PM)
- **Pipeline:** col 148 `Pasta do Projeto Atualizada` (status Sim/Não) + col 149 `Número da OS` (text) + col 156 `Portfólio de Automação` (board_relation → workspace Projetos). Esses 3 campos juntos formam o **handoff CRM→PM**: trava no Pedido Convertido em Venda.
- **MCP CRM:** **NÃO TEM EQUIVALENTE**. `05_OPORTUNIDADES` tem coluna "Convertido em Projeto 🚀" como grupo, mas sem campo OS, sem flag pasta atualizada, sem board_relation a Portfólio.
- **dashboards.txt** + travas.txt mencionam "PASTA DO PROJETO ATUALIZADA Sim", "NÚMERO DA O.S. PREENCHIDO" como travas obrigatórias.
- **Conclusão:** arv-crm precisa de campos `numero_os: str` + `pasta_projeto_atualizada: bool` + futura FK `projeto_id: int → arv-pm.Projeto` (Fase 2 quando arv-pm existir). **CONFIRMADO COMO BURACO** — Bruno esqueceu de modelar isso no MCP CRM redesign (omissão). Importante para SPEC porque é a interface de saída do CRM.

#### C.6 Score Lead (ICP) vs Score Oportunidade (BANT/MEDDIC) — 1 ou 2 sistemas?
- **Pipeline:** **3 sistemas coexistem**:
  - **Lead Score (ICP):** col 32 numbers + col 33 Classificação (4 labels A/B/C/D), botão col 31 `Gerar Leadscore`. Avalia FIT do lead (segmento, porte, distância, já cliente etc).
  - **Score Técnico (viabilidade):** cols 157-167 (9 perguntas tech v2) + botão col 166 + col 168 status com 5 labels (Frio/Morno/Quente...). Avalia se ARV consegue entregar.
  - **Score Oportunidade (BANT/MEDDIC):** cols 64-77 (BANT/MEDDIC v1, 14 perguntas — col 78 placeholder) + cols 170-177 (versão "v2" com 8 perguntas, parcialmente DUPLICADAS de v1) + botão col 178 + col 179 numbers + col 180 Temperatura status (6 labels).
- **MCP CRM:** simplificou para **2 sistemas**: `Lead Score` (numbers em 04_LEADS) + `Score Técnico` (numbers em 05_OPORTUNIDADES) + `Score Oportunidade` (numbers em 05_OPORTUNIDADES). Mantém 3 mas sem perguntas estruturadas.
- **dashboards.txt** "Entrada de Leads" pede "Quantidade/Qualidade dos Leads Qualificados – ICP" (gráfico de barras). Não menciona BANT explicitamente, mas o sistema de travas implica scoring.
- **Conclusão:** arv-crm já tem `models/scoring_resposta.py` (1 modelo só). **Recomendo manter 3 sistemas distintos como categorias dentro de scoring_resposta**: `categoria: Enum[LEAD_ICP, TECH_VIABILIDADE, OPP_BANT_MEDDIC]`. Cada categoria tem suas próprias perguntas. **CONFIRMADO COMO BURACO** — precisa de catálogo explícito de perguntas para cada categoria (deduplicar v1/v2 do legado), e recomendo formalizar 3 enums + 3 endpoints calc.

---

## Apêndice: Surpresas relevantes

1. **Meta de vendas hardcoded em 2 fórmulas do Pipeline.** R$ 7.562.285,08 (anual) e R$ 630.190,59 (mensal = anual÷12) — na fórmula da coluna, não em uma config. Atualizar meta = editar fórmula. Anti-pattern severo.
2. **Sistema BANT/MEDDIC duplicado v1 + v2 no Pipeline.** 14 perguntas v1 (cols 64-77, prefix `color_mksx*`) + 8 perguntas v2 (cols 170-177, prefix `color_mkzn*`) — várias DUPLICADAS literais ("Quais resultados esperados?" aparece com IDs diferentes). Resultado: 2 versões coexistem sem fonte da verdade. Bruno provavelmente reformulou v1 em v2 mas não desativou v1.
3. **Campo `Status da Projeção` (col 78) com labels-default Monday placeholder** — "Em andamento/Feito/Parado". Nunca configurado. Está no Pipeline em produção há 2+ anos com 1.875 items.
4. **Campo `Temos todas as informações técnicas` (col 151) usa status com 3 labels (Em andamento/Feito/Parado)** mas TRAVA exige Sim/Não. Bug de tipo: a regra de trava lê "Feito" como "Sim", o que é frágil.
5. **Coluna `Números` no Calendário de Visitas (col 24, id `numeric_mktvdpy6`).** Nome genérico, sem contexto, provável zumbi.
6. **Fórmula `Proposta sem Imposto` inclui IR e CSLL no SUM.** Possível bug semântico: IR/CSLL **são** impostos. O nome diz "sem imposto" mas a fórmula inclui esses 2.
7. **MCP CRM tem `top_group=Inativos`/`Canceladas` como default em TODOS os 11 boards.** Bug de configuração consistente. Provável que o script/MCP de criação aplicou o último grupo como default em vez do primeiro.
8. **Workspace MCP CRM diz ter 12 boards, mas `workspace_info` retorna 11.** Discrepância com `MONDAY-INVENTORY.md` anterior (que contou 12). Real: **11 boards** distribuídos em 6 folders.
9. **`05_OPORTUNIDADES` tem grupo lixo "Group Title" não-usado** (last group, sem items, deveria ter sido removido). Mesmo lixo aparece em `06_ORCAMENTOS`, `07_TAREFAS`, `08_VISITAS`, `09_TAREFAS_TECNICAS`, `HISTORICO_FASES`. Resíduo de template Monday padrão.
10. **`02_CONTATOS.Empresa` usa `board_relation` simples** (não tem `allowMultipleItems` — implicitamente é N:1). Mas Monday board_relation é tecnicamente N:N. arv-crm pode modelar como FK (1:N: 1 contato pertence a 1 empresa, 1 empresa tem N contatos).
11. **24 labels de "Próx. Atividade" no Pipeline (col 59) vs 21 labels no Tarefas (col 9)** — sobreposição mas não 100% igual. "Reunião agendada 🗓️" vs "Reunião Agendada 🗓️" (capitalização diferente, IDs diferentes — Monday vê como labels distintas).
