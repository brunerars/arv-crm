"""ICP scoring legado (substituido na Macro B pelo icp_calculator.py + scoring_catalog.py).

Adaptado pra usar campos pos-007 (segmento_mercado FK, quantidade_funcionarios int,
n_plantas_industriais, distancia_planta_km). Valores nas regras permanecem os mesmos
do v1 ate Macro B reescrever via SPEC §5.
"""
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from models.lead import Lead
from models.referencia import SegmentoMercado
from models.scoring_resposta import ScoringResposta

SCORING_RULES = {
    "segmento": {
        "automotivo": 25, "alimentos": 20, "farmaceutico": 20,
        "metalurgia": 15, "quimico": 15, "plasticos": 10,
    },
    "funcionarios_bucket": {
        "1-50": 5, "51-200": 10, "201-500": 15, "501-1000": 20, "1000+": 25,
    },
    "n_plantas_industriais": {
        1: 5, 2: 10, 3: 15,
    },
    "distancia_planta_km": {
        50: 25, 100: 20, 200: 15, 500: 10,
    },
}


def _funcionarios_bucket(n: int) -> str:
    if n <= 50:
        return "1-50"
    if n <= 200:
        return "51-200"
    if n <= 500:
        return "201-500"
    if n <= 1000:
        return "501-1000"
    return "1000+"


class ScoringService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def calculate_score(self, lead: Lead) -> Lead:
        empresa = lead.empresa
        if not empresa:
            return lead

        await self.db.execute(
            delete(ScoringResposta).where(ScoringResposta.lead_id == lead.id)
        )

        total_score = 0
        respostas: list[ScoringResposta] = []

        if empresa.segmento_mercado_id:
            seg_result = await self.db.execute(
                select(SegmentoMercado).where(SegmentoMercado.id == empresa.segmento_mercado_id)
            )
            seg_obj = seg_result.scalar_one_or_none()
            if seg_obj:
                seg_lower = seg_obj.nome.lower()
                for key, points in SCORING_RULES["segmento"].items():
                    if key in seg_lower:
                        respostas.append(ScoringResposta(
                            lead_id=lead.id, criterio="segmento", valor=seg_obj.nome, pontos=points
                        ))
                        total_score += points
                        break

        if empresa.quantidade_funcionarios:
            bucket = _funcionarios_bucket(empresa.quantidade_funcionarios)
            points = SCORING_RULES["funcionarios_bucket"].get(bucket, 5)
            respostas.append(ScoringResposta(
                lead_id=lead.id,
                criterio="quantidade_funcionarios",
                valor=str(empresa.quantidade_funcionarios),
                pontos=points,
            ))
            total_score += points

        if empresa.n_plantas_industriais:
            plants = empresa.n_plantas_industriais
            points = 5
            for threshold, pts in sorted(SCORING_RULES["n_plantas_industriais"].items()):
                if plants >= threshold:
                    points = pts
            respostas.append(ScoringResposta(
                lead_id=lead.id,
                criterio="n_plantas_industriais",
                valor=str(plants),
                pontos=points,
            ))
            total_score += points

        if empresa.distancia_planta_km:
            dist = float(empresa.distancia_planta_km)
            points = 5
            for threshold in sorted(SCORING_RULES["distancia_planta_km"].keys()):
                if dist <= threshold:
                    points = SCORING_RULES["distancia_planta_km"][threshold]
                    break
            respostas.append(ScoringResposta(
                lead_id=lead.id,
                criterio="distancia_planta_km",
                valor=str(dist),
                pontos=points,
            ))
            total_score += points

        for r in respostas:
            self.db.add(r)

        lead.lead_score = total_score
        if total_score >= 70:
            lead.classificacao = "A"
        elif total_score >= 50:
            lead.classificacao = "B"
        elif total_score >= 30:
            lead.classificacao = "C"
        else:
            lead.classificacao = "D"

        await self.db.commit()
        await self.db.refresh(lead)
        return lead
