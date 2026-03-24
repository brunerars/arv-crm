"""SLA rules per stage and origin type. Single source of truth."""

# Key: (etapa, origem_tipo, origem_sub_tipo)
# Value: max days allowed in stage
SLA_RULES: dict[tuple[str, str | None, str | None], int] = {
    ("prospeccao", "passiva", None): 3,
    ("prospeccao", "ativa", "vendas"): 15,
    ("prospeccao", "ativa", "pre_vendas"): 7,
    ("primeiro_contato", "passiva", None): 7,
    ("primeiro_contato", "ativa", "vendas"): 30,
    ("primeiro_contato", "ativa", "pre_vendas"): 20,
    ("qualificacao", None, None): 15,
}
