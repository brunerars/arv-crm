from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from models.lead import Lead
from models.scoring_resposta import ScoringResposta

SCORING_RULES = {
    "segmento": {
        "automotivo": 25, "alimentos": 20, "farmaceutico": 20,
        "metalurgia": 15, "quimico": 15, "plasticos": 10,
    },
    "num_funcionarios": {
        "1-50": 5, "51-200": 10, "201-500": 15, "501-1000": 20, "1000+": 25,
    },
    "num_plantas": {
        1: 5, 2: 10, 3: 15,
    },
    "distancia_arv_km": {
        50: 25, 100: 20, 200: 15, 500: 10,
    },
}


class ScoringService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def calculate_score(self, lead: Lead) -> Lead:
        empresa = lead.empresa
        if not empresa:
            return lead

        # Clear previous scoring
        await self.db.execute(
            delete(ScoringResposta).where(ScoringResposta.lead_id == lead.id)
        )

        total_score = 0
        respostas = []

        # Segmento
        if empresa.segmento:
            seg_lower = empresa.segmento.lower()
            for key, points in SCORING_RULES["segmento"].items():
                if key in seg_lower:
                    respostas.append(ScoringResposta(
                        lead_id=lead.id, criterio="segmento", valor=empresa.segmento, pontos=points
                    ))
                    total_score += points
                    break

        # Funcionarios
        if empresa.num_funcionarios:
            points = SCORING_RULES["num_funcionarios"].get(empresa.num_funcionarios, 5)
            respostas.append(ScoringResposta(
                lead_id=lead.id, criterio="num_funcionarios", valor=empresa.num_funcionarios, pontos=points
            ))
            total_score += points

        # Plantas
        if empresa.num_plantas:
            plants = empresa.num_plantas
            points = 5
            for threshold, pts in sorted(SCORING_RULES["num_plantas"].items()):
                if plants >= threshold:
                    points = pts
            respostas.append(ScoringResposta(
                lead_id=lead.id, criterio="num_plantas", valor=str(empresa.num_plantas), pontos=points
            ))
            total_score += points

        # Distancia
        if empresa.distancia_arv_km:
            dist = float(empresa.distancia_arv_km)
            points = 5
            for threshold in sorted(SCORING_RULES["distancia_arv_km"].keys()):
                if dist <= threshold:
                    points = SCORING_RULES["distancia_arv_km"][threshold]
                    break
            respostas.append(ScoringResposta(
                lead_id=lead.id, criterio="distancia_arv_km", valor=str(dist), pontos=points
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
