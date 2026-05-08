"""SLA rules per stage and origin type. Single source of truth.

SPEC §6 matriz origem x etapa. Etapas pos-015 (5 valores SPEC §3.1).
"""

# Key: (etapa, origem_tipo, origem_sub_tipo)
# Value: max days allowed in stage
SLA_RULES: dict[tuple[str, str | None, str | None], int] = {
    ("LEAD_INICIAL", "passiva", None): 3,
    ("LEAD_INICIAL", "ativa", "vendas"): 15,
    ("LEAD_INICIAL", "ativa", "pre_vendas"): 7,
    ("ANALISE_INTERNA", None, None): 5,
    ("QUALIFICACAO_INICIAL", "passiva", None): 7,
    ("QUALIFICACAO_INICIAL", "ativa", "vendas"): 30,
    ("QUALIFICACAO_INICIAL", "ativa", "pre_vendas"): 20,
    ("QUALIFICACAO_OPORTUNIDADE", None, None): 15,
}
